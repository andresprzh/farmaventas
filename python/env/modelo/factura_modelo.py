from modelo.conexion import Conexion
import pymysql

class ModeloFactura(Conexion):

    def __init__(self):
        Conexion.__init__(self)

    # def buscarFacturas(self,factura=None):
    #     busqueda=self.buscarItem()