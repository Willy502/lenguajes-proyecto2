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
                label += "λ," + produccion["name"] + ";" + ','.join([str(val["valor"]) for val in rule]) + "\n"

        dot.edge("q:n", "q",label=label)

        label = ""
        for out in grammar.terminales:
            label += out + "," + out + ",λ\n"

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
                label += " RUNNING"
            dot.edge("i", "p", label=label)

            label = "λ,λ;" + grammar.io
            if label == transicion:
                label += " RUNNING"
            dot.edge("p", "q", label=label)

            label = ""
            for produccion in grammar.producciones:
                rules = produccion["rules"]
                for rule in rules:
                    intern_label = "λ," + produccion["name"] + ";" + ''.join([str(val["valor"]) for val in rule])
                    if intern_label == transicion:
                        intern_label += " RUNNING"
                    label += intern_label + "\n"

            dot.edge("q:n", "q",label=label)

            label = ""
            for out in grammar.terminales:
                intern_label = out + "," + out + ";λ"
                if intern_label == transicion:
                    intern_label += " RUNNING"
                label += intern_label + "\n"

            dot.edge("q:s", "q", label=label)
            
            label = "λ,#;λ"
            if label == transicion:
                label += " RUNNING"
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
                for produccion in grammar.producciones:
                    actual_stack_top = stack[0]
                    #print (actual_stack_top)
                    #print(produccion)
                    if actual_stack_top["tipo"] == "no terminal" and actual_stack_top["valor"] == produccion["name"]:
                        if len(produccion["rules"]) == 1:
                            stack.pop(0)

                            for o in reversed(range(len(produccion["rules"][0]))):
                                stack.insert(0, produccion["rules"][0][o])
                                stack_to_print.append({
                                    "pila":stack.copy(),
                                    "entrada":string[i],
                                    "estado":state
                                })

                            print(stack)
                            
                            
                        else:
                            rule = {}
                            current_char = string[i]
                            for current_rule in produccion["rules"]:
                                if current_rule[0]["valor"] == current_char:
                                    rule = current_rule
                                
                            if rule == {}:

                                for int_rule in produccion["rules"]:
                                    if int_rule[0]["valor"] in grammar.nterminales:
                                        for int_prod in grammar.producciones:
                                            if int_prod["name"] == int_rule[0]["valor"]:
                                                for rule_searched in int_prod["rules"]:
                                                    if rule_searched[0]["valor"] == current_char:
                                                        if len(rule_searched) > 1 and rule_searched[1]["tipo"] == "terminal": # Ambiguedad de un grado
                                                            if rule_searched[1]["valor"] == string[i+1]:
                                                                rule = [{
                                                                    "tipo":"no terminal",
                                                                    "valor": int_rule[0]["valor"]
                                                                }]
                                                        else:
                                                            rule = [{
                                                                "tipo":"no terminal",
                                                                "valor": int_rule[0]["valor"]
                                                            }]

                            stack.pop(0)

                            for o in reversed(range(len(rule))):
                                stack.insert(0, rule[o])
                            stack_to_print.append({
                                "pila":stack.copy(),
                                "entrada":current_char,
                                "estado":state
                            })

                            print(stack)

                    elif actual_stack_top["tipo"] == "terminal" and actual_stack_top["valor"] == string[i]:
                        i += 1
                        stack.pop(0)
                        stack_to_print.append({
                            "pila":stack.copy(),
                            "entrada":current_char,
                            "estado":state
                        })
                        print(stack)

                    elif actual_stack_top["tipo"] == "terminal" and actual_stack_top["valor"] != string[i]:
                        print("Cadena no aceptada, caracter no esperado: " + current_char)
                        return
                    elif actual_stack_top["tipo"] == "no terminal" and actual_stack_top["valor"] == "#":
                        stack.pop(0)
                        stack_to_print.pop()
                        stack_to_print.append({
                            "pila":[{
                            "tipo": "no terminal",
                            "valor": "#"
                        }],
                            "entrada":"λ",
                            "estado":state
                        })
                        state = "f"
                        i -= 1
                        break


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

