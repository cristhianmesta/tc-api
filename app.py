from flask import Flask, jsonify, request
import datetime
import pandas as pd
import Utils.calendar as calendar

from Features.exchangeRate import getExchangeRateByDay, getExchangeRateByMonth, getExchangeRateGreaterThan
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

@app.route("/mins-by-month/<month>")
def minsByMonth(month):
    monthNumber, yearNumer = list(month.split("-"))
    daysNumber = calendar.numeberOfDays(int(monthNumber), int(yearNumer))
    results = getExchangeRateByMonth(monthNumber,yearNumer)
    month_dict = [{
        'day'   : int(result[0].strftime("%d")),
        'month' : int(result[0].strftime("%m")),
        'year'  : int(result[0].strftime("%Y")),
        'hour'  : int(result[0].strftime("%H")),
        'fecha' : result[0],
        'pc'    : result[1],
        'pv'    : result[2],
    }for result in results]
    data = pd.DataFrame(month_dict)

    json_result = []
    for day in range(1,daysNumber+1):
        if len(data[ (data["day"] == day) ]):
            month_dict = {
                'day_of_the_month': day,
            }
            for hour in range(8,19):
                dft = data[ (data["day"] == day) & (data["hour"] == hour) ]

                if len(dft)>0:
                    # items = dft[dft["pv"] == dft['pv'].min()].reset_index()
                    month_dict['at_' + str(hour)] = dft['pv'].min()
                    # for index, row in items.iterrows():
                    #     month_dict[str(hour)].append(dict(row))

            json_result.append(month_dict)

    return jsonify(json_result)

@app.route("/average-by-month/<month>")
def averageByMonth(month):
    results = getExchangeRateByMonth(month)
    if len(results) == 0:
        return jsonify([]);
    results_dict = [{
        'fecha' : result[0].strftime("%Y-%m-%d"),
        'pc'    : result[1],
        'pv'    : result[2],
    }for result in results]
    data = pd.DataFrame(results_dict)
    return (data.groupby(['fecha'], as_index=False).mean()
                .groupby('fecha')['pc','pv'].mean()).to_json()

# @app.route("/mins-by-month/<month>")
# def minsByMonth(month):
#     results = getExchangeRateByMonth(month)
#     if len(results) == 0:
#         return jsonify([]);
#     results_dict = [{
#         'fecha' : result[0],
#         'day'   : result[0].strftime('%Y-%m-%d'),
#         'pc'    : result[1],
#         'pv'    : result[2],
#     }for result in results]
#     data = pd.DataFrame(results_dict)
#     print(data.groupby(['day']))
#     return jsonify([])
