from flask import Blueprint, render_template, request, jsonify

import sys
from pathlib import Path

from flask import Blueprint, render_template, request
from flask import url_for, send_file, abort

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(str(BASE_DIR / "services"))
sys.path.append(str(BASE_DIR / "scripts"))

from sheets import buscar_por_id, buscar_por_nome, buscar_sugestoes # type: ignore
from gerar_qrcode import gerar_qrcode # type: ignore

produto_bp = Blueprint("produto", __name__)

@produto_bp.route("/api/produtos/sugestoes")
def sugestoes_produtos():
    nome = request.args.get("q", "").strip()

    if len(nome) < 2:
        return jsonify([])

    sugestoes = buscar_sugestoes(nome)

    return jsonify([
        {
            "id": produto["id"],
            "nome": produto["nome"]
        }
        for produto in sugestoes
    ])
    
@produto_bp.route("/qrcode/<int:produto_id>")
def qrcode_produto(produto_id):
    # Verifica se o produto existe
    produto = buscar_por_id(produto_id)

    if not produto:
        abort(404)

    # Monta a URL da página do produto
    url_produto = url_for(
        "produto.produto",
        id=produto_id,
        _external=True
    )

    # Gera o QR Code
    imagem = gerar_qrcode(url_produto)

    # Verifica se o usuário solicitou o download
    download = request.args.get("download") == "1"

    return send_file(
        imagem,
        mimetype="image/png",
        as_attachment=download,
        download_name=f"qrcode_produto_{produto_id}.png"
    )

@produto_bp.route("/produto")
def produto():
    id_produto = request.args.get("id")
    nome = request.args.get("q", "").strip()

    # Acesso direto pelo ID (QR Code ou sugestão)
    if id_produto:
        dados_produto = buscar_por_id(id_produto)

        if dados_produto is None:
            return render_template(
                "erro.html",
                error=404,
                descricao="Produto não encontrado"
            ), 404

        return render_template(
            "produto.html",
            produto=dados_produto
        )

    # Pesquisa pelo nome
    if nome:
        resultados = buscar_por_nome(nome)

        if len(resultados) == 1:
            return render_template(
                "produto.html",
                produto=resultados[0]
            )

        return render_template(
            "produto.html",
            produto=None,
            resultados=resultados,
            busca=nome
        )

    return render_template(
        "produto.html",
        produto=None,
        resultados=[],
        busca=""
    )