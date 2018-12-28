import os
from flask import Flask, jsonify, request, json, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename


from controlador.copiapp_controlador import ControladorCopiapp
from controlador.sede_controlador import ControladorSede
from controlador.factura_controlador import ControladorFactura

FILE_PATH = os.path.abspath(__file__)
UPLOAD_FOLDER = os.path.dirname(FILE_PATH)+'/temp'
# UPLOAD_FOLDER = realpath(__file__)
ALLOWED_EXTENSIONS = set(['txt', 'dat'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# file=open('pla_remi.dat')
# objfile = Archivo(file)
# return jsonify(objfile.fileToarray())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/copiupload', methods=['POST'])
def uploadfile():
    
    if 'file' in request.files:
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileupath = app.config['UPLOAD_FOLDER']+"/"+filename
            
            fileu = open(fileupath)
            datfact = [
                '',
                request.form['codigocom'],
                request.form['sede'],
                request.form['nombre'],
                '',
                request.form['fecha']
            ]
            respuesta = {}
            controlador = ControladorCopiapp(fileu)
            controlador.setData()
            res = controlador.insertarData(datfact)
            # return jsonify(res)
            if res == 1062:
                respuesta['estado'] = 'error'
                respuesta['contenido'] = 'Archivo ya subido a la base de datos'
                return jsonify(respuesta)
            if res == True:
                respuesta['estado'] = 'ok'
                respuesta['contenido'] = controlador.getData()
                return jsonify(respuesta)
            else:
                return jsonify(res)
    else:
        return 'Error'


@app.route('/documento', methods=['GET', 'POST'])
def documento():
    if request.method == 'GET':

        factura = request.args.get('factura')
        if factura is None:
            factura = 'funciona'

        controlador = ControladorCopiapp()

        return jsonify(controlador.getDocument(factura))

    if request.method == 'POST':
        datos = request.form
        return jsonify(datos)

@app.route('/facturas', methods=['GET', 'POST'])
def facturas():
    if request.method == 'GET':

        fecha = request.args.get('fecha')
        if fecha is None:
            fecha = 'funciona'

        controlador = ControladorFactura()
        res=controlador.getFacturas(fecha)
        return jsonify(res)
        # return jsonify(controlador.getDocument(factura))

    if request.method == 'POST':
        datos = request.form
        return jsonify(datos)

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':

        factura = request.args.get('factura')
        if factura is None:
            factura = 'funciona'
        
        respuesta = {}
        controlador = ControladorFactura()
        res = controlador.setItems(factura)
        if res:
            respuesta['estado'] = 'ok'
            respuesta['contenido'] = controlador.getData()
            return jsonify(respuesta)

    if request.method == 'POST':
        datos = request.form
        return jsonify(datos)


# sanity check route
@app.route('/ping', methods=['GET', 'POST'])
def ping_pong():
    if request.method == 'GET':

        dato = request.args.get('dato')
        if dato is None:
            dato = 'funciona'
        return jsonify(dato)

    if request.method == 'POST':
        datos = request.form
        return jsonify(datos)


@app.route('/puntosv', methods=['GET', 'POST'])
def puntos():
    if request.method == 'GET':
        controlador = ControladorSede()
        res = controlador.getSedes()
        return jsonify(res)
    if request.method == 'POST':
        datos = request.form
        return jsonify(datos)


if __name__ == '__main__':
    app.run()
