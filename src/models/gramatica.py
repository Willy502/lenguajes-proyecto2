class Gramatica:

    def __init__(self):
        self._name = None
        self._nterminales = None
        self._terminales = None
        self._io = None
        self._producciones = []

    @property
    def name(self):
        return self._name

    @property
    def nterminales(self):
        return self._nterminales

    @property
    def terminales(self):
        return self._terminales

    @property
    def io(self):
        return self._io

    @property
    def producciones(self):
        return self._producciones

    @name.setter
    def name(self, value):
        self._name = value

    @nterminales.setter
    def nterminales(self, value):
        self._nterminales = value

    @terminales.setter
    def terminales(self, value):
        self._terminales = value

    @io.setter
    def io(self, value):
        self._io = value

    @producciones.setter
    def producciones(self, value):
        self._producciones.append(value)