from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()

class Estacionamientos(db.Model):
    __tablename__='estacionamientos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True)
    direccion = db.Column(db.String(60))
    telefono = db.Column(db.String(20))
    capacidad = db.Column(db.String(20))
    entradas = db.relationship('Entradas')

class User(db.Model):
    __tablename__='usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username
        self.password = self.__create_password(password)

    def __create_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

class Entradas(db.Model):
    __tablename__='entradas'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True)
    estacionamiento = db.Column(db.String(20), db.ForeignKey('estacionamientos.nombre'))
    hora_entrada = db.Column(db.String(30))
    fecha_entrada = db.Column(db.String(30))
    registro = db.relationship('Registros')

class Registros(db.Model):
    __tablename__='registros'
    id = db.Column(db.Integer, primary_key=True)
    registro_matricula = db.Column(db.String(20), db.ForeignKey('entradas.matricula'))
    fecha_salida = db.Column(db.String(30))
    hora_salida = db.Column(db.String(30))
    total = db.Column(db.String(20))
