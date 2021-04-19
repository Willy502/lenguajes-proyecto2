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