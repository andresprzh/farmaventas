from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)


class Conexion:

    def __init__(self):

        mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'root'
        app.config['MYSQL_DATABASE_PASSWORD'] = ''
        app.config['MYSQL_DATABASE_DB'] = 'farmaventas'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        mysql.init_app(app)
        self.conn = mysql.connect()
        self.cursor = self.conn.cursor()

    def buscarItem(self):
        self.cursor.execute("SELECT * from copi")
        return self.cursor.fetchone()
