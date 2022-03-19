from flask import Flask, jsonify
from flask import url_for
from markupsafe import escape

from exchangeRate import getExchangeRateByDay

app = Flask(__name__)

@app.route("/")
def index():
    return "Bienvenido a TC-API"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/projects/')
def projects():
    return 'The project page --> RUTA: ' + url_for('hello', name='John Doe')

@app.route("/exchange-rate/<day>")
def exchangeRate(day):
    results = getExchangeRateByDay(day)
    results_dict = [{
        'fecha' : result[0],
        'pc'    : result[1],
        'pv'    : result[2],
    }for result in results]
    return jsonify(results_dict)




with app.test_request_context():
    print(url_for('index'))
    print(url_for('projects'))
    print(url_for('hello', name='John Doe'))