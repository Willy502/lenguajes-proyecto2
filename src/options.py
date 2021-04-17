import tkinter as tk
from tkinter import filedialog as fd
from .proyecto_singleton import *

class Options:

    def load_file(self):
        root = tk.Tk()
        root.withdraw()
        file = fd.askopenfilename(title='Open files', filetypes=[('text files', '*.glc')])

        if file != "":
            ProyectoSingleton().file = file
            print("El archivo se ha cargado exitosamente\n")

        else:
            print("No se ha seleccionado ningun archivo\n")
        
    def read_file(self):
        print("Read")

    def show_gram_info(self):
        print("Show")