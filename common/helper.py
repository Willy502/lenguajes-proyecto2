import webbrowser
import os

class Helper:

    def build_html(self, gramatica, name, pdf):

        info1 = "Terminales = { " + ','.join([str(l) for l in gramatica.terminales]) + " }\n"
        info2 = "Alfabeto de la pila = { " + ','.join([str(l) for l in gramatica.terminales]) + "," + ','.join([str(l) for l in gramatica.nterminales]) + ",# }\n"
        info3 = "Estados = { i,p,q,f }\n"
        info4 = "Estado Inicial = { i }\n"
        info5 = "Estado de aceptación = { f }\n"

        html = '''<!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
                <title>''' + name + '''</title>
                <style>
                    .bg-c {
                        background-color: #fff;
                    }
                    body {
                        background-color: #303E73;
                    }
                    html, body {
                        height: 100%;
                    }
                    h1, p {
                        color: #fff;
                    }
                </style>
            </head>
            <body>
            <br />
            <h1>Nombre: ''' + name + '''</h1>
            <hr />
                <div class="container">
                    <div class="row">
                        <div class="col-8 offset-2">
                            <embed class="col-12" type="application/pdf" src="''' + pdf + '''" height="500px">
                        </div>
                        <div class="col-8 offset-2">
                            <p>''' + info1 + '''</p>
                            <p>''' + info2 + '''</p>
                            <p>''' + info3 + '''</p>
                            <p>''' + info4 + '''</p>
                            <p>''' + info5 + '''</p>
                        </div>
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
            </body>
            </html>'''

        file = open(name + '.html', 'w')
        file.write(html)
        file.close()
        filename = 'file://' + os.path.realpath(file.name)
        webbrowser.open_new_tab(filename)

    def build_transiciones(self, data, gramatica):
        transiciones = []
        for i in range(len(data)):
            # del estado
            build_string = "("
            build_string += data[i]["estado"]
            if build_string != "(f":

                # Lee
                lee = ""
                if len(data[i]["pila"]) > 0 and data[i]["pila"][0]["tipo"] == "terminal":
                    lee = data[i]["pila"][0]["valor"]
                    build_string += "," + lee
                else:
                    lee = "λ"
                    build_string += "," + lee
                
                # Saca
                if len(data[i]["pila"]) > 0 and i != 1:
                    build_string += "," + data[i]["pila"][0]["valor"]
                else:
                    build_string += ",λ"

                # al estado
                build_string += ";" + data[i + 1]["estado"]

                # Ingresa
                previous_stack = "".join([printed["valor"] for printed in reversed(data[i - 1]["pila"])])
                actual_stack = "".join([printed["valor"] for printed in reversed(data[i]["pila"])])
                next_stack = "".join([production_part["valor"] for production_part in reversed(data[i + 1]["pila"])])

                if actual_stack == next_stack:
                    build_string += ",λ"
                else:
                    insert = ""
                    if len(actual_stack) == len(next_stack):
                        for o in range(len(actual_stack)):
                            if actual_stack[o] != next_stack[o]:
                                insert += next_stack[o]
                        build_string += "," + insert
                    elif len(actual_stack) > len(next_stack):
                        build_string += ",λ"
                    elif len(actual_stack) < len(next_stack):
                        insert += ","
                        for o in range(len(actual_stack)):
                            if actual_stack[o] != next_stack[o]:
                                insert += next_stack[o]
                        
                        for o in range(len(actual_stack), len(next_stack)):
                            insert += next_stack[o]
                        build_string += insert


            build_string += ")"
            transiciones.append(build_string)
        
        return transiciones

    def build_table(self, data, gramatica):
        lines = ''
        contador = 0
        transiciones = self.build_transiciones(data, gramatica)
        for item in data:
            #print(item)
            lines += "<tr>\n"
            lines += "<th scope='row'>" + str(contador) + "</th>\n"
            build_pila = ""
            for pila in item["pila"]:
                build_pila += pila["valor"]
            lines += "<td scope='col'>" + build_pila + "</td>\n"
            lines += "<td scope='col'>" + str(item["entrada"]) + "</td>\n"
            transicion = transiciones[contador]
            lines += "<td scope='col'>" + transicion + "</td>\n"
            lines += "</tr>\n"
            contador += 1
            

        html = '''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">

            <title>Reporte de tabla</title>
        </head>
        <body>

            <div class="container">
                <div class="row">
                    <br>
                    <br>
                    <h1>Reporte de tabla</h1>
                    <hr>
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">Iteración</th>
                            <th scope="col">Pila</th>
                            <th scope="col">Entrada</th>
                            <th scope="col">Transiciones</th>
                            </tr>
                        </thead>
                        <tbody>'''
        html += lines
        html += '''
                        </tbody>
                    </table>
                </div>
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>

        </body>
        </html>
        '''
        file = open('tabla.html', 'w')
        file.write(html)
        file.close()
        filename = 'file://' + os.path.realpath(file.name)
        webbrowser.open_new_tab(filename)