from flask import Flask
from config.app_run_config import APP_RUN_CONFIG
from services.whasts_app_client_service import WhatsAppClient
import time

app = Flask(__name__)
app.template_folder = 'templates'

from routes import *

if __name__ == '__main__':
    time.sleep(2)
    client = WhatsAppClient(app)
    client.initialize()
    app.run(**APP_RUN_CONFIG)