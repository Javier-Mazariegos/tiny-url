from flask import Flask, url_for, request,redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import time
import os
from redisworks import Root
import ast

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
#REDIS_HOST = os.getenv("REDIS_HOST", None)
#cache = redis.Redis(host=REDIS_HOST, port=6379)

conn = redis.StrictRedis('localhost', port=6379, charset="utf-8", decode_responses=True)

#con esta funcion se sobreescribe
#hola1 = "URL"
#hola2 = "www.google.com"
#conn.hset("diccionario1","1", "{'URL': 'yahoo', 'visitas': '10'}") #---este es para escribir uno nuevo


#dic = eval(conn.hget("diccionario1", "1")) ------
#dic["visitas"] = "0"                       --------- Todo esto es para editar las visitas o un url
#conn.hset("diccionario1","1", str(dic))    ------


#conn.hdel("diccionario1","1[visitas]") ----- Este es para borrar un registro

#conn.flushall() ----Este es para borrar todas las keys

#print(conn.hgetall("diccionario1")) ----------- este es para obtener todo el diccionario

#print(conn.hkeys("diccionario1"))  ------------ este es para obtener todas las llaves

#print(conn.hvals("diccionario1"))   ------------ este es para obtener todos los valores

#print(conn.hlen("diccionario1"))    ----------- obtenemos cuantos elementos hay en el diccionario

#print(conn.hexists("diccionario1", "1"))  ------ retorna un true o false si la llave existe o no

#if(len(diccionarioURL) == 0):
#    diccionarioURL = {}

#conn.flushall()
bandera = 0
app = Flask(__name__)


def existe(custom):
    global bandera
    bandera = -1
    if(conn.hlen("diccionarioURLS") != 0):
        for key,value in conn.hgetall("diccionarioURLS").items():
            if key == custom or custom == "crear" or custom == "urls" or custom == "stats":
                bandera = 1
                break
    return bandera

"""
def contar(customid):
    vistas = 0
    for k,v in diccionarioURL.items():
        if customid == k:
            vistas = v["visitas"]
            vistas = int(vistas) + 1
            v["visitas"] = vistas
"""


@app.route('/')
def tiny():
    template = env.get_template("index.html")
    customidNuevo = request.args.get('custom')
    return template.render(ultimakey = customidNuevo, banderaExito = bandera)


@app.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        url = request.form['url']
        customid = request.form['customid']
        if "/" not in customid and existe(customid) == -1:
            conn.hset("diccionarioURLS", customid , "{'URL': '"+url+"', 'visitas': '0'}")
        return redirect(url_for('tiny',custom = customid), 301)


@app.route('/urls')
def urls():
    template = env.get_template('list.html')
    nDiccionario = {}
    for key,value in conn.hgetall("diccionarioURLS").items():
        nuevoURl = eval(value)
        nDiccionario[key] = nuevoURl["URL"]
    print(nDiccionario)
    return template.render(diccionario = nDiccionario)


@app.route('/eliminar', methods=['POST'])
def eliminar():
    if request.method == 'POST':
        customid = request.form['customid']
        conn.hdel("diccionarioURLS",customid)
        return redirect(url_for('urls'), 301)


"""
#Crear Stats
@app.route('/stats')
def stats():
    template = env.get_template('stats.html')
    return template.render(diccionario = diccionarioURL)

@app.route('/<name>')   
def ejemplo(name):
    contar(name)
    return redirect(url_for('stats'), 301)

"""

if __name__ == "__main__":
    app.run()