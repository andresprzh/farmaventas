from modelo.factura_modelo import ModeloFactura

class ControladorFactura:
    
    def __init__(self):
        self.facturas=[]
        self.modelo = ModeloFactura()

    def getFacturas(self,fecha):
        res=self.modelo.buscarItem('factura','fecha',fecha)
        return res