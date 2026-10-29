from flask import Flask, render_template
from produto import produto_bp

app = Flask(__name__, template_folder="../templates")
app.register_blueprint(produto_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def not_found(error):
    erro = 404
    desc = "Pagina ou produto não encontrado"
    return render_template("erro.html", error=erro, descricao=desc)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)