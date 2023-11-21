from utils.generate_and_save_qr import generate_and_save_qr


class WhatsAppClientHandler:

    def __init__(self, app) -> None:
        self.app = app

    def qr(self, qr, *args, **kwargs):
        return generate_and_save_qr(self.app, qr)

    def message(self, message, *args, **kwargs):
        message_content = message.body
        menu_options = [
            '1. Opção 1',
            '2. Opção 2',
            '3. Opção 3',
        ]

        menu_message = f'Escolha uma opção:\n{"\n".join(menu_options)}'
        message.reply(menu_message)