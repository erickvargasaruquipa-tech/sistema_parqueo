from . import db
from datetime import datetime
from .cliente_model import Cliente

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    id_vehiculo = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(20), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # se llenará desde tarifas
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    color = db.Column(db.String(50))
    foto = db.Column(db.String(255))
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    cliente = db.relationship('Cliente', backref=db.backref('vehiculos', lazy=True))
