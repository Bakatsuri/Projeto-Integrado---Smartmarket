from auth import conectar_planilha

id_sheets = "1gN1ZkxJWPEUN-AOiXYUxRf7iBlzqCV0LiARjIdpU2eE"

def obter_aba():
    client = conectar_planilha()
    planilha = client.open_by_key(id_sheets)
    return planilha.sheet1


def listar_produtos():
    return obter_aba().get_all_records()


def buscar_por_nome(nome):
    nome = nome.strip().casefold()

    if not nome:
        return []

    produtos = listar_produtos()

    return [
        produto
        for produto in produtos
        if nome in str(produto.get("nome", "")).casefold()
    ]


def buscar_por_id(id_produto):
    id_produto = str(id_produto).strip()
    produtos = listar_produtos()

    for produto in produtos:
        if str(produto.get("id", "")).strip() == str(id_produto).strip():
            return produto

    return None
