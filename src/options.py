import tkinter as tk
from tkinter import filedialog as fd
from .proyecto_singleton import *
from .reader import *
from .main_menu import *

class Options:

    def load_file(self):
        root = tk.Tk()
        root.withdraw()
        file = fd.askopenfilename(title='Open files', filetypes=[('text files', '*.glc')])

        if file != "":
            ProyectoSingleton().file = file
            print("El archivo se ha cargado exitosamente\n")
            self.read_file()

        else:
            print("No se ha seleccionado ningun archivo\n")
        
    def read_file(self):
        Reader().read()

    def show_gram_info(self):
        print("---------------------------------")
        gramaticas = ProyectoSingleton().gramaticas
        for gramatica in gramaticas:
            print("Nombre de la gramática tipo 2 = " + gramatica.name)
            print("No terminales = { " + ', '.join([str(l) for l in gramatica.nterminales]) + " }")
            print("Terminales = { " + ', '.join([str(l) for l in gramatica.terminales]) + " }")
            print("No terminal inicial = " + gramatica.io)
            print("Producciones:")
            for produccion in gramatica.producciones:
                rules_print = ""
                
                i = 0
                for prods in produccion["rules"]:
                    if i > 0:
                        rules_print += "\n    |"
                    for p in prods:
                        rules_print += " " + p["valor"]
                    i += 1
                print(produccion["name"] + " -> " + rules_print)
            print("---------------------------------")
