from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.admin_model import Administrador
from models import db
import hashlib

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def requiere_superadmin():
    return 'rol' in session and session.get('rol') == 'superadmin'

@admin_bp.route('/listado')
def listado():
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    admins = Administrador.query.order_by(Administrador.id_admin.asc()).all()
    return render_template('admin/listado.html', admins=admins)

@admin_bp.route('/nuevo')
def nuevo():
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    return render_template('admin/nuevo.html')

@admin_bp.route('/guardar', methods=['POST'])
def guardar():
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    nombre = request.form.get('nombre','').strip()
    apellido_paterno = request.form.get('apellido_paterno','').strip()
    apellido_materno = request.form.get('apellido_materno','').strip()
    usuario = request.form.get('usuario','').strip()
    password = request.form.get('password','')
    rol = request.form.get('rol','admin')
    if not all([nombre, apellido_paterno, apellido_materno, usuario, password]):
        flash('Todos los campos son obligatorios')
        return redirect(url_for('admin.nuevo'))
    if Administrador.query.filter_by(usuario=usuario).first():
        flash('El usuario ya existe')
        return redirect(url_for('admin.nuevo'))
    admin = Administrador(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        usuario=usuario,
        password_hash=hashlib.sha256(password.encode()).hexdigest(),
        rol=rol,
        estado='activo'
    )
    db.session.add(admin)
    db.session.commit()
    flash('Administrador creado')
    return redirect(url_for('admin.listado'))

@admin_bp.route('/cambiar_estado/<int:id_admin>')
def cambiar_estado(id_admin):
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    admin = Administrador.query.get_or_404(id_admin)
    admin.estado = 'inactivo' if admin.estado == 'activo' else 'activo'
    db.session.commit()
    return redirect(url_for('admin.listado'))

@admin_bp.route('/editar/<int:id_admin>', methods=['GET','POST'])
def editar(id_admin):
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    admin = Administrador.query.get_or_404(id_admin)
    if request.method == 'POST':
        admin.nombre = request.form.get('nombre','').strip()
        admin.apellido_paterno = request.form.get('apellido_paterno','').strip()
        admin.apellido_materno = request.form.get('apellido_materno','').strip()
        admin.usuario = request.form.get('usuario','').strip()
        admin.rol = request.form.get('rol','admin')
        password = request.form.get('password','')
        if password:
            admin.password_hash = hashlib.sha256(password.encode()).hexdigest()
        db.session.commit()
        flash('Administrador actualizado')
        return redirect(url_for('admin.listado'))
    return render_template('admin/editar.html', admin=admin)

@admin_bp.route('/eliminar/<int:id_admin>')
def eliminar(id_admin):
    if not requiere_superadmin():
        return redirect(url_for('auth.login'))
    admin = Administrador.query.get_or_404(id_admin)
    db.session.delete(admin)
    db.session.commit()
    flash('Administrador eliminado')
    return redirect(url_for('admin.listado'))
