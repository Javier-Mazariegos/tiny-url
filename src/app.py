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

conn = redis.Redis('localhost', port=6379, charset="utf-8", decode_responses=True)
l = Root()
diccionarioURL = l.the.mapping.example
if(len(diccionarioURL) == 0):
    diccionarioURL = {}
bandera = 0
app = Flask(__name__)

def obtenerUrl():
    ultima = ""
    if bandera == -1:
        for key,value in diccionarioURL.items():
            ultima = key
    return ultima


def existe(custom):
    global bandera
    bandera = -1
    if(len(diccionarioURL) != 0):
        for key,value in diccionarioURL.items():
            if key == custom or key == "crear" or key == "urls" or key == "stats":
                bandera = 1
                break
    return bandera


#Tiny Urls
@app.route('/')
def tiny():
    template = env.get_template("index.html")
    ultima = obtenerUrl()
    return template.render(ultimakey = ultima, banderaExito = bandera)

@app.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        url = request.form['url']
        customid = request.form['customid']
        if "/" not in customid:
            if existe(customid) == -1:
                diccionarioURL[customid] = {"URL":url,"visitas": "0"}
                l.the.mapping.example = {customid: {"URL":url,"visitas": "0"}}
        return redirect(url_for('tiny'), 301)

#Url List
@app.route('/urls')
def urls():
    template = env.get_template('list.html')
    return template.render()


#Crear Stats
@app.route('/stats')
def stats():
    template = env.get_template('stats.html')
    return template.render()

if __name__ == "__main__":
    app.run()