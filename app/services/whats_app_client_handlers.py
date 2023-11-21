from utils.generate_and_save_qr import generate_and_save_qr
import os
import openai

openai.api_key = os.getenv('OPENIA_API_KEY')

class WhatsAppClientHandler:

    def __init__(self, app) -> None:
        self.app = app

    def qr(self, qr, *args, **kwargs):
        return generate_and_save_qr(self.app, qr)

    def message(self, message, *args, **kwargs):
        message_content = message.body

        if message_content.startswith('Quem são os alunos participantes?'):
            message_to_send = 'Os Alunos São Deivid Hugo e Rafael Pinheiro'
        elif message_content.startswith('Deu trabalho?'):
            message_to_send = 'Deu trabalho dms'
        elif message_content.startswith('Me conte sobre a sua criação?'):
            message_to_send = 'Nosso projeto, o seu passaporte para incorporar as funcionalidades \n do WhatsApp Web em projetos Python. \n Simplificando, é o wweb.js, mas em Python.'
        elif message_content.startswith('Eu quero saber'):
            response = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=message_content,
                max_tokens=150  
            )
            message_to_send = response['choices'][0]['text']
        else: 
            menu_options = [
                'Escreva: Quem são os alunos participantes?',
                'Escreva: Deu trabalho?',
                'Escreva: Me conte sobre a sua criação?',
                'Escreva: Eu quero saber ....'
            ]
            message_to_send = f'Escreva uma opção:\n{"\n".join(menu_options)}'

        message.reply(message_to_send)
