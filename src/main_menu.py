import time
from .options import *
from .proyecto_singleton import *

class MainMenu:

    def __init__(self):
        self.show_data()

    def show_data(self):
        print("Lenguajes formales y de programación A+")
        print("Wilfred Alejandro Barrios Ola")
        print("201602734")
        self.counter_back()

    def counter_back(self):
        i = 5
        while i > 0:
            print(i)
            i -= 1
            time.sleep(1)
        print("Bienvenido")
        self.show_menu()

    def show_menu(self):
        print("")
        print("1. Cargar archivo")
        print("2. Mostrar información general de la gramática")
        print("3. Generar autómata de pila equivalente")
        print("4. Reporte de recorrido")
        print("5. Reporte en tabla")
        print("6. Salir")
        print("> ", end='')
        answer = input()
        self.select_menu_option(answer)

    def select_menu_option(self, option):

        if option not in ["1", "2", "3", "4", "5", "6"]:
            print("Seleccione una opción válida")
            self.show_menu()
            return
        
        if option in ["2", "3", "4", "5"] and ProyectoSingleton().file is None:
            print("No ha cargado un archivo de gramáticas")
            self.show_menu()
            return

        if option == "1":
            Options().load_file()
        elif option == "2":
            Options().show_gram_info()
        elif option == "3":
            Options().generate_equivalent_automata()
        elif option == "4":
            print(option)
        elif option == "5":
            print(option)
        elif option == "6":
            quit()
        self.show_menu()