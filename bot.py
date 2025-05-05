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
        if update.message and update.message.text.startswith('/gasto'):
            partes = update.message.text.split(' ', 3)  # Divide no máximo em 4 partes
            if len(partes) < 4:
                raise ValueError("Formato incorreto")
            
            descricao = partes[1]
            categoria = partes[2]
            try:
                valor = float(partes[3])
            except ValueError:
                raise ValueError("Valor deve ser um número")
            
            data = datetime.now().strftime("%d/%m/%Y")
            
            # Aqui você deve adicionar à planilha
            planilha.append_row([data, descricao, categoria, valor])

        await update.message.reply_text(
                f"✅ Gasto registrado:\n📌 {descricao} | 🏷 {categoria} | 💰 R$ {valor:.2f}"
            )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro: {str(e)}\nUse o formato: /gasto descrição categoria valor")

# === COMANDO /listar ===
async def listar_gastos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dados = planilha.get_all_records()
        if not dados:
            await update.message.reply_text("Nenhum gasto registrado.")
            return

        mensagem = "📋 *Seus gastos registrados:*\n"
        for reg in dados[-10:]:  # mostra os últimos 10
            mensagem += f"{reg['Data']} | {reg['Descrição']} | {reg['Categoria']} | R$ {reg['Valor']:.2f}\n"

        await update.message.reply_text(mensagem, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("Erro ao listar gastos.")
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
        # Armazena que o usuário está no modo de registro
        context.user_data['awaiting_expense'] = True
        await query.edit_message_text(
            "Envie o gasto no formato: /gasto descrição categoria valor\n"
            "Exemplo: /gasto Almoço Alimentação 25.50"
        )
    elif option == "Consulta":
        await listar_gastos(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'awaiting_expense' in context.user_data and context.user_data['awaiting_expense']:
        if update.message.text.startswith('/gasto'):
            context.user_data['awaiting_expense'] = False
            await registrar_gasto(update, context)
        else:
            await update.message.reply_text("Por favor, use o comando /gasto seguido dos dados")
    else:
        # Comportamento padrão para outras mensagens
        pass