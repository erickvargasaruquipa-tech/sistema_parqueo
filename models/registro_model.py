from . import db
from datetime import datetime, timezone, timedelta
from .cliente_model import Cliente
from .vehiculo_model import Vehiculo

class Registro(db.Model):
    __tablename__ = 'registros'
    id_registro = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculos.id_vehiculo'), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)  # Se asignará en el controlador
    fecha_salida = db.Column(db.DateTime, nullable=True)

    tiempo_transcurrido = db.Column(db.String(50), nullable=True)  # NUEVA COLUMNA
    total_pagar = db.Column(db.Numeric(10,2), nullable=True)
    estado = db.Column(db.Enum('abierto', 'cerrado', name='estado_enum'), default='abierto')

    cliente = db.relationship('Cliente', backref=db.backref('registros', lazy=True))
    vehiculo = db.relationship('Vehiculo', backref=db.backref('registros', lazy=True))
