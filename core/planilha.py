import os
from dotenv import load_dotenv
from core.sheets import conectGoogle

load_dotenv()

planilha_id = os.environ.get("PLANILHA_ID")
arquivo_credenciais = os.environ.get("ARQUIVO_CREDENCIAIS")

planilha = conectGoogle(arquivo_credenciais, planilha_id)
