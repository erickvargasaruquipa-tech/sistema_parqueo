from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime, timezone, timedelta
from app import db
from models.registro_model import Registro

salida_bp = Blueprint('salida_controller', __name__, url_prefix='/salida')

# --- Función para hora en Bolivia ---
def hora_bolivia():
    return datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-4)))

@salida_bp.route('/buscar_salida', methods=['GET', 'POST'])
def buscar_salida():
    registro = None
    if request.method == 'POST':
        placa = request.form.get('placa')
        ci = request.form.get('ci')
        if not placa or not ci:
            flash("Debe ingresar placa y CI para buscar.", "danger")
            return redirect(url_for('salida_controller.buscar_salida'))

        registro = Registro.query.join(Registro.cliente).join(Registro.vehiculo).filter(
            Registro.fecha_salida == None,
            Registro.vehiculo.has(placa=placa),
            Registro.cliente.has(ci=ci)
        ).first()

        if not registro:
            flash('No se encontró ningún registro activo que coincida con PLACA + CI.', 'danger')
            return redirect(url_for('salida_controller.buscar_salida'))

    return render_template('salida/buscar_salida.html', registro=registro)


@salida_bp.route('/confirmar_salida/<int:registro_id>', methods=['POST'])
def confirmar_salida(registro_id):
    registro = Registro.query.get_or_404(registro_id)

    # Hora de salida Bolivia
    fecha_salida = hora_bolivia()
    registro.fecha_salida = fecha_salida

    # Asegurar que fecha_ingreso sea aware
    if registro.fecha_ingreso.tzinfo is None:
        registro.fecha_ingreso = registro.fecha_ingreso.replace(tzinfo=timezone(timedelta(hours=-4)))

    tiempo_transcurrido = registro.fecha_salida - registro.fecha_ingreso
    registro.tiempo_transcurrido = str(tiempo_transcurrido)

    # Tomar monto del formulario (editable)
    monto_form = request.form.get("monto", type=float)
    registro.total_pagar = monto_form if monto_form is not None else 0.0

    registro.estado = 'cerrado'
    db.session.commit()

    flash('Salida registrada correctamente.', 'success')
    return redirect(url_for('administrador.inicio'))
