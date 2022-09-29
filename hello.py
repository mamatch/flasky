from flask import Flask, request, make_response, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<string:name>')
def get_user(name):
    return render_template('user.html', name=name)
