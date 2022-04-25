# Import Library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# Inisialisasi object
app = Flask(__name__)

# inisialisasi object flask restfull
api = Api(app)

# inisialisasi object flask cors
CORS(app)

# Inisiallisasi SQLAlchemy
db = SQLAlchemy(app)

# konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# Membuat database model
class ModelDatabase(db.Model):
    # Membuat Field/Kolom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT) # Field Tambahan

    # Membuat method untuk menyimpan data agar lebih simpel
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# Create Database
db.create_all()

# inisialisasi variabel kosong bertipe dictionary
identitas = {}


# Membuat class Resource
class ContohResource(Resource):
    # Metode get dan post
    def get(self):
        
        # Menampilkan data dari database sqlite
        query = ModelDatabase.query.all()
        output = [
            {
                "nama":data.nama, 
                "umur":data.umur, 
                "alamat":data.alamat
            } 
            for data in query]

        response = {
            "code":200,
            "msd":"query data sukses",
            "data":output
        }
        return response, 200

    def post(self):
        data_nama = request.form["nama"]
        data_umur = request.form["umur"]
        data_alamat = request.form["alamat"]
        
        # Masukkan data ke dalam database model
        model = ModelDatabase(nama=data_nama, umur=data_umur, alamat=data_alamat)
        model.save()

        response = {
            "msg" : "Data berhasi dimasukkan",
            "code" : 200
        }
        return response, 200

    def delete(self):
        query = ModelDatabase.query.all()
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg" : "data berhasil dihapus semua",
            "code" : 200
        }

        return response

# Membuat class baru untuk mengedit dan menghapus data
class UpdateResource(Resource):
    def put(self, id):
        # Konsumsi id untuk query model databasenya / pilih data berdasarkan id
        query = ModelDatabase.query.get(id)

        # Form untuk pengeditan data
        edit_nama = request.form["nama"]
        edit_umur = request.form["umur"]
        edit_alamat = request.form["alamat"]

        # replace nilai yang ada di setiap field/kolom
        query.nama = edit_nama
        query.umur = edit_umur
        query.alamat = edit_alamat

        db.session.commit()

        response = {
            "msg" : "edit data berhasil",
            "code" : 200
        }

        return response

    # delete by id
    def delete(self, id):
        query = ModelDatabase.query.get(id)

        db.session.delete(query)
        db.session.commit()

        response = {
            "msg":"data berhasil dihapus",
            "code":200
        }

        return response


# Setup resource
api.add_resource(ContohResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])

app.run(debug=True)

