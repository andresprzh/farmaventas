from modelo.sedes_modelo import ModeloSede


class ControladorSede:

    def __init__(self):
        self.modelo = ModeloSede()

    def getSedes(self):
        tabla = 'sedes'
        busqueda = self.modelo.mostrarSedes(tabla)
        res = []
        for row in busqueda:
            res.append({
                "num_sede": row[0],
                "descripcion": row[1]
            })
        return res
