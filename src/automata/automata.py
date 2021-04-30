from src.proyecto_singleton import *
from graphviz import Digraph
from common.helper import *
import time

class Automata:

    forze_error = False

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
                
                stack_top = stack[0]
                current_char = string[i]

                if current_char not in grammar.terminales:
                    self.forze_error = True

                if self.forze_error == True:
                    # Caracter no permitido
                    self.run_realtime(menu_option, stack_to_print, grammar, "Caracter no permitido: " + current_char)
                    return

                elif stack_top["tipo"] == "terminal" and stack_top["valor"] == current_char:
                    stack.pop(0)

                    stack_top = stack[0]
                    print(stack)
                    if stack_top["tipo"] == "no terminal" and stack_top["valor"] == "#":
                        state = "f" # Me aceptaron
                        stack_to_print.append({
                            "pila":stack.copy(),
                            "entrada": "λ",
                            "estado":state
                        })
                    else:
                        i += 1
                        temp = i
                        if i >= input_length:
                            temp -= 1

                        stack_to_print.append({
                            "pila":stack.copy(),
                            "entrada": string[temp],
                            "estado":state
                        })

                        if i >= input_length:
                            # Cadena incompleta, se esperaban más caracteres
                            self.run_realtime(menu_option, stack_to_print, grammar, "Cadena incompleta, se esperaban más caracteres")
                
                elif stack_top["tipo"] == "terminal" and stack_top["valor"] != current_char:
                    # Cadena inválida, caracter no esperado
                    self.run_realtime(menu_option, stack_to_print, grammar, "Cadena inválida, caracter no esperado: " + current_char)
                    return

                elif stack_top["tipo"] == "no terminal":
                    self.terminal_search(grammar.producciones, stack_top.copy(), stack, stack_to_print, string, i, [], state, menu_option)
                    continue
                    

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
                # Cadena aceptada
                self.run_realtime(menu_option, stack_to_print, grammar, "Cadena aceptada")
                return
    
    def terminal_search(self, producciones, stack_top, stack, stack_to_print, string, position, next_rules, state, menu_option):
        grammar = ProyectoSingleton().selected_grammar
        entrada = string[position]

        for produccion in producciones:
            if stack_top["valor"] == produccion["name"]:

                rules = []

                # Check ambiguity
                for rule in produccion["rules"]:
                    if rule[0]["tipo"] == "terminal" and rule[0]["valor"] == entrada:
                        rules.append(rule)
                    elif rule[0]["tipo"] == "no terminal":
                        rules.append(rule)
                
                rule_length = len(rules)

                for pos in range(rule_length):

                    rule = rules[pos]

                    if rule[0]["tipo"] == "no terminal":
                        #print(rule)
                        if next_rules == []:
                            next_rules = rule

                        if pos == rule_length and next_rules == []:
                            # Caracter no esperado
                            self.run_realtime(menu_option, stack_to_print, grammar, "Caracter no esperado: " + entrada)
                            self.forze_error = True
                            return

                        self.terminal_search(producciones, rule[0], stack, stack_to_print, string, position, next_rules, state, menu_option)

                    elif rule[0]["tipo"] == "terminal" and rule[0]["valor"] == entrada:

                        ambiguity_rules = []
                        for internal_rule in rules:
                            if internal_rule[0]["valor"] == entrada:
                                ambiguity_rules.append(internal_rule)

                        if len(ambiguity_rules) > 1:
                            # AMBIGUEDAD
                            if position == len(string) - 1: # Cadena terminada
                                for ambiguity_rule in ambiguity_rules:
                                    if len(ambiguity_rule) == 1:
                                        rule = ambiguity_rule
                            else:
                                next_character = string[position + 1]
                                rule = []
                                for ambiguity_rule in ambiguity_rules:

                                    if len(ambiguity_rule) > 1:
                                        if ambiguity_rule[1]["tipo"] == "terminal" and ambiguity_rule[1]["valor"] == next_character:
                                            rule = ambiguity_rule
                                            break
                                        else:
                                            for int_prod in producciones:
                                                if int_prod["name"] == ambiguity_rule[1]["valor"]:
                                                    for int_rule in int_prod["rules"]:
                                                        if int_rule[0]["valor"] == next_character:
                                                            rule = ambiguity_rule

                                    if len(ambiguity_rule) == 1 and rule == []:
                                        rule = ambiguity_rule

                        if next_rules == []:
                            next_rules = rule

                        stack.pop(0)
                        for o in reversed(range(len(next_rules))):
                            stack.insert(0, next_rules[o])

                        stack_to_print.append({
                            "pila":stack.copy(),
                            "entrada":entrada,
                            "estado":state
                        })

                        print(stack)
                        return

                    elif rule[0]["tipo"] == "terminal" and rule[0]["valor"] != entrada and pos == rule_length and next_rules != []:
                        print(stack) # Cadena invalida, caracter no esperado
                        self.forze_error = True
                        return

    def run_realtime(self, menu_option, stack_to_print, grammar, reason):
        print(reason)
        if menu_option == 4:
            self.build_automata_running(stack_to_print, grammar)
        else:
            Helper().build_table(stack_to_print, grammar)
                    