from app import app, WhatsAppClient
from flask import request, jsonify
from services.whasts_app_client_service import WhatsAppClient

@app.route('/api/event-hub/<identifier>/', methods=['POST'])
def event_hub(identifier):
    identifier = int(identifier)
    whats_app_client = WhatsAppClient.identifiers.get(identifier)

    if not whats_app_client:
        return jsonify({'error': f'WhatsAppClient with identifier {identifier} not found'}), 404

    data = request.json
    event = data.get('event')
    arguments = data.get('arguments', {})

    if not event:
        return jsonify({'error': 'Event field is required in the request data'}), 400
    
    whats_app_client.trigger_event(event, *arguments)
    return jsonify({'message': f'Event {event} triggered successfully for WhatsAppClient {identifier}'})