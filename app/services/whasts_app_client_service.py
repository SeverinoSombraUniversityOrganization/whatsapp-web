import requests
from config.api_provider_config import API_PROVIDER_BASE_URL
from .event_hub_service import EventHub

class WhatsAppClient(EventHub):
    identifiers = {}

    @classmethod
    def build_url(cls, path):
        return f"{API_PROVIDER_BASE_URL}{path}"
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._generate_identifier()
        self.register_events()
        self.started = False

    def _generate_identifier(self):
        total_whats_app_clients = len(WhatsAppClient.identifiers.keys())
        self.identifier = total_whats_app_clients + 1
        WhatsAppClient.identifiers[self.identifier] = self

    def initialize(self):
        if self.started == False:
            url = self.build_url(f'initialize-client/{str(self.identifier)}')

            try:
                response = requests.post(url)
                response.raise_for_status()
                response_data = response.json()
                print(response_data['message'])
                self.started = True
                return True
            except requests.RequestException as e:
                print(f"Erro na solicitação: {e}")
                return False

    def register_events(self):
        self.on('qr', lambda qr, *args, **kwargs: print(f"QR Code received: {qr}"))
