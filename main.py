import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bot import registrar_gasto, listar_gastos


load_dotenv()
token_bot = os.environ.get("TOKEN_BOT")


# === INICIAR O BOT ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(token_bot).build()

    app.add_handler(CommandHandler("gasto", registrar_gasto))
    app.add_handler(CommandHandler("listar", listar_gastos))

    print("Bot em execução...")
    app.run_polling()
