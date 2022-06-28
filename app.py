from flask import Flask, jsonify, request
from datetime import datetime
from pytz import timezone
import pandas as pd
import Utils.calendar as calendar

from Features.exchangeRate import getExchangeRateByDay, getExchangeRateByMonth, getExchangeRateGreaterThan
from flask_cors import CORS

SERVICES = ("KAMBISTA", "REXTIE", "TKAMBIO")
tz = timezone('US/Pacific')

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def index():
    return "Bienvenido a TC-API"

@app.route("/exchange-rate/<day>")
def exchangeRate(day):
    service = request.args.get('service') 
    
    if service == None :
        return "No existen valores para el servicio indicado", 400

    if not (service.upper() in str(SERVICES)):
        return "No existen valores para el servicio indicado", 400

    results = getExchangeRateByDay('TIPO_CAMBIO_'+service.upper(), day)
    results_dict = [{
        'fecha' : result[1].astimezone(tz),
        'pc'    : result[2],
        'pv'    : result[3],
    }for result in results]
            # 'fecha' : result[1].strftime("%Y-%m-%d %H:%M:%S.%f"),
    return jsonify(results_dict)

@app.route("/exchange-rate/geather-than", methods=['GET'])
def exchangeRate_geatherThan():
    service = request.args.get('service') 
    
    if service == None :
        return "No existen valores para el servicio indicado", 400

    if not (service.upper() in str(SERVICES)):
        return "No existen valores para el servicio indicado", 400

    moment = request.args.get("moment")
    if(moment == '' or moment==None) : moment = datetime.datetime.now()

    try:
        results = getExchangeRateGreaterThan('TIPO_CAMBIO_'+service.upper(),moment)
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
    service = request.args.get('service') 
    
    if service == None :
        return "No existen valores para el servicio indicado", 400

    if not (service.upper() in str(SERVICES)):
        return "No existen valores para el servicio indicado", 400

    monthNumber, yearNumer = list(month.split("-"))
    daysNumber = calendar.numeberOfDays(int(monthNumber), int(yearNumer))
    results = getExchangeRateByMonth('TIPO_CAMBIO_'+service.upper(),monthNumber,yearNumer)
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
