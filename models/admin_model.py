from . import db
from datetime import datetime

class Administrador(db.Model):
    __tablename__ = 'administradores'
    id_admin = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default='admin')
    estado = db.Column(db.String(20), default='activo')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
