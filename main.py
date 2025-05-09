import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
from bot import registrar_gasto, listar_gastos, start, buttonOptions, handle_message


load_dotenv()
token_bot = os.environ.get("TOKEN_BOT")

# Inicialização do Bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(token_bot).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttonOptions))
    app.add_handler(CommandHandler("gasto", registrar_gasto))
    app.add_handler(CommandHandler("listar", listar_gastos))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot em execução...")
    app.run_polling()
