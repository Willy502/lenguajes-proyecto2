import tkinter as tk
from tkinter import filedialog as fd
from .proyecto_singleton import *
from .reader import *
from .main_menu import *
import os
from src.automata.automata import *

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
        i = 1
        for gramatica in gramaticas:
            print(str(i) + ". " + gramatica.name)
            i += 1
        print("---------------------------------")
        print("Seleccione una gramática > ", end="")
        answer = input()
        self.screen_clear()

        gramatica = gramaticas[int(answer) - 1]
        ProyectoSingleton().selected_grammar = gramatica

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

    def screen_clear(self):
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platfrom
            _ = os.system('cls')

    def generate_equivalent_automata(self):
        Automata().build_equivalent_automata()

    def run_report(self):
        print("Ingresa la cadena a evaluar > ", end="")
        answer = input()
        Automata().run_report(answer)
