#Archivo usado para crear una pagina con flask
#Se importa flask
from flask import Flask
#Se inicializa la funcionalidad de flask en la variable app
app = Flask(__name__)

#Se indica la ruta principal
@app.route('/')
#Se indica la ruta index y la funcionalidad que debe ejecutarse al accederse a la misma
@app.route('/index')
def index():
    return "Hola mundo"