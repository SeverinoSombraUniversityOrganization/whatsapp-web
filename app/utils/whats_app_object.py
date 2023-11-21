class WhatsAppObject:
    def __init__(self, **entries):
        self.index = None
        self.argument_configs = {}

        self.executed_methods = {}
        self.__dict__.update(entries)

    @staticmethod
    def js_objects_to_python_objects(js_objects_list, argument_configs):
        for i, js_object in enumerate(js_objects_list):
            if isinstance(js_object, dict):
                python_object = WhatsAppObject(**js_object)
                python_object.index = i
                python_object.argument_configs = argument_configs
                js_objects_list[i] = python_object
        return js_objects_list

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            if name not in self.executed_methods:
                self.executed_methods[name] = []

            self.executed_methods[name].append(args)

            if self.index not in self.argument_configs.keys():
                self.argument_configs[self.index] = {
                    'executedMethods': self.executed_methods
                }
        return wrapper

    def __str__(self):
        return str(self.index)