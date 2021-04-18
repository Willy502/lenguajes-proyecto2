class ProyectoSingleton(object):

    __instance = None
    file = None
    gramaticas = None
    selected_grammar = None

    def __new__(cls):
        if ProyectoSingleton.__instance is None:
            ProyectoSingleton.__instance = object.__new__(cls)
        return ProyectoSingleton.__instance