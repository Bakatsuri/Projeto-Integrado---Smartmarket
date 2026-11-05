import os
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def conectar_planilha():
    caminho_credenciais = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        str(Path(__file__).resolve().parents[2] / "credentials.json")
    )

    credentials = Credentials.from_service_account_file(
        caminho_credenciais,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    return client