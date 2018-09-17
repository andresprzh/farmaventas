from modelo.conexion import Conexion
import pymysql

class ModeloFactura(Conexion):

    def __init__(self):
        Conexion.__init__(self)
    
    def buscarItems(self,factura):
        self.cursor.close ()
        # vuelve a crea el curso para mostrar resultados com dictionarios
        self.cursor = self.conn.cursor (pymysql.cursors.DictCursor)
        try:
            self.cursor.execute("""SELECT citems.id_item,cod_barras,unidad,factor,transaccion,precio_unidad,
            descuento1,descuento2,iva,factura,descripcion
            FROM citems
            INNER JOIN ITEMS ON ITEMS.ID_ITEM=citems.id_item
            WHERE factura=%s""" % factura)
            res=self.cursor.fetchall()
            self.cursor.close ()
            return res
        except:
            self.cursor.close ()
            return False

        self.cursor.close ()
    
    def buscarItemsne(self,factura):
        self.cursor.close ()
        # vuelve a crea el curso para mostrar resultados com dictionarios
        self.cursor = self.conn.cursor (pymysql.cursors.DictCursor)
        try:
            res=self.buscarItem('copid','factura',factura)
            return res
        except:
            self.cursor.close ()
            return False

        self.cursor.close ()

    