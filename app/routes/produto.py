from flask import Flask, render_template, Blueprint

produto_bp = Blueprint("produto", __name__)

@produto_bp.route("/produto")
def produto():
    return render_template("produto.html")