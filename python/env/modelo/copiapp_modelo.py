from modelo.conexion import Conexion


class ModeloCopiapp(Conexion):

    def __init__(self):
        Conexion.__init__(self)

    def insertDataNE(self, data):

        cols = list(data[0].keys())

        sql = "INSERT INTO copid(%s) VALUES" % (",".join(cols))
        for row in data:
            values = "('%(cod_drog)s','%(fecha)s','%(factura)s','%(refcopi)s','%(descripcion)s',%(cantidad)d,%(costo_desc)d,%(costo_full)d,%(iva)f,%(descuento)f,'%(cod_barras)s','%(cod_fab)s',%(control_line)d,%(descuento_2)f,'%(unidad)s',%(algo1)d,%(algo2)d)," % (
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

        sql = "INSERT INTO factura(num_factura,codcomp,sede,nombre,fecha,fecha_ingreso) VALUES('%s');" % (
            "','".join(data))

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def buscarItem(self, item):

        sql = """SELECT ITEMS.ID_ITEM, ITEMS.ID_REFERENCIA,  ITEMS.DESCRIPCION, ITEMS.UNIMED_EMPAQ, ITEMS.UNIMED_INV_1,
            ITEMS.FACTOR_EMPAQ, ITEMS.IMPUESTO, ITEMS.ULTIMO_COSTO_ED, MIN(COD_BARRAS.ID_CODBAR) AS ID_CODBAR
            FROM COD_BARRAS INNER JOIN ITEMS ON ID_ITEM = ID_ITEMS
            WHERE( ID_REFERENCIA = '%s'
            OR COD_BARRAS.ID_CODBAR = '%s')
            GROUP BY ITEMS.ID_ITEM, ITEMS.ID_REFERENCIA, ITEMS.DESCRIPCION, ITEMS.UNIMED_EMPAQ,
            ITEMS.UNIMED_INV_1, ITEMS.FACTOR_EMPAQ, ITEMS.IMPUESTO, ITEMS.ULTIMO_COSTO_ED;""" % (tuple(item))
        
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return False

    def insertData(self, data):

        cols = list(data[0].keys())
        cols = cols[1:-1]

        sql = "INSERT INTO citems(%s) VALUES" % (",".join(cols))
        for row in data:
            values = "('%(id_item)s','%(unidad)s',%(factor)d,'%(transaccion)f','%(precio_unidad)f','%(descuento1)f',%(descuento2)f,%(iva)f,'%(factura)s')," % (
                row)
            sql += values

        sql = sql[:-1]+";"
        
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False
