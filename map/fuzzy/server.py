from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/fuzzy')
def fuzzy_get():
    'here we will get the json object from file'


