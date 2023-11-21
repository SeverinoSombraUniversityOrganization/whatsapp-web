import os

# Configuração para execução da aplicação Flask
APP_RUN_CONFIG = {
    'host': os.getenv('APP_HOST', '0.0.0.0'),  # Obtém o endereço do host da aplicação a partir das variáveis de ambiente ou usa '0.0.0.0' como padrão
    'port': int(os.getenv('APP_PORT', 5000)),    # Obtém a porta da aplicação a partir das variáveis de ambiente ou usa 5000 como padrão
    'debug': True,                              # Ativa o modo de depuração para facilitar o desenvolvimento (pode ser desativado em produção)
}
