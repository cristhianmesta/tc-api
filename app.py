from flask import Flask
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/projects/')
def projects():
    return 'The project page'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('projects'))
    print(url_for('hello', name='John Doe'))