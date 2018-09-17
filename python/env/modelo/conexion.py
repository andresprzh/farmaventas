from flask import Flask
# from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__)


class Conexion:

    def __init__(self):

        # self.mysql = MySQL()
        # app.config['MYSQL_DATABASE_USER'] = 'root'
        # app.config['MYSQL_DATABASE_PASSWORD'] = ''
        # app.config['MYSQL_DATABASE_DB'] = 'farmacompras'
        # app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        # self.mysql.init_app(app)
        # self.conn = self.mysql.connect()
        # self.cursor = self.conn.cursor()
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='farmacompras',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def buscarItem(self, tabla,valor=None,item=None):
        if(valor==None):
            self.cursor.execute("SELECT * from %s" % tabla)
            return self.cursor.fetchall()
        else:
            # sql="SELECT * from %s WHERE %s = '%s'" % (tabla,valor,item)
            # return sql
            self.cursor.execute("SELECT * from %s WHERE %s = '%s'" % (tabla,valor,item))
            return self.cursor.fetchall()
        
