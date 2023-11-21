from utils.generate_and_save_qr import generate_and_save_qr


class WhatsAppClientHandler:

    def __init__(self, app) -> None:
        self.app = app

    def qr(self, qr, *args, **kwargs):
        return generate_and_save_qr(self.app, qr)

    def message(self, message, *args, **kwargs):
        
        message.reply('Calica')
        message.reply('Bora vê')