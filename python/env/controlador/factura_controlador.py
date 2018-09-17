from modelo.factura_modelo import ModeloFactura
from controlador.copiapp_controlador import ControladorCopiapp

class ControladorFactura(ControladorCopiapp):
    
    def __init__(self):
        ControladorCopiapp.__init__(self)
        self.facturas=[]
        self.modelo = ModeloFactura()

    def getFacturas(self,fecha):
        res=self.modelo.buscarItem('factura','fecha',fecha)
        return res

    def setItems(self,factura):
        self.factura=factura
        # busca los items encontrados
        items=self.modelo.buscarItems(factura)
        
        if items:
            self.items=items
            itemsne=self.modelo.buscarItemsne(factura)
        if itemsne:
            self.itemsne=itemsne
            return True
        else:
            return False
        


        
