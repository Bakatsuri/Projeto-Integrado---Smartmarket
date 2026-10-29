
from flask import Blueprint, render_template, request

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "services"))

from sheets import buscar_por_id, buscar_por_nome # type: ignore

produto_bp = Blueprint("produto", __name__)


@produto_bp.route("/produto")
def produto():
    id_produto = request.args.get("id")
    nome = request.args.get("q", "").strip()

    # Acesso direto pelo ID (QR Code ou link)
    if id_produto:
        dados_produto = buscar_por_id(id_produto)

        if dados_produto is None:
            return render_template(
                "erro.html",
                error=404,
                descricao="Produto não encontrado"
            ), 404

        return render_template("produto.html", produto=dados_produto)


    if nome:
        resultados = buscar_por_nome(nome)

        if len(resultados) == 1:
            return render_template(
                "produto.html",
                produto=buscar_por_id(resultados[0]["id"])
            )

        if len(resultados) > 1:
            return render_template(
                "resultados.html",
                produtos=resultados,
                busca=nome
            )



    return render_template("produto.html", produto=None)

