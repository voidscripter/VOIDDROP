"""QR code generation for the currently advertised LAN URL."""

from io import BytesIO


def qr_png(url: str) -> bytes:
    import qrcode
    image = qrcode.make(url)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()
