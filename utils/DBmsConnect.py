import mysql.connector


class DBmsConnect:

    def __init__(self):
        self.dbms = mysql.connector.connect(
            host='localhost',
            user='root',
            password='12345678',
            database='game_zone'
        )

