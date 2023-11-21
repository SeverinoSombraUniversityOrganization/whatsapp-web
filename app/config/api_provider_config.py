import os

# Configuração do provedor de API para o serviço API Provider
API_PROVIDER_CONFIG = {
    'host': os.getenv('API_PROVIDER_SERVICE'),  # Obtém o endereço do host do serviço a partir das variáveis de ambiente
    'port': int(os.getenv('API_PROVIDER_PORT', 3000)),  # Obtém a porta do serviço a partir das variáveis de ambiente ou usa 3000 como padrão
}

# Construção da URL base para solicitações à API Provider
API_PROVIDER_BASE_URL = f"http://{API_PROVIDER_CONFIG['host']}:{API_PROVIDER_CONFIG['port']}/api/"
