from flask import Flask, url_for, request,redirect
from jinja2 import Template, Environment, FileSystemLoader
import redis
import time
import os

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
REDIS_HOST = os.getenv("REDIS_HOST", None)
cache = redis.Redis(host=REDIS_HOST, port=6379)

app = Flask(__name__)

#Tiny Urls
@app.route('/')
def tiny():
    template = env.get_template("index.html")

    return template.render()

#Url List
#@app.route('/urls')
#def urls():
    #template = env.get_template('index.html')
    #return template.render(my_data=my_json['data'], headers=my_json['headers'], image_file= image_file)


#Crear Stats
#@app.route('/stats')
#def stats():
    #template = env.get_template('index.html')
    #return template.render(my_data=my_json['data'], headers=my_json['headers'], image_file= image_file)


if __name__ == "__main__":
    app.run(host="localhost", debug=True)