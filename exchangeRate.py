from Infraestructura.Data.sqlserver import SqlServer

def getExchangeRateByDay(day):
    db = SqlServer("DRIVER={ODBC Driver 17 for SQL Server};SERVER=CM3-THINKPAD;DATABASE=TIPO_CAMBIO;Trusted_Connection=yes")
    query = "SELECT * FROM TIPO_CAMBIO_KAMBISTA WHERE FORMAT(Fecha, 'yyyy-MM-dd') = ?"
    params = (day, )
    return db.select(query, params)