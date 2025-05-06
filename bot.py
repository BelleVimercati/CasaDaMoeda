import os
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from dotenv import load_dotenv
from sheets import conectGoogle
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes


load_dotenv()
planilha_id = os.environ.get("PLANILHA_ID")
arquivo_credenciais = os.environ.get("ARQUIVO_CREDENCIAIS")

planilha = conectGoogle(arquivo_credenciais, planilha_id)


# === COMANDO /gasto ===
async def registrar_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        partes = update.message.text.split(" ", 2)
        if len(partes) < 3:
            raise ValueError("Formato incorreto")

        descricao = partes[0]
        categoria = partes[1]
        try:
            valor = float(partes[2])
        except ValueError:
            raise ValueError("Valor deve ser um número")

        data = datetime.now().strftime("%d/%m/%Y")
        planilha.append_row([data, descricao, categoria, valor])

        await update.message.reply_text(
            f"✅ Gasto registrado:\n📌 {descricao} | 🏷 {categoria} | 💰 R$ {valor:.2f}"
        )
    except Exception as e:
        await update.message.reply_text(
            await update.message.reply_text(f"⚠️ Erro: {str(e)}\nUse o formato: descrição categoria valor")
        )


# === COMANDO /listar ===
async def listar_gastos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message or update.callback_query.message
    if not message:
        print("Não foi encontrado nenhum gasto.")
        return

    try:
        dados = planilha.get_all_records()
        if not dados:
            await message.reply_text("Você ainda não registrou nenhum gasto.")
            return

        mensagem = "📋 *Seus gastos registrados:*\n"
        for reg in dados[-10:]:
            try:
                valor = float(reg["Valor"]) if reg["Valor"] else 0.0
            except ValueError:
                valor = 0.0
            mensagem += f"{reg['Data']} | {reg['Descrição']} | {reg['Categoria']} | R$ {valor:.2f}\n"

        await message.reply_text(mensagem, parse_mode="Markdown")
    except Exception as e:
        await message.reply_text("Erro ao listar gastos.")
        print(f"Erro: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Registrar Gasto", callback_data="Registro"),
            InlineKeyboardButton("Listar Gastos", callback_data="Consulta"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Escolha sua opção:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
    option = query.data
    if option == "Registro":
        context.user_data["awaiting_expense"] = True
        await query.edit_message_text(
            "Envie o gasto no formato: descrição categoria valor\n"
            "Exemplo: Almoço Alimentação 25.50"
        )
    elif option == "Consulta":
        await listar_gastos(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_expense'):
        await registrar_gasto(update, context)
        context.user_data['awaiting_expense'] = False
    else:
        await update.message.reply_text("Envie /start para ver as opções disponíveis.")
