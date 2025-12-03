from models import db

class Parqueo(db.Model):
    __tablename__ = 'parqueos'

    id_parqueo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.Integer)  # Solo números, max 8 dígitos
    horario_apertura = db.Column(db.Time, nullable=False)
    horario_cierre = db.Column(db.Time, nullable=False)
    capacidad_autos = db.Column(db.Integer, nullable=False)
    capacidad_motos = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text)
    logo = db.Column(db.String(255))  # Ruta relativa dentro de static

    def __repr__(self):
        return f"<Parqueo {self.nombre}>"
