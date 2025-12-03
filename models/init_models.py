from .admin_model import Administrador
from . import db
import hashlib

def create_superusuario():
    if not Administrador.query.filter_by(usuario='maruja').first():
        admin = Administrador(
            nombre='Maruja',
            apellido_paterno='Vino',
            apellido_materno='de Challco',
            usuario='maruja',
            password_hash=hashlib.sha256('maru445v'.encode()).hexdigest(),
            rol='superadmin',
            estado='activo'
        )
        db.session.add(admin)
        db.session.commit()
        print("Superusuario creado")
