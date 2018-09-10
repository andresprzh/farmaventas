import os
from flask import Flask, jsonify, request, json, abort
from flask_cors import CORS
from werkzeug.utils import secure_filename

from controlador.copiapp_controlador import Copiapp

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


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/copiupload', methods=['POST'])
def uploadfile():
    if 'file' in request.files:
        file = request.files['file']

        # objfile = Archivo(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fileupath = app.config['UPLOAD_FOLDER']+"/"+filename
            fileu = open(fileupath)
            objfile = Copiapp(fileu)
            objfile.setData()
            res = objfile.insertarData()
            if res == True:
                return jsonify(objfile.getData())
            else:
                return jsonify(res)


if __name__ == '__main__':
    app.run()
