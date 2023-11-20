from app import app

@app.route('/')
def welcome():
    return f'Bem-vindo ao seu aplicativo Flask!'

