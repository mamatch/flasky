from flask import Flask, request, make_response
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Hello</h1>'
    