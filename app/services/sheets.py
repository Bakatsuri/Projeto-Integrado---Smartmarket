from auth import conectar_planilha
import re
import time
import unicodedata
from rapidfuzz import fuzz

id_sheets = "1gN1ZkxJWPEUN-AOiXYUxRf7iBlzqCV0LiARjIdpU2eE"

_cache_produtos = None
_cache_atualizado = 0
TEMPO_CACHE = 30


def normalizar_texto(texto):
    texto = str(texto).casefold().strip()

    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )

    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return " ".join(texto.split())
def obter_aba():
    client = conectar_planilha()
    planilha = client.open_by_key(id_sheets)
    return planilha.sheet1


def listar_produtos():
    global _cache_produtos, _cache_atualizado

    agora = time.monotonic()

    if (
        _cache_produtos is None
        or agora - _cache_atualizado > TEMPO_CACHE
    ):
        _cache_produtos = obter_aba().get_all_records()
        _cache_atualizado = agora

    return [dict(produto) for produto in _cache_produtos]

def buscar_por_nome(nome):
    consulta = normalizar_texto(nome)

    if not consulta:
        return []

    produtos = listar_produtos()
    resultados = []

    for produto in produtos:
        nome_produto = normalizar_texto(produto.get("nome", ""))

        if consulta in nome_produto:
            pontuacao = 100
        else:
            pontuacao = fuzz.WRatio(consulta, nome_produto)

        if pontuacao >= 65:
            resultados.append((pontuacao, produto))

    resultados.sort(key=lambda item: item[0], reverse=True)

    return [produto for _, produto in resultados]

def buscar_sugestoes(nome, limite=6):
    return buscar_por_nome(nome)[:limite]

def buscar_por_id(id_produto):
    id_produto = str(id_produto).strip()
    produtos = listar_produtos()

    for produto in produtos:
        if str(produto.get("id", "")).strip() == str(id_produto).strip():
            return produto

    return None
