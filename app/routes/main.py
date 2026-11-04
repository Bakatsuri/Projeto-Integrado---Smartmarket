from flask import Flask, render_template
from produto import produto_bp
from flask import request, send_file
from gerar_qrcode import gerar_qrcode #type: ignore

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.register_blueprint(produto_bp)


@app.route("/")
def home():
    return render_template("home.html")

@app.errorhandler(404)
def not_found(error):
    erro = 404
    desc = "Pagina ou produto não encontrado"
    return render_template("erro.html", error=erro, descricao=desc)

@app.route("/qrcode")
def qrcode_home():
    url_home = request.url_root

    imagem = gerar_qrcode(url_home)

    download = request.args.get("download") == "1"

    return send_file(
        imagem,
        mimetype="image/png",
        as_attachment=download,
        download_name="qrcode_smartmarket.png"
    )
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

