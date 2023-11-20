from flask import Flask
from config.app_run_config import APP_RUN_CONFIG

app = Flask(__name__)

from routes import *

if __name__ == '__main__':
    app.run(**APP_RUN_CONFIG)