from modelo.conexion import Conexion


class ModeloCopiapp(Conexion):

    def __init__(self):
        Conexion.__init__(self)

    def insertData(self, data):

        cols = list(data[0].keys())
        # cols = list(data.keys())
        # vals = list(data.values())

        sql = "INSERT INTO copid(%s) VALUES" % (",".join(cols))
        # values = "('%(cod_drog)s','%(fecha)s','%(factura)s','%(refcopi)s','%(descripcion)s',%(cantidad)d,%(costo_desc)d,%(costo_full)d,%(iva)f,%(descuento)f,'%(cod_barras)s','%(cod_fab)s',%(control_line)d,%(descuento_2)f,'%(unidad)s',%(algo1)d,%(algo2)d)" % (data)
        for row in data:
            values = "('%(cod_drog)s','%(fecha)s','%(factura)s','%(refcopi)s','%(descripcion)s',%(cantidad)d,%(costo_desc)d,%(costo_full)d,%(iva)f,%(descuento)f,'%(cod_barras)s','%(cod_fab)s',%(control_line)d,%(descuento_2)f,'%(unidad)s',%(algo1)d,%(algo2)d)," % (
                row)
            sql += values

        sql = sql[:-1]+";"

        # values = "('%(cod_drog)s','%(fecha)s','%(factura)s','%(refcopi)s','%(descripcion)s',%(cantidad)d,%(costo_desc)d,%(costo_full)d,%(iva)f,%(descuento)f,'%(cod_barras)s','%(cod_fab)s',%(control_line)d,%(descuento_2)f,'%(unidad)s',%(algo1)d,%(algo2)d)"
        # sql += values

        # return sql
        # self.cursor.executemany(sql, vals)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def insertarFact(self, data):

        sql = "INSERT INTO factura(num_factura,nitcomp,codcomp,localizacion,fecha) VALUES('%s')" % (
            "','".join(data))
        # return sql
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False
