from modelo.conexion import Conexion


class ModeloPunto(Conexion):

    def __init__(self):
        Conexion.__init__(self)

    def mostrarSedes(self, tabla):
        res = self.buscarItem(tabla)
        return res
