import qrcode
from io import BytesIO


def gerar_qrcode(url):
    """
    Gera um QR Code a partir de uma URL e retorna a imagem em memória.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    imagem = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    arquivo = BytesIO()
    imagem.save(arquivo, format="PNG")
    arquivo.seek(0)

    return arquivo