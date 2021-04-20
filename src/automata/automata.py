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

                print(stack)
                
            
            elif state == "p":
                stack.insert(0, {
                    "tipo": "no terminal",
                    "valor": grammar.io
                })

                state = "q"
                print(stack)

            elif state == "q":
                for produccion in grammar.producciones:
                    actual_stack_top = stack[0]
                    #print (actual_stack_top)
                    #print(produccion)
                    if actual_stack_top["tipo"] == "no terminal" and actual_stack_top["valor"] == produccion["name"]:
                        if len(produccion["rules"]) == 1:
                            stack.pop(0)

                            for o in reversed(range(len(produccion["rules"][0]))):
                                stack.insert(0, produccion["rules"][0][o])

                            print(stack)
                            
                            
                        else:
                            rule = {}
                            current_char = string[i]
                            for current_rule in produccion["rules"]:
                                if current_rule[0]["valor"] == current_char:
                                    rule = current_rule
                                
                            if rule == {}:
                                #print("INTERNAL ---------")
                                #print(current_char)
                                #print(produccion)
                                for int_rule in produccion["rules"]:
                                    if int_rule[0]["valor"] in grammar.nterminales:
                                        for int_prod in grammar.producciones:
                                            if int_prod["name"] == int_rule[0]["valor"]:
                                                for rule_searched in int_prod["rules"]:
                                                    if rule_searched[0]["valor"] == current_char:
                                                        rule = [{
                                                            "tipo":"no terminal",
                                                            "valor": int_rule[0]["valor"]
                                                        }]

                                #for internal_prod in grammar.producciones:
                                    
                                #print("-----------")

                            stack.pop(0)

                            for o in reversed(range(len(rule))):
                                stack.insert(0, rule[o])

                            print(stack)

                    elif actual_stack_top["tipo"] == "terminal" and actual_stack_top["valor"] == string[i]:
                        i += 1
                        stack.pop(0)
                        print(stack)

                    elif actual_stack_top["tipo"] == "terminal" and actual_stack_top["valor"] != string[i]:
                        print("error")
                        return
                    elif actual_stack_top["tipo"] == "no terminal" and actual_stack_top["valor"] == "#":
                        stack.pop(0)
                        state = "f"
                        print(state)


            elif state == "f":
                print("Estado f")

