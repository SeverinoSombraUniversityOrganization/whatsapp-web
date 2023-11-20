from flask import Flask
from config.app_run_config import APP_RUN_CONFIG

app = Flask(__name__)


@app.route('/')
def welcome():
    return f'Bem-vindo ao seu aplicativo Flask!'

if __name__ == '__main__':
    app.run(**APP_RUN_CONFIG)