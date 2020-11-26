from flask import Flask, url_for, request,redirect, abort
from jinja2 import Template, Environment, FileSystemLoader
import redis
import time
import os
from redisworks import Root
import ast
import random, string # para hacer la funcion de un random id
from datetime import datetime #para la hora y fecha

environment="development"

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

bandera = 0
app = Flask(__name__)

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
  return ''.join(random.choice(chars) for _ in range(N)) #---------------para hacer un random id


def existe(custom):
    global bandera
    bandera = -1
    if(conn.hlen("diccionarioURLS") != 0):
        for key,value in conn.hgetall("diccionarioURLS").items():
            if key == custom or custom == "crear" or custom == "urls" or custom == "stats":
                bandera = 1
                break
    return bandera

def contar(customid):
    visitas = 0
    dic = {}
    for k,v in conn.hgetall("diccionarioURLS").items():
        if customid == k:
            dic = eval(conn.hget("diccionarioURLS", str(k)))
            visitas = int(dic["visitas"]) + 1 
            print(visitas)
            dic["visitas"] = str(visitas)
            print(dic["visitas"])
            conn.hset("diccionarioURLS", str(k), str(dic))

def urlOriginal(key):
    for k,v in conn.hgetall("diccionarioURLS").items():
        if key == k:
            nuevoURl = eval(v)
            print("=====================================================================")
            print(nuevoURl["URL"])
            return nuevoURl["URL"]

            

@app.route('/')
def tiny():
    randomid = randStr(chars='abcdefghijklmnopqrstuvwxyz0123456789',N=6)
    template = env.get_template("index.html")
    customidNuevo = request.args.get('custom')
    base_url = request.base_url
    print("==============", base_url)
    return template.render(ultimakey = customidNuevo, banderaExito = bandera, randomid = randomid, base_url=base_url )


@app.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        url = request.form['url']
        customid = request.form['customid']
        if "/" not in customid and existe(customid) == -1:
            now = datetime.now()
            current_time = now.strftime("%d-%b-%Y %H:%M:%S")
            print("Current Time =", current_time)
            conn.hset("diccionarioURLS", customid , "{'URL': '"+url+"', 'visitas': '0', 'hora':'"+current_time+"'}")
        return redirect(url_for('tiny',custom = customid), 301)

@app.route('/urls')
def urls():
    template = env.get_template('list.html')
    nDiccionario = {}
    for key,value in conn.hgetall("diccionarioURLS").items():
        nuevoURl = eval(value)
        nDiccionario[key] = nuevoURl["URL"]
        base_url = request.base_url
    return template.render(diccionario = nDiccionario,base_url=base_url)


@app.route('/eliminar', methods=['POST'])
def eliminar():
    if request.method == 'POST':
        customid = request.form['customid']
        conn.hdel("diccionarioURLS",customid)
        return redirect(url_for('urls'), 301)

#redirecccionar key
@app.route('/<tinykey>')
def redireccionar(tinykey):
    print ("----------------TinyKEY--------------",tinykey)
    data = conn.hget("diccionarioURLS",tinykey)
    if data :
        print (data)
        parsed_data = eval(data)
        contar(tinykey)
        return redirect(parsed_data["URL"], code=302)
    else :
        abort(404)

#Crear Stats
@app.route('/stats')
def stats():
    template = env.get_template('stats.html')
    nDiccionario = {}
    for key,value in conn.hgetall("diccionarioURLS").items():
        nuevoURl = eval(value)
        nDiccionario[key] = {"URL": nuevoURl["URL"], "visitas": nuevoURl["visitas"], "hora": nuevoURl["hora"]}
    return template.render(diccionario = nDiccionario)


@app.errorhandler(404)
def page_not_found(e):
    template = env.get_template('404.html')
    return template.render(), 404


if __name__ == "__main__":
    debug=False
    if environment == "development" or environment == "local":
        debug=True
    print("Local change")
    app.run(host="0.0.0.0")
