# Import Library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# Inisialisasi object
app = Flask(__name__)

# inisialisasi object flask restfull
api = Api(app)

# inisialisasi object flask cors
CORS(app)

# inisialisasi variabel kosong bertipe dictionary
identitas = {}


# Membuat class Resource
class ContohResource(Resource):
    # Metode get dan post
    def get(self):
        # response = {"msg" : "Hello World, ini app restful pertama"}
        return identitas

    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"msg" : "Data berhasi dimasukkan"}
        return response;

# Setup resource
api.add_resource(ContohResource, "/", methods=["GET", "POST"])

app.run(debug=True, port=5005)

