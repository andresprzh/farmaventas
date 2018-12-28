from modelo.conexion import Conexion
import pymysql


class ModeloCopiapp(Conexion):

    def __init__(self):
        Conexion.__init__(self)

    def insertDataNE(self, data):

        cols = list(data[0].keys())

        sql = "INSERT INTO copid(%s) VALUES" % (",".join(cols))
        for row in data:
            values = "('%(cod_drog)s','%(fecha)s','%(factura)s','%(refcopi)s','%(descripcion)s',%(cantidad)d,%(costo_desc)d,%(costo_full)d,%(iva)f,%(descuento)f,'%(cod_barras)s','%(cod_fab)s',%(control_line)d,%(descuento_2)f,'%(unidad)s',%(algo1)d,%(algo2)d,%(estado)d)," % (
                row)
            sql += values

        sql = sql[:-1]+";"

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def insertarFact(self, data):

        sql = "INSERT INTO factura(num_factura,codcomp,sede,nombre,fecha,fecha_ingreso) VALUES('%s')" % (
            "','".join(data))

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            # self.conn.close()
            return True
        except pymysql.err.IntegrityError as e:
            return e.args[0]
            # return None

    def buscarItem(self, item):

        sql = """SELECT  ITEMS.ID_ITEM, ITEMS.ID_REFERENCIA,  ITEMS.DESCRIPCION, ITEMS.UNIMED_COM,ITEMS.FACTOR_COM, ITEMS.ULTIMO_COSTO_ED, COD_BARRAS.ID_CODBAR
            FROM COD_BARRAS INNER JOIN ITEMS ON ID_ITEM = ID_ITEMS
            WHERE( ID_REFERENCIA = '%s'
            OR COD_BARRAS.ID_CODBAR = '%s') LIMIT 1;""" % (tuple(item))
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return False

    def insertData(self, data):

        cols = list(data[0].keys())
        cols = cols[:-1]

        sql = "INSERT INTO citems(%s) VALUES" % (",".join(cols))
        for row in data:
            values = "('%(id_item)s','%(cod_barras)s','%(unidad)s',%(factor)d,'%(transaccion)f','%(precio_unidad)f','%(descuento1)f',%(descuento2)f,%(iva)f,'%(factura)s')," % (
                row)
            sql += values

        sql = sql[:-1]+";"

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except pymysql.err.IntegrityError as e:
            return e.args[1]

    def buscarDataFactura(self, factura):
        sql = """SELECT factura.num_factura, factura.nitcomp, factura.fecha, factura.codcomp, factura.sede,
        citems.cod_barras,citems.id_item, citems.factor, citems.unidad, citems.transaccion, citems.transaccion2, citems.precio_unidad, citems.descuento1, citems.descuento2, citems.iva, citems.motivo_compra
        FROM citems
        INNER JOIN factura ON factura.num_factura = citems.factura
        WHERE citems.factura = '%s'""" % (factura)

        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return False
