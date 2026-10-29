import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def conectar_planilha():
    credentials = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    return client