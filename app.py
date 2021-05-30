#Archivo usado para crear una pagina con flask
#Se importa flask y librerias necesarias para renderizar la página
from flask import Flask, render_template, request, jsonify, make_response
#Se importa los archivos Memgraph y dboperationes
from graficoredsocial.database import Memgraph
from graficoredsocial import db_operations
#Se inicializa la funcionalidad de flask en la variable app
app = Flask(__name__)

#Se indica la ruta principal
@app.route('/')
#Se indica la ruta index y la funcionalidad que debe ejecutarse al accederse a la misma
#En este caso, cada que se refresca la página index la base de datos se limpia y repuebla con nueva data.
@app.route('/index')
def index():
    db = Memgraph()
    db_operations.clear(db)
    db_operations.populate_database(db, "resources/data_small.txt")
    return render_template('index.html')

#Método usado para renderizar el template asociado a la pagina del query
@app.route('/query')
def query():
    return render_template('query.html')

#Metodo encargado de responder peticiones post del cliente y retornar el grafo de información que se recupera.
@app.route("/get-graph", methods=["POST"])
def get_graph():
   db = Memgraph()
   response = make_response(
       jsonify(db_operations.get_graph(db)), 200)
   return response

#Metodo usado para renderizar la respuesta de obtener usuarios
@app.route('/get-users', methods=["POST"])
def get_users():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_users(db)), 200)
    return response

#Metodo asociado a la renderización del método obtener relaciones
@app.route('/get-relationships', methods=["POST"])
def get_relationships():
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_relationships(db)), 200)
    return response