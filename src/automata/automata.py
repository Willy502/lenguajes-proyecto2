from src.proyecto_singleton import *
from graphviz import Digraph
from common.helper import *
import time

class Automata:

    def build_equivalent_automata(self):
        grammar = ProyectoSingleton().selected_grammar
        name_show = "AP_" + grammar.name
        dot = Digraph(comment=name_show, graph_attr={'rankdir':'LR', 'splines':'line'})
        dot.node("", "", color="white")
        dot.node("i", "i", shape='circle')
        dot.node("p", "p", shape='circle')
        dot.node("q", "q", shape='circle')
        dot.node("f", "f", shape='doublecircle')

        dot.edge("", "i")
        dot.edge("i", "p", label="λ,λ;#")
        dot.edge("p", "q", label="λ,λ;" + grammar.io)

        label = ""
        for produccion in grammar.producciones:
            rules = produccion["rules"]
            for rule in rules:
                label += "λ," + produccion["name"] + ";" + ''.join([str(val["valor"]) for val in rule]) + "\n"

        dot.edge("q:n", "q",label=label)

        label = ""
        for out in grammar.terminales:
            label += out + "," + out + ";λ\n"

        dot.edge("q:s", "q", label=label)
        
        dot.edge("q", "f", label="λ,#;λ")

        dot.render('test-output/AP_' + grammar.name + '.gv', view=False)
        file_name = dot.filepath + ".pdf"
        Helper().build_html(grammar ,name_show ,file_name, False, None)
        print("Autómata de pila equivalente generado exitósamente")

    def build_automata_running(self, data, gramatica):
        transiciones = Helper().build_transiciones(data, gramatica)
        label = ""
        contador = 0
        for transicion in transiciones:
            estado = ""
            if transicion != "(f)":
                estado = transicion[1]
                transicion = transicion[3:-1]
                transicion = transicion.split(";")[0] + ";" + transicion.split(";")[1][2:]
            else:
                estado = transicion[1]
                transicion = transicion[1:-1]
            
            color = []
            style = []
            if estado == "i":
                color = ["yellow", "black", "black", "black"]
                style = ["filled", "", "", ""]
            elif estado == "p":
                color = ["black", "yellow", "black", "black"]
                style = ["", "filled", "", ""]
            elif estado == "q":
                color = ["black", "black", "yellow", "black"]
                style = ["", "", "filled", ""]
            elif estado == "f":
                color = ["black", "black", "black", "yellow"]
                style = ["", "", "", "filled"]

            grammar = ProyectoSingleton().selected_grammar
            name_show = "AP_" + grammar.name + "_running"
            dot = Digraph(comment=name_show, graph_attr={'rankdir':'LR', 'splines':'line'})
            dot.node("", "", color="white")
            dot.node("i", "i", shape='circle', style=style[0], color=color[0])
            dot.node("p", "p", shape='circle', style=style[1], color=color[1])
            dot.node("q", "q", shape='circle', style=style[2], color=color[2])
            dot.node("f", "f", shape='doublecircle', style=style[3], color=color[3])

            dot.edge("", "i")
            label = "λ,λ;#"
            if label == transicion:
                label += " (RUNNING)"
            dot.edge("i", "p", label=label)

            label = "λ,λ;" + grammar.io
            if label == transicion:
                label += " (RUNNING)"
            dot.edge("p", "q", label=label)

            label = ""
            for produccion in grammar.producciones:
                rules = produccion["rules"]
                for rule in rules:
                    intern_label = "λ," + produccion["name"] + ";" + ''.join([str(val["valor"]) for val in rule])
                    if intern_label == transicion:
                        intern_label += " (RUNNING)"
                    label += intern_label + "\n"

            dot.edge("q:n", "q",label=label)

            label = ""
            for out in grammar.terminales:
                intern_label = out + "," + out + ";λ"
                if intern_label == transicion:
                    intern_label += " (RUNNING)"
                label += intern_label + "\n"

            dot.edge("q:s", "q", label=label)
            
            label = "λ,#;λ"
            if label == transicion:
                label += " (RUNNING)"
            dot.edge("q", "f", label=label)

            dot.render('test-output/AP_' + grammar.name + '_running.gv', view=False)
            file_name = dot.filepath + ".pdf"
            Helper().build_html(grammar ,name_show ,file_name, True, data[contador])
            time.sleep(1)
            contador += 1

    def run_report(self, string, menu_option):
        grammar = ProyectoSingleton().selected_grammar

        i = 0
        input_length = len(string)
        stack = []
        stack_to_print = []
        state = "i"

        stack_to_print.append({
            "pila":stack.copy(),
            "entrada":string[i],
            "estado":state
        })
        print(stack)
        while (i < input_length):

            if state == "i":
                state = "p"
                stack.insert(0, {
                    "tipo": "no terminal",
                    "valor": "#"
                })
                stack_to_print.append({
                    "pila":stack.copy(),
                    "entrada":string[i],
                    "estado":state
                })

                print(stack)
                
            
            elif state == "p":
                state = "q"
                stack.insert(0, {
                    "tipo": "no terminal",
                    "valor": grammar.io
                })
                stack_to_print.append({
                    "pila":stack.copy(),
                    "entrada":string[i],
                    "estado":state
                })

                print(stack)

            elif state == "q":
                print("estado q")


            elif state == "f":
                print(stack)
                stack_to_print.append({
                    "pila":[{
                    "tipo": "terminal",
                    "valor": "λ"
                }],
                    "entrada":"λ",
                    "estado":state
                })
                print("Cadena aceptada")
                if menu_option == 4:
                    self.build_automata_running(stack_to_print, grammar)
                else:
                    Helper().build_table(stack_to_print, grammar)
                return

