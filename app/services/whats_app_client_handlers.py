# Importando a função 'generate_and_save_qr' do módulo 'utils'
from utils.generate_and_save_qr import generate_and_save_qr
import os
import requests

# Obtendo a chave da API OpenAI a partir de uma variável de ambiente
openai_api_key = os.getenv('OPENIA_API_KEY')

# URL da API OpenAI para solicitar completions de texto
api_url = 'https://api.openai.com/v1/engines/text-davinci-003/completions'

# Classe para manipular mensagens no cliente do WhatsApp
class WhatsAppClientHandler:

    def __init__(self, app) -> None:
        """
        Inicializa o manipulador de cliente do WhatsApp.

        Parameters:
            app: Objeto representando a aplicação do WhatsApp
        """
        self.app = app

    def qr(self, qr, *args, **kwargs):
        """
        Gera e salva um código QR.

        Parameters:
            qr: Dados para gerar o código QR

        Returns:
            None
        """
        return generate_and_save_qr(self.app, qr)

    def message(self, message, *args, **kwargs):
        """
        Manipula mensagens recebidas no cliente do WhatsApp.

        Parameters:
            message: Objeto representando a mensagem recebida

        Returns:
            None
        """
        message_content = message.body

        # Lógica condicional para diferentes tipos de mensagens
        if message_content.startswith('Quem são os alunos participantes?'):
            message_to_send = 'Os Alunos São Deivid Hugo e Rafael Pinheiro'
        elif message_content.startswith('Deu trabalho?'):
            message_to_send = 'Deu trabalho dms'
        elif message_content.startswith('Me conte sobre a sua criação?'):
            message_to_send = 'Nosso projeto, o seu passaporte para incorporar as funcionalidades \n do WhatsApp Web em projetos Python. \n Simplificando, é o wweb.js, mas em Python.'
        elif message_content.startswith('Eu quero saber'):
            response = self.make_openai_request(message_content)
            message_to_send = response['choices'][0]['text']
        else:
            menu_options = [
                'Escreva: Quem são os alunos participantes?',
                'Escreva: Deu trabalho?',
                'Escreva: Me conte sobre a sua criação?',
                'Escreva: Eu quero saber ....'
            ]
            message_to_send = f'Escreva uma opção:\n{"\n".join(menu_options)}'

        # Responde à mensagem com a mensagem apropriada
        message.reply(message_to_send)

    def make_openai_request(self, prompt):
        """
        Faz uma solicitação à API OpenAI para obter uma resposta com base no prompt fornecido.

        Parameters:
            prompt: O prompt para a solicitação à OpenAI

        Returns:
            dict: Resposta da API OpenAI em formato de dicionário
        """
        # Configuração dos cabeçalhos e dados para a solicitação à OpenAI
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}'
        }

        data = {
            'model': 'text-davinci-003',
            'prompt': prompt,
            'max_tokens': 150
        }

        # Faz a solicitação à API OpenAI e retorna a resposta como um dicionário JSON
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()
