import gspread
from oauth2client.service_account import ServiceAccountCredentials


def conectGoogle(arquivo_credenciais: str, planilha_id: str):
    # === CONECTAR AO GOOGLE SHEETS ===
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creeds = ServiceAccountCredentials.from_json_keyfile_name(
        filename=arquivo_credenciais, scopes=scopes
    )
    client = gspread.authorize(creeds)
    planilha = client.open_by_key(planilha_id).get_worksheet(0)
    return planilha
