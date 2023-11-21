from app import app, WhatsAppClient
from flask import request, jsonify
from services.whasts_app_client_service import WhatsAppClient
from utils.whats_app_object import WhatsAppObject

@app.route('/api/event-hub/<identifier>/', methods=['POST'])
def event_hub(identifier):
    identifier = int(identifier)
    whats_app_client = WhatsAppClient.identifiers.get(identifier)

    if not whats_app_client:
        return jsonify({'error': f'WhatsAppClient with identifier {identifier} not found'}), 404

    data = request.json
    event_name = data.get('event')
    arguments = data.get('arguments', [])

    with open(f"logs/whats-app-clients/{identifier}-logs-{event_name}.txt", 'a') as file:
        file.write(str(arguments)  + '\n')

    if not event_name:
        return jsonify({'error': 'Event field is required in the request data'}), 400
    
    argument_configs = {}
    processed_arguments = WhatsAppObject.js_objects_to_python_objects(arguments, argument_configs)
    whats_app_client.trigger_event(event_name, *processed_arguments)

    return jsonify({
        'message': f'Event {event_name} triggered successfully for WhatsAppClient {identifier}',
        'argConfig': argument_configs
    })