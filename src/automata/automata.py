from src.proyecto_singleton import *
from graphviz import Digraph

class Automata:

    def build_equivalent_automata(self):
        grammar = ProyectoSingleton().selected_grammar

        dot = Digraph(comment="AP_" + grammar.name, graph_attr={'rankdir':'LR'})
        dot.node("", "", color="white")
        dot.node("i", "i", shape='circle')
        dot.node("p", "p", shape='circle')
        dot.node("q", "q", shape='circle')
        dot.node("f", "f", shape='doublecircle')

        dot.edge("", "i")
        dot.edge("i", "p", label="λ,λ;#")
        dot.edge("p", "q", label="λ,λ;" + grammar.io)
        dot.edge("q", "f")

        dot.render('test-output/AP_' + grammar.name + '.gv', view=True)
        print("Autómata de pila equivalente generado exitósamente")

