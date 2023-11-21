# Importando a classe Flask do módulo Flask
from flask import Flask

# Importando a configuração de execução da aplicação
from config.app_run_config import APP_RUN_CONFIG

# Importando as classes necessárias para o cliente WhatsApp e manipulador de eventos
from services.whasts_app_client_service import WhatsAppClient
from services.whats_app_client_handlers import WhatsAppClientHandler

# Importando a biblioteca time para introduzir um pequeno atraso antes da execução
import time

# Criando uma instância da aplicação Flask
app = Flask(__name__)
app.template_folder = 'templates'  # Configurando a pasta de templates da aplicação

# Importando as rotas definidas no arquivo 'routes'
from routes import *

# Verificando se o script está sendo executado diretamente
if __name__ == '__main__':
    # Introduzindo um pequeno atraso antes da criação do cliente WhatsApp
    time.sleep(2)

    # Criando uma instância do cliente WhatsApp e do manipulador de eventos
    client = WhatsAppClient(app)
    client_events_handler = WhatsAppClientHandler(app)

    # Registrando os métodos do manipulador de eventos para os eventos 'qr' e 'message' do cliente WhatsApp
    client.on('qr', client_events_handler.qr)
    client.on('message', client_events_handler.message)

    # Inicializando o cliente WhatsApp
    client.initialize()

    # Executando a aplicação Flask com as configurações fornecidas
    app.run(**APP_RUN_CONFIG)
