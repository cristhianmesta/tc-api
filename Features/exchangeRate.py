from Infraestructura.Data.sqlserver import SqlServer

CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=CM3-THINKPAD;DATABASE=TIPO_CAMBIO;Trusted_Connection=yes"

def getExchangeRateByDay(table, day):
    db = SqlServer(CONNECTION_STRING)
    query = ("SELECT * FROM {t} WHERE FORMAT(Fecha, 'yyyy-MM-dd') = ?").format(t = table)
    params = (day,)
    return db.select(query, params)

def getExchangeRateGreaterThan(table,moment):
    db = SqlServer(CONNECTION_STRING)
    query = ("SELECT * FROM {t} WHERE Fecha > CONVERT(datetime,?) AND FORMAT(Fecha, 'yyyy-MM-dd') = FORMAT(CONVERT(datetime,?), 'yyyy-MM-dd')").format(t = table)
    params = (moment, moment)
    return db.select(query, params)

def getExchangeRateByMonth(table, month, year):
    db = SqlServer(CONNECTION_STRING)
    query = ("SELECT [Fecha],[Compra],[Venta] FROM {t} WHERE month(Fecha)=? AND year(Fecha)=?").format(t = table)
    params = (month, year)
    return db.select(query, params)
    