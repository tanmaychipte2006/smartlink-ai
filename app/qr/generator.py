import os
import qrcode


def generate_qr(short_url: str, filename: str):

    os.makedirs("qrcodes", exist_ok=True)

    img = qrcode.make(short_url)

    path = f"qrcodes/{filename}.png"

    img.save(path)

    return path