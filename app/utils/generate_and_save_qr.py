from flask import Flask, send_from_directory
import qrcode

def generate_and_save_qr(app, qr_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    static_path = 'static'
    img.save(f"{static_path}/images/whats-app-qr-code.png")

