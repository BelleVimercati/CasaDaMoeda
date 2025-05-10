import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from handlers.callbacks import buttonOptions
from dotenv import load_dotenv
from bot import *
from core.actions import *
from handlers.callbacks import buttonOptions


load_dotenv()
token_bot = os.environ.get("TOKEN_BOT")

# Inicialização do Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(token_bot).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttonOptions))
    # chama handle_message() para qualquer texto que não seja comando — é aqui que ele verifica se você está enviando um gasto.
    app.add_handler(CommandHandler("gasto", registrar_gasto))
    app.add_handler(CommandHandler("listar", listar_gastos))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot em execução...")
    app.run_polling()
