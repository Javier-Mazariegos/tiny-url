from flask import Flask, url_for, request,redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import time
import os
from redisworks import Root

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
#REDIS_HOST = os.getenv("REDIS_HOST", None)
#cache = redis.Redis(host=REDIS_HOST, port=6379)

conn = redis.Redis('localhost', port=6379, charset="utf-8", decode_responses=True)
l = Root()
diccionarioURL = dict(l.something)


app = Flask(__name__)


def existe(custom): 
    bandera = -1
    for key,value in diccionarioURL.items():
        if key == custom:
            bandera = 1
            break
    return bandera
#Tiny Urls
@app.route('/')
def tiny():
    template = env.get_template("index.html")
    return template.render(diccionario = diccionarioURL)

@app.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        url = request.form['url']
        customid = request.form['customid']
        if existe(customid) == -1:
            diccionario2 = {customid:{"URL":url,"visitas": "0"}}
            diccionarioURL.update(diccionario2)
            return redirect(url_for('tiny', 201))
        else:
            return redirect(url_for('tiny', 400))

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
    app.run(debug=True)