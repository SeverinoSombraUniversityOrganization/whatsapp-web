from app import app
from flask import render_template, request, jsonify
import requests

GPT3_API_KEY = "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"

@app.route('/', methods=['GET', 'POST'])    
def index():
    if request.method == 'POST':
        try:
            user_message = request.json.get('user_message')

            if not user_message:
                return jsonify({'error': 'Campo de mensagem do usuário não fornecido'}), 400

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {GPT3_API_KEY}',
            }

            data = {
                'prompt': user_message,
                'max_tokens': 50,
            }

            gpt3_url = 'https://api.openai.com/v1/chat/completions'
            response = requests.post(gpt3_url, headers=headers, json=data)
            response.raise_for_status()

            bot_message = response.json()['choices'][0]['text'].strip()
            return jsonify({'bot_message': bot_message})

        except Exception as e:
            print(f"Erro interno: {e}")
            return jsonify({'error': 'Erro interno no servidor'}), 500

    return render_template('index.html')