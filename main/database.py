import mysql.connector


class DataBase:
    def __init__(self, host, database, user, password):
        self.connection = None
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        self.connection = mysql.connector.connect(host=self.host,
                                                  database=self.database,
                                                  user=self.user,
                                                  password=self.password,
                                                  auth_plugin='mysql_native_password')

    def request(self, request, commit=False, fetchall=False):
        if not self.connection.is_connected():
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(request)
        if commit:
            self.connection.commit()
        if fetchall:
            rows = cursor.fetchall()
            if rows:
                return rows[0][0]
            else:
                return None
        cursor.close()
