import requests
from config.api_provider_config import API_PROVIDER_BASE_URL
from .event_hub_service import EventHub

class WhatsAppClient(EventHub):
    """
    Classe que representa um cliente do WhatsApp e herda funcionalidades de EventHub.

    Atributos de Classe:
        identifiers (dict): Dicionário para armazenar identificadores de clientes WhatsApp.

    Métodos de Classe:
        build_url(cls, path): Método de classe para construir uma URL completa a partir de um caminho.

    Métodos:
        __init__(self, app, *args, **kwargs): Método de inicialização do cliente WhatsApp.
        _generate_identifier(self): Método para gerar identificadores únicos para instâncias de clientes WhatsApp.
        initialize(self): Método para inicializar o cliente WhatsApp.

    Atributos:
        identifier (int): Identificador único atribuído ao cliente WhatsApp.
        started (bool): Indica se o cliente WhatsApp foi iniciado.

    """

    identifiers = {}

    @classmethod
    def build_url(cls, path):
        """
        Método de classe para construir uma URL completa a partir de um caminho.

        Parameters:
            path (str): Caminho a ser anexado à URL base.

        Returns:
            str: URL completa resultante.

        """
        return f"{API_PROVIDER_BASE_URL}{path}"
    
    def __init__(self, app, *args, **kwargs) -> None:
        """
        Inicializa o cliente WhatsApp.

        Parameters:
            app: Objeto representando a aplicação do WhatsApp.

        """
        super().__init__(*args, **kwargs)
        self._generate_identifier()
        self.started = False

    def _generate_identifier(self):
        """
        Gera um identificador único para a instância do cliente WhatsApp.

        """
        total_whats_app_clients = len(WhatsAppClient.identifiers.keys())
        self.identifier = total_whats_app_clients + 1
        WhatsAppClient.identifiers[self.identifier] = self

    def initialize(self):
        """
        Inicializa o cliente WhatsApp.

        Returns:
            bool: True se a inicialização foi bem-sucedida, False caso contrário.

        """
        if not self.started:
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
