# controllers/tarifas_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.tarifa_model import Tarifa, db

tarifas_bp = Blueprint('tarifas', __name__, url_prefix='/administrador/tarifas')

def requiere_admin():
    return 'rol' in session and session.get('rol') in ['superadmin', 'admin']

# --- LISTAR TARIFAS ---
@tarifas_bp.route('/')
def index():
    if not requiere_admin():
        return redirect(url_for('auth.login'))
    tarifas = Tarifa.query.all()
    return render_template('administrador/tarifas.html', tarifas=tarifas)

# --- AGREGAR TARIFA ---
@tarifas_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        precio_hora = request.form.get('precio_hora', '').strip()

        if not tipo_vehiculo or not precio_hora:
            flash('Por favor complete todos los campos')
            return redirect(url_for('tarifas.agregar'))

        try:
            precio_hora = float(precio_hora)
        except ValueError:
            flash('El precio debe ser un número')
            return redirect(url_for('tarifas.agregar'))

        tarifa = Tarifa(tipo_vehiculo=tipo_vehiculo, precio_hora=precio_hora)
        db.session.add(tarifa)
        db.session.commit()
        flash('Tarifa agregada correctamente')
        return redirect(url_for('tarifas.index'))

    return render_template('administrador/tarifa_form.html', accion="Agregar")

# --- EDITAR TARIFA ---
@tarifas_bp.route('/editar/<int:id_tarifa>', methods=['GET', 'POST'])
def editar(id_tarifa):
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    tarifa = Tarifa.query.get_or_404(id_tarifa)

    if request.method == 'POST':
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        precio_hora = request.form.get('precio_hora', '').strip()

        if not tipo_vehiculo or not precio_hora:
            flash('Por favor complete todos los campos')
            return redirect(url_for('tarifas.editar', id_tarifa=id_tarifa))

        try:
            precio_hora = float(precio_hora)
        except ValueError:
            flash('El precio debe ser un número')
            return redirect(url_for('tarifas.editar', id_tarifa=id_tarifa))

        tarifa.tipo_vehiculo = tipo_vehiculo
        tarifa.precio_hora = precio_hora
        db.session.commit()
        flash('Tarifa actualizada correctamente')
        return redirect(url_for('tarifas.index'))

    return render_template('administrador/tarifa_form.html', tarifa=tarifa, accion="Editar")

# --- ELIMINAR TARIFA ---
@tarifas_bp.route('/eliminar/<int:id_tarifa>')
def eliminar(id_tarifa):
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    tarifa = Tarifa.query.get_or_404(id_tarifa)
    db.session.delete(tarifa)
    db.session.commit()
    flash('Tarifa eliminada correctamente')
    return redirect(url_for('tarifas.index'))
