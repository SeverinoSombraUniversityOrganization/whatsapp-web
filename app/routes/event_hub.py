from app import app, WhatsAppClient
from flask import request, jsonify
from services.whasts_app_client_service import WhatsAppClient
from utils.whats_app_object import WhatsAppObject

@app.route('/api/event-hub/<identifier>/', methods=['POST'])
def event_hub(identifier):
    """
    Rota Flask para manipulação de eventos em um cliente WhatsApp específico.

    Parameters:
        identifier (str): Identificador do cliente WhatsApp.

    Returns:
        jsonify: Resposta JSON indicando o status da operação.

    """
    identifier = int(identifier)
    whats_app_client = WhatsAppClient.identifiers.get(identifier)

    # Verifica se o cliente WhatsApp com o identificador fornecido foi encontrado
    if not whats_app_client:
        return jsonify({'error': f'WhatsAppClient with identifier {identifier} not found'}), 404

    data = request.json
    event_name = data.get('event')
    arguments = data.get('arguments', [])

    # Verifica se o campo 'event' está presente nos dados da solicitação
    if not event_name:
        return jsonify({'error': 'Event field is required in the request data'}), 400
    
    argument_configs = {}
    processed_arguments = WhatsAppObject.js_objects_to_python_objects(arguments, argument_configs)

    try:
        # Tenta acionar o evento no cliente WhatsApp
        whats_app_client.trigger_event(event_name, *processed_arguments)
        return jsonify({
            'message': f'Event {event_name} triggered successfully for WhatsAppClient {identifier}',
            'argConfig': argument_configs
        })
    except Exception as e:
        # Retorna um erro em caso de falha ao acionar o evento
        return jsonify({'error': f'Error triggering event {event_name} for WhatsAppClient {identifier}'}), 500
