from . import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    ci = db.Column(db.String(30), unique=True, nullable=False)


    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
