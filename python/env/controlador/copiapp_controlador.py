from modelo.copiapp_modelo import ModeloCopiapp


class ControladorCopiapp:

    def __init__(self, file):
        self.file = file
        self.itemsne = []  # variable que almacena items no encontrados
        self.items = []  # variable que almacena los items encontrados
        # objeto del modelo que se comunica con la base de datos
        self.modelo = ModeloCopiapp()

    def setData(self):
        res = []
        # se convierte el archivo en un array
        data = self.file.readlines()
        # se recorre el array para cada linea
        for row in data:
             # convierte la linea en array separando los datos por ,
            fields = row.split(',')
            # se acomoda la fehca a un formato que detecte mysql
            fecha = fields[1]
            fecha = fecha[0:4]+'-'+fecha[4:6]+'-'+fecha[6:]
            item = [fields[3], fields[10]]
            res = self.modelo.buscarItem(item)

            # si no hay errores en la busqueda
            if res != False:

                # si se encuentran resultados se guarda en la tabla de items
                if len(res) > 0:

                    for row in res:
                        iditem = row[0]
                        des = row[2]
                        unidad = row[3]

                    self.items.append({
                        'estado': 'encontrado',
                        'id_item': str(iditem),
                        'unidad': str(unidad),
                        'transaccion': int(fields[5]),
                        'precio_unidad': int(fields[6]),
                        'descuento1': float(fields[9])/100,
                        'descuento2': float(fields[13])/100,
                        'iva': float(fields[8]),
                        'factura': (fields[2]).rstrip(),
                        'descripcion': des
                    })
                # si no se encuentra el iten en la base de datos se guerda en la tabla itemsn
                else:
                    self.itemsne.append({
                        'cod_drog': fields[0],
                        'fecha': fecha,
                        'factura': (fields[2]),  # se requiere en tabla factura
                        'refcopi': (fields[3]),  # prioridad busqueda 2
                        'descripcion': fields[4],
                        'cantidad': int(fields[5]),
                        'costo_desc': int(fields[6]),  # se requiere en vitem
                        'costo_full': int(fields[7]),  # se requiere en vitem
                        'iva': float(fields[8]),  # se requiere en vitem
                        'descuento': float(fields[9])/100,  # se requiere
                        'cod_barras': fields[10],  # prioridad busqueda 1
                        'cod_fab': fields[11],
                        'control_line': int(fields[12]),
                        'descuento_2': float(fields[13])/100,  # se requiere
                        'unidad': fields[14],  # se requiere en vitem
                        'algo1': int(fields[15]),
                        'algo2': int(fields[16])
                    })

        # return respuesta

    def insertarData(self, datfact):

        datfact[0] = self.items[0]['factura'].rstrip()

        if self.modelo.insertarFact(datfact):
            data = self.items

            res = (self.modelo.insertData(data))
        else:
            res = False

        # si hay items fuera de la base de datos los agrega en una tabla
        if res == True and len(self.itemsne):
            data = self.itemsne

            return (self.modelo.insertDataNE(data))
        else:
            return res

    def getData(self):
        return self.items
