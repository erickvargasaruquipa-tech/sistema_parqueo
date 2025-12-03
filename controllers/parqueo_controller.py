from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.parqueo_model import Parqueo
from models import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

parqueo_bp = Blueprint('parqueo', __name__, url_prefix='/administrador/parqueo')
UPLOAD_FOLDER = 'static/uploads/parqueos'

def requiere_admin():
    return 'rol' in session and session.get('rol') in ['superadmin', 'admin']

# --- LISTAR PARQUEOS ---
@parqueo_bp.route('/')
def index():
    if not requiere_admin():
        return redirect(url_for('auth.login'))
    parqueos = Parqueo.query.all()
    return render_template('administrador/parqueo.html', parqueos=parqueos)

# --- AGREGAR PARQUEO ---
@parqueo_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        direccion = request.form.get('direccion', '').strip()
        telefono = request.form.get('telefono', '').strip()
        horario_apertura = request.form.get('horario_apertura', '').strip()
        horario_cierre = request.form.get('horario_cierre', '').strip()
        capacidad_autos = request.form.get('capacidad_autos', '').strip()
        capacidad_motos = request.form.get('capacidad_motos', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        logo_file = request.files.get('logo')

        if not nombre or not direccion or not horario_apertura or not horario_cierre:
            flash('Por favor complete todos los campos obligatorios')
            return redirect(url_for('parqueo.agregar'))

        # Validaciones numéricas
        try:
            telefono = int(telefono) if telefono else None
            capacidad_autos = int(capacidad_autos)
            capacidad_motos = int(capacidad_motos)
        except ValueError:
            flash('Los campos de teléfono, capacidad de autos y motos deben ser números')
            return redirect(url_for('parqueo.agregar'))

        # Validar 8 dígitos máximo en teléfono
        if telefono and len(str(telefono)) > 8:
            flash('El teléfono no puede tener más de 8 dígitos')
            return redirect(url_for('parqueo.agregar'))

        # Convertir horarios a objeto time
        try:
            horario_apertura = datetime.strptime(horario_apertura, '%H:%M').time()
            horario_cierre = datetime.strptime(horario_cierre, '%H:%M').time()
        except ValueError:
            flash('Formato de horario incorrecto')
            return redirect(url_for('parqueo.agregar'))

        logo_path = None
        if logo_file and logo_file.filename != '':
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(logo_file.filename)
            logo_path = f"uploads/parqueos/{filename}"
            logo_file.save(os.path.join('static', 'uploads', 'parqueos', filename))

        parqueo = Parqueo(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            horario_apertura=horario_apertura,
            horario_cierre=horario_cierre,
            capacidad_autos=capacidad_autos,
            capacidad_motos=capacidad_motos,
            descripcion=descripcion,
            logo=logo_path
        )
        db.session.add(parqueo)
        db.session.commit()
        flash('Parqueo agregado correctamente')
        return redirect(url_for('parqueo.index'))

    return render_template('administrador/parqueo_form.html', accion="Agregar")

# --- EDITAR PARQUEO ---
@parqueo_bp.route('/editar/<int:id_parqueo>', methods=['GET', 'POST'])
def editar(id_parqueo):
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    parqueo = Parqueo.query.get_or_404(id_parqueo)

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        direccion = request.form.get('direccion', '').strip()
        telefono = request.form.get('telefono', '').strip()
        horario_apertura = request.form.get('horario_apertura', '').strip()
        horario_cierre = request.form.get('horario_cierre', '').strip()
        capacidad_autos = request.form.get('capacidad_autos', '').strip()
        capacidad_motos = request.form.get('capacidad_motos', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        logo_file = request.files.get('logo')

        if not nombre or not direccion or not horario_apertura or not horario_cierre:
            flash('Por favor complete todos los campos obligatorios')
            return redirect(url_for('parqueo.editar', id_parqueo=id_parqueo))

        try:
            telefono = int(telefono) if telefono else None
            capacidad_autos = int(capacidad_autos)
            capacidad_motos = int(capacidad_motos)
        except ValueError:
            flash('Los campos de teléfono, capacidad de autos y motos deben ser números')
            return redirect(url_for('parqueo.editar', id_parqueo=id_parqueo))

        if telefono and len(str(telefono)) > 8:
            flash('El teléfono no puede tener más de 8 dígitos')
            return redirect(url_for('parqueo.editar', id_parqueo=id_parqueo))

        try:
            horario_apertura = datetime.strptime(horario_apertura, '%H:%M').time()
            horario_cierre = datetime.strptime(horario_cierre, '%H:%M').time()
        except ValueError:
            flash('Formato de horario incorrecto')
            return redirect(url_for('parqueo.editar', id_parqueo=id_parqueo))

        parqueo.nombre = nombre
        parqueo.direccion = direccion
        parqueo.telefono = telefono
        parqueo.horario_apertura = horario_apertura
        parqueo.horario_cierre = horario_cierre
        parqueo.capacidad_autos = capacidad_autos
        parqueo.capacidad_motos = capacidad_motos
        parqueo.descripcion = descripcion

        if logo_file and logo_file.filename != '':
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(logo_file.filename)
            logo_path = f"uploads/parqueos/{filename}"
            logo_file.save(os.path.join('static', 'uploads', 'parqueos', filename))
            parqueo.logo = logo_path

        db.session.commit()
        flash('Parqueo actualizado correctamente')
        return redirect(url_for('parqueo.index'))

    return render_template('administrador/parqueo_form.html', parqueo=parqueo, accion="Editar")

# --- ELIMINAR PARQUEO ---
@parqueo_bp.route('/eliminar/<int:id_parqueo>')
def eliminar(id_parqueo):
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    parqueo = Parqueo.query.get_or_404(id_parqueo)
    db.session.delete(parqueo)
    db.session.commit()
    flash('Parqueo eliminado correctamente')
    return redirect(url_for('parqueo.index'))
