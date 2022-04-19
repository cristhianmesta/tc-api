from Infraestructura.Data.sqlserver import SqlServer

CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=CM3-THINKPAD;DATABASE=TIPO_CAMBIO;Trusted_Connection=yes"

def getExchangeRateByDay(day):
    db = SqlServer(CONNECTION_STRING)
    query = "SELECT * FROM TIPO_CAMBIO_KAMBISTA WHERE FORMAT(Fecha, 'yyyy-MM-dd') = ?"
    params = (day, )
    return db.select(query, params)

def getExchangeRateGreaterThan(moment):
    db = SqlServer(CONNECTION_STRING)
    query = "SELECT * FROM TIPO_CAMBIO_KAMBISTA WHERE Fecha > CONVERT(datetime,?) AND FORMAT(Fecha, 'yyyy-MM-dd') = FORMAT(CONVERT(datetime,?), 'yyyy-MM-dd')"
    params = (moment, moment)
    return db.select(query, params)

def getExchangeRateByMonth(month, year):
    db = SqlServer(CONNECTION_STRING)
    query = "SELECT [Fecha],[Compra],[Venta] FROM [dbo].[TIPO_CAMBIO_KAMBISTA] WHERE month(Fecha)=? AND year(Fecha)=?"
    params = (month, year)
    return db.select(query, params)
    