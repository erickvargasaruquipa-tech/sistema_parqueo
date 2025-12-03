from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.admin_model import Administrador
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def login():
    if 'rol' in session:
        if session.get('rol') == 'superadmin':
            return redirect(url_for('admin.listado'))
        return redirect(url_for('administrador.inicio'))
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.form.get('usuario','').strip()
    password = request.form.get('password','')
    admin = Administrador.query.filter_by(usuario=usuario).first()
    if not admin:
        flash('Usuario no encontrado')
        return redirect(url_for('auth.login'))
    if admin.estado == 'inactivo':
        flash('Usuario desactivado, no puede ingresar')
        return redirect(url_for('auth.login'))
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != admin.password_hash:
        flash('Contraseña incorrecta')
        return redirect(url_for('auth.login'))
    session.clear()
    session['usuario'] = admin.usuario
    session['rol'] = admin.rol
    session['id_admin'] = admin.id_admin
    if admin.rol == 'superadmin':
        return redirect(url_for('admin.listado'))
    return redirect(url_for('administrador.inicio'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
