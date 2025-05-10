from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from core.actions import *

# Função que exibe os botões ao usuário
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Registrar Gasto", callback_data="Registro"),
            InlineKeyboardButton("Listar Gastos", callback_data="Consulta"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha sua opção:", reply_markup=reply_markup)


# Lida com mensagens enviadas diretamente
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_expense'):
        await tratar_categoria(update, context)
        context.user_data['awaiting_expense'] = False
    else:
        await update.message.reply_text("Envie /start para ver as opções disponíveis.")
