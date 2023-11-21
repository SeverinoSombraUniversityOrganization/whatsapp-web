class EventHub:
    """
    Classe que implementa um mecanismo simples de hub de eventos para gerenciar eventos e ouvintes.

    Atributos:
        _listeners (dict): Dicionário para armazenar eventos e seus respectivos ouvintes.

    Métodos:
        __init__(self): Método de inicialização da instância do hub de eventos.
        on(self, event, listener): Adiciona um ouvinte a um evento específico.
        emit(self, event, *args, **kwargs): Emite um evento chamando todos os ouvintes associados a esse evento.
        trigger_event(self, event, *args): Atalho para emitir um evento com argumentos.

    """

    def __init__(self):
        """
        Inicializa a instância do hub de eventos.

        """
        self._listeners = {}

    def on(self, event, listener):
        """
        Adiciona um ouvinte a um evento específico.

        Parameters:
            event (str): Nome do evento.
            listener (callable): Função ou método a ser chamado quando o evento é emitido.

        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)

    def emit(self, event, *args, **kwargs):
        """
        Emite um evento chamando todos os ouvintes associados a esse evento.

        Parameters:
            event (str): Nome do evento.
            *args: Argumentos posicionais a serem passados para os ouvintes.
            **kwargs: Argumentos de palavra-chave a serem passados para os ouvintes.

        """
        if event in self._listeners:
            for listener in self._listeners[event]:
                listener(*args, **kwargs)

    def trigger_event(self, event, *args):
        """
        Atalho para emitir um evento com argumentos.

        Parameters:
            event (str): Nome do evento.
            *args: Argumentos posicionais a serem passados para os ouvintes.

        """
        if event in self._listeners.keys():
            self.emit(event, *args)
