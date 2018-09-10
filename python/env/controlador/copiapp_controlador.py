from modelo.copiapp_modelo import mdlArchivo


class Copiapp:

    def __init__(self, file):
        self.file = file
        self.datos = []
        self.modelo = mdlArchivo()

    def setData(self):
        # se convierte el archivo en un array
        data = self.file.readlines()
        # se recorre el array para cada linea
        for row in data:
             # convierte la linea en array separando los datos por ,
            fields = row.split(',')
            # se acomoda la fehca a un formato que detecte mysql
            fecha = fields[1]
            fecha = fecha[0:4]+'-'+fecha[4:6]+'-'+fecha[6:]

            self.datos.append({
                'cod_drog': fields[0],
                'fecha': fecha,
                'factura': (fields[2]),
                'refcopi': (fields[3]),
                'descripcion': fields[4],
                'cantidad': int(fields[5]),
                'costo_desc': int(fields[6]),
                'costo_full': int(fields[7]),
                'iva': float(fields[8]),
                'descuento': float(fields[9])/100,
                'cod_barras': fields[10],
                'cod_fab': fields[11],
                'control_line': int(fields[12]),
                'descuento_2': float(fields[13]),
                'unidad': fields[14],
                'algo1': int(fields[15]),
                'algo2': int(fields[16])
            })

    def getData(self):
        return self.datos

    def insertarData(self):

        data = self.datos
        # return data
        return (self.modelo.insertData(data))
