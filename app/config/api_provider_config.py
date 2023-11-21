import os

API_PROVIDER_CONFIG = {
    'host': os.getenv('API_PROVIDER_SERVICE'),
    'port': int(os.getenv('API_PROVIDER_PORT', 3000)),
}

API_PROVIDER_BASE_URL = f"http://{API_PROVIDER_CONFIG['host']}:{API_PROVIDER_CONFIG['port']}/api/"
