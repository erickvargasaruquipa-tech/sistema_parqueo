from . import db

class Tarifa(db.Model):
    __tablename__ = 'tarifas'

    id_tarifa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_vehiculo = db.Column(db.String(50), nullable=False)
    precio_hora = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Tarifa {self.tipo_vehiculo}: {self.precio_hora}>"
