from ast import arg
from flask import Flask, jsonify, request, url_for
from markupsafe import escape
import datetime

from exchangeRate import getExchangeRateByDay, getExchangeRateGreaterThan

app = Flask(__name__)

@app.route("/")
def index():
    return "Bienvenido a TC-API"

@app.route("/exchange-rate/<day>")
def exchangeRate(day):
    results = getExchangeRateByDay(day)
    results_dict = [{
        'fecha' : result[1],
        'pc'    : result[2],
        'pv'    : result[3],
    }for result in results]
    return jsonify(results_dict)

@app.route("/exchange-rate/geather-than", methods=['GET'])
def exchangeRate_geatherThan():
    moment = request.args.get("moment")
    if(moment == '' or moment==None) : moment = datetime.datetime.now()

    try:
        results = getExchangeRateGreaterThan(moment)
        results_dict = [{
            'fecha' : result[1],
            'pc'    : result[2],
            'pv'    : result[3],
        }for result in results]
        return jsonify(results_dict)
    except ValueError:
        return "Se admiten solo fecha para el parámetro moment", 400
        

# @app.route('/projects/')
# def projects():
#     return 'The project page --> RUTA: ' + url_for('hello', name='John Doe')


# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('projects'))
#     print(url_for('hello', name='John Doe'))