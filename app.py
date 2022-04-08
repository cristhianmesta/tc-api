from flask import Flask, jsonify, request
import datetime

from Features.exchangeRate import getExchangeRateByDay, getExchangeRateGreaterThan
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def index():
    return "Bienvenido a TC-API"

@app.route("/exchange-rate/<day>")
def exchangeRate(day):
    results = getExchangeRateByDay(day)
    results_dict = [{
        'fecha' : result[1].strftime("%Y-%m-%d %H:%M:%S.%f"),
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
            'fecha' : result[1].strftime("%Y-%m-%d %H:%M:%S.%f"),
            'pc'    : result[2],
            'pv'    : result[3],
        }for result in results]
        return jsonify(results_dict)
    except ValueError:
        return "Se admiten solo fecha para el parámetro moment", 400
        