#!/bin/bash
#Instrucciones usadas para indicarle a docker como debe correr la página de flask
#Indica como ejecutar la app
export FLASK_APP=app.py
#Está opción le indica a flask que se ejecute en modo desarrollo
export FLASK_ENV=development
flask run --host 0.0.0.0