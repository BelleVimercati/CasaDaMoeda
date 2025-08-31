from telegram import Update
from telegram.ext import ContextTypes
from bot import *

# Tratamento dos clickes dos botões
async def buttonOptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
    option = query.data
    if option == "Registro":
        #O bot salva uma flag em context.user_data informando a aplicação que o usuário enviará um gasto.
        context.user_data["awaiting_expense"] = True 
        await query.edit_message_text(
            "Envie o gasto no formato: descrição valor\n"
            "Exemplo: Almoço 25.50"
        )
    elif option == "Consulta":
        await listar_gastos(update, context)

    #Botões de categorias de gastos
    elif option.startswith("cat_") and context.user_data.get("awaiting_category"):
        context.user_data["categoria"] = option.replace("cat_", "")
        await tratar_forma(update, context)

    #Botões de forma de pagamento
    elif option.startswith("pg_") and context.user_data.get("awaiting_pagamento"):
        context.user_data["pagamento"] = option.replace("pg_", "")
        await registrar_gasto(update, context)