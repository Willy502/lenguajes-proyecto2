from src.models.gramatica import *
from .proyecto_singleton import *

class Reader:

    _is_valid_gram = False

    def read(self):
        with open(ProyectoSingleton().file, 'r') as file:
            data = file.readlines()

            arrayGramatica = []
            gramatica = Gramatica()
            line_of_gram = 1
            

            for line in data:
                
                if line_of_gram == 1: # Nombre de la gramatica
                    line_of_gram += 1
                    gramatica.name = line.strip()
                elif line_of_gram == 2: # Terminales, no terminales y punto inicial
                    gramatica.nterminales = line.split(";")[0].split(",")
                    gramatica.terminales = line.split(";")[1].split(",")
                    gramatica.io = line.split(";")[2].split(",")
                    line_of_gram += 1
                elif line.strip() == "*": # Cambio de gramatica
                    print(self._is_valid_gram)
                    if self._is_valid_gram:
                        arrayGramatica.append(gramatica)
                    gramatica = Gramatica()
                    line_of_gram = 1 
                    self._is_valid_gram = False
                else: # Producciones
                    self.buildProductions(gramatica, line)
            
            ProyectoSingleton().gramaticas = arrayGramatica

    def buildProductions(self, gramatica, line):
        productions = line.split("->")
        name = productions[0]
        production = productions[1].split(" ")

        productionsArray = []

        for prod in production:
            if prod.strip() in gramatica.nterminales:
                productionsArray.append({
                    "tipo": "no terminal",
                    "valor": prod.strip()
                })
                
            elif prod.strip() in gramatica.terminales:
                productionsArray.append({
                    "tipo": "terminal",
                    "valor": prod.strip()
                })

            if prod.strip() == name:
                self._is_valid_gram = True

        for grams in gramatica.producciones:
            if grams["name"] == name:
                grams["rules"].append(productionsArray)
                return

        gramatica.producciones = {
                    "name": name,
                    "rules": productionsArray
                }
