from datetime import datetime
from models import db

class ListaNegra(db.Model):
    __tablename__ = 'lista_negra'

    id_lista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_vehiculo = db.Column(db.Integer, db.ForeignKey('vehiculos.id_vehiculo', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    estado = db.Column(db.Enum('activo', 'inactivo', name='estado_enum'), default='activo', nullable=False)
    registrado_por = db.Column(db.Integer, db.ForeignKey('administradores.id_admin', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    vehiculo = db.relationship('Vehiculo', backref='lista_negra')
    cliente = db.relationship('Cliente', backref='lista_negra')
