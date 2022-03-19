import pyodbc

class SqlServer:

    def __init__(self, cnn_str):
        self.connection = pyodbc.connect(cnn_str)
        self.cursor = self.connection.cursor()

    def select(self, str_sql, params):
        try:
            self.cursor.execute(str_sql, params) 
            rows = self.cursor.fetchall() 
            return rows
        except Exception as e:
            print("Ocurrió un error al insertar: ", e)
        finally:
            self.connection.close()