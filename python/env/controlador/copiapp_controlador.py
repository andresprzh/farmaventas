from modelo.copiapp_modelo import ModeloCopiapp


class ControladorCopiapp:

    def __init__(self, file):
        self.file = file
        self.fecha = ''  # variable que almacena la fecha de copidrogas
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
            self.fecha = fecha  # se asigna la fecha a la variable de clase

            # busca si el item ya esta en la base de datos
            item = [fields[3].rstrip(), fields[10].rstrip()]
            res = self.modelo.buscarItem(item)

            # si no hay errores en la busqueda
            if res != False:
                # datos de items que presenten algun error
                datane = {
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
                    'algo2': int(fields[16]),
                    'estado': 0  # estado del item(0 si no se encuentra)
                }
                # si se encuentran resultados se guarda en la tabla de items
                if len(res) > 0:
                    # lista que guarda los codigos de barras de los items encontrados
                    cod_barras = []
                    # si el c
                    for rowr in res:
                        iditem = rowr[0]
                        des = rowr[2]
                        unidad = rowr[3]
                        cod_barras.append(rowr[6])
                        factor = float(rowr[4])
                        costo = float(rowr[5])
                    # acomoda la lista de codigos de barras como set para mejorar velocidad de busqueda
                    cod_barras = str(cod_barras)
                    # datos de items que no tienen errores
                    data = {
                        'id_item': str(iditem),
                        'unidad': str(unidad),
                        'factor': float(factor),
                        'transaccion': int(fields[5]),
                        'precio_unidad': int(fields[6]),
                        'descuento1': float(fields[9])/100,
                        'descuento2': float(fields[13])/100,
                        'iva': float(fields[8]),
                        'factura': (fields[2]).rstrip(),
                        'descripcion': des
                    }

                    # print(cod_barras)
                    # comprueba si el item tiene la misma referencia y codigo de barras
                    if str(rowr[1]) == str(item[0]) and (item[1] in cod_barras):

                       # si el costo de  copidrogras es igual al de la base de datos con un margen +- 50%
                        if ((costo*factor)*0.5 <= float(fields[7]) <= (costo*factor)*1.5):
                            if ((costo*factor)*0.15 <= float(fields[7]) <= (costo*factor)*1.15):
                                self.__setItem(data)
                            # si el costo del producto es mayor o menor en un 15 % al producto en la base de datos estado 4.
                            else:
                                datane['estado'] = 4
                                self.__setItemsne(datane)

                        # si el costo no corresponde al del factor se busca si coincide con el valor de unitario
                        elif (costo*0.5 <= float(fields[7]) <= costo*1.5):
                            data['unidad'] = 'UND'
                            if (costo*0.15 <= float(fields[7]) <= costo*1.15):
                                self.__setItem(data)
                            # si el costo del producto es mayor o menor en un 15 % al producto en la base de datos estado 4.
                            else:
                                datane['estado'] = 4
                                self.__setItemsne(datane)
                        # si el costo no se encuentra se agrega el item a no encontrados con un estado 3(Posible embalaje incorrecto o un cambio mayor al ±50 % del producto)
                        else:
                            datane['estado'] = 3
                            self.__setItemsne(datane)
                    else:

                        if str(rowr[1]) != str(item[0]):
                            estado = 1  # estado si la referencia no coincide
                        else:
                            estado = 2  # estado si el codigo de barras no coinciden
                        datane['estado'] = estado
                        # se inserta el item en la tabla de no encontrados con el estaod del error
                        self.__setItemsne(datane)
                # si no se encuentra el iten en la base de datos se guerda en la tabla itemsn
                else:
                    print(datane['descripcion']+" no encontrado")
                    self.__setItemsne(datane)

    def insertarData(self, datfact):

        # se asignan los dtaos faltantes de la factura
        datfact[0] = self.items[0]['factura'].rstrip()
        datfact[4] = self.fecha

        # si se logra crear la factura  se insertan los dato
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
        res = {
            'items': self.items,
            'itemsne': self.itemsne
        }
        return res

    def __setItem(self, data):

        self.items.append({
            'id_item': data['id_item'],
            'unidad': data['unidad'],
            'factor': data['factor'],
            'transaccion': data['transaccion'],
            'precio_unidad': data['precio_unidad'],
            'descuento1': data['descuento1'],
            'descuento2': data['descuento2'],
            'iva': data['iva'],
            'factura': data['factura'],
            'descripcion': data['descripcion']
        })

    def __setItemsne(self, data):
        self.itemsne.append({
            'cod_drog': data['cod_drog'],
            'fecha': data['fecha'],
            'factura': data['factura'],
            'refcopi': data['refcopi'],
            'descripcion': data['descripcion'],
            'cantidad': data['cantidad'],
            'costo_desc': data['costo_desc'],
            'costo_full': data['costo_full'],
            'iva': data['iva'],
            'descuento': data['descuento'],
            'cod_barras': data['cod_barras'],
            'cod_fab': data['cod_fab'],
            'control_line': data['control_line'],
            'descuento_2': data['descuento_2'],
            'unidad': data['unidad'],
            'algo1': data['algo1'],
            'algo2': data['algo2'],
            'estado': data['estado']
        })
