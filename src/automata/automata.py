from src.proyecto_singleton import *
from graphviz import Digraph
from common.helper import *

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
                label += "λ," + produccion["name"] + ";" + ','.join([str(val["valor"]) for val in rule]) + "\n"

        dot.edge("q:n", "q",label=label)

        label = ""
        for out in grammar.terminales:
            label += out + "," + out + ",λ\n"

        dot.edge("q:s", "q", label=label)
        
        dot.edge("q", "f", label="λ,#;λ")

        dot.render('test-output/AP_' + grammar.name + '.gv', view=False)
        file_name = dot.filepath + ".pdf"
        Helper().build_html(grammar ,name_show ,file_name)
        print("Autómata de pila equivalente generado exitósamente")

    def run_report(self, string):
        grammar = ProyectoSingleton().selected_grammar

        i = 0
        input_length = len(string)
        stack = []
        state = "i"

        while (i < input_length):

            if state == "i":
                stack.insert(0, {
                    "tipo": "no terminal",
                    "valor": "#"
                })

                state = "p"
                
            
            elif state == "p":
                stack.insert(0, {
                    "tipo": "no terminal",
                    "valor": grammar.io
                })

                state = "q"

            elif state == "q":
                print("Estado q")
                print(stack)
                return

            elif state == "f":
                print("Estado f")

