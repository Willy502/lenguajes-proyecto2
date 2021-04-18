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
        print("Show")