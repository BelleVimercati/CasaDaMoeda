from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.planilha import planilha

# Função de gasto
async def registrar_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    categoria = context.user_data.get("categoria")
    descricao = context.user_data.get("descricao")
    pagamento = context.user_data.get("pagamento")
    valor = context.user_data.get("valor")
    data = datetime.now().strftime("%d/%m/%Y")

    planilha.append_row([data, descricao, categoria, valor, pagamento])

    await query.edit_message_text(
        f"✅ Gasto registrado:\n📌 {descricao} | 🏷 {categoria} | 💰 R$ {valor:.2f} | 🏦 {pagamento}"
    )

    context.user_data.clear()


# Função de listagem
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
            mensagem += f"{reg['Data']} | {reg['Descrição']} | {reg['Categoria']} | R$ {valor:.2f} | {reg['Pagamento']}\n"

        await message.reply_text(mensagem, parse_mode="Markdown")
    except Exception as e:
        await message.reply_text("Erro ao listar gastos.")
        print(f"Erro: {e}")


# Função para a criação de botões de categoria
async def tratar_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    partes = update.message.text.split(" ", 1)
    if len(partes) < 2:
        await update.message.reply_text("Formato inválido. Use: descrição valor")
        return

    descricao = partes[0]

    try:
        valor = float(partes[1])
    except ValueError:
        await update.message.reply_text("Formato inválido. Use: descrição valor")
        return

    # Alterando o contexto da ação do usuário
    context.user_data["descricao"] = descricao
    context.user_data["valor"] = valor
    context.user_data["awaiting_expense"] = False
    context.user_data["awaiting_category"] = True

    # Criando os botões de categoria
    keyboard = [
        [InlineKeyboardButton("Essencial", callback_data="cat_Alimentação")],
        [InlineKeyboardButton("Diversão", callback_data="cat_Necessidades")],
        [InlineKeyboardButton("Caridade/Presentes", callback_data="cat_Caridade")],
        [InlineKeyboardButton("Vontades", callback_data="cat_Vontades")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma categoria:", reply_markup=reply_markup)


# Criação de botões de forma de pagamento
async def tratar_forma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["awaiting_category"] = False
    context.user_data["awaiting_pagamento"] = True

    keyboard = [
        [InlineKeyboardButton("Débito", callback_data="pg_Débito")],
        [InlineKeyboardButton("Crédito", callback_data="pg_Crédito")],
        [InlineKeyboardButton("Pix", callback_data="pg_Pix")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Escolha a forma de pagamento:", reply_markup=reply_markup
    )
