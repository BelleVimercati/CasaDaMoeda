import os
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from dotenv import load_dotenv
from sheets import conectGoogle


load_dotenv()
planilha_id = os.environ.get("PLANILHA_ID")
arquivo_credenciais = os.environ.get("ARQUIVO_CREDENCIAIS")

planilha = conectGoogle(arquivo_credenciais, planilha_id)

# === COMANDO /gasto ===
async def registrar_gasto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        partes = update.message.text.split(" ")
        if len(partes) != 4:
            raise ValueError("Formato incorreto")

        descricao = partes[1]
        categoria = partes[2]
        valor = float(partes[3])
        data = datetime.now().strftime("%d/%m/%Y")

        planilha.append_row([data, descricao, categoria, valor])

        await update.message.reply_text(
            f"✅ Gasto registrado:\n📌 {descricao} | 🏷 {categoria} | 💰 R$ {valor:.2f}"
        )
    except:
        await update.message.reply_text("⚠️ Formato inválido. Use:\n/gasto Descrição Categoria Valor")

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