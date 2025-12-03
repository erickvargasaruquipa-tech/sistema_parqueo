from flask import Blueprint, jsonify
from datetime import datetime, timezone, timedelta
from models.cliente_model import Cliente
from models.vehiculo_model import Vehiculo
from models.registro_model import Registro

ingreso_bp = Blueprint('ingreso_controller', __name__, url_prefix='/ingreso_controller')

# --- AUTOCOMPLETAR POR CI ---
@ingreso_bp.route('/autocompletar/ci/<ci>')
def autocompletar_ci(ci):
    cliente = Cliente.query.filter_by(ci=ci).first()
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    registro_activo = Registro.query.filter_by(id_cliente=cliente.id_cliente, estado='abierto').first()
    vehiculo = Vehiculo.query.filter_by(id_cliente=cliente.id_cliente).first()

    return jsonify({
        'cliente': {
            'nombre': cliente.nombre,
            'apellido_paterno': cliente.apellido_paterno,
            'apellido_materno': cliente.apellido_materno,
            'telefono': cliente.telefono,
            'ci': cliente.ci
        },
        'vehiculo': {
            'placa': vehiculo.placa if vehiculo else '',
            'tipo': vehiculo.tipo if vehiculo else '',
            'marca': vehiculo.marca if vehiculo else '',
            'modelo': vehiculo.modelo if vehiculo else '',
            'color': vehiculo.color if vehiculo else ''
        },
        'registro_activo': True if registro_activo else False
    })


# --- AUTOCOMPLETAR POR PLACA ---
@ingreso_bp.route('/autocompletar/placa/<placa>')
def autocompletar_placa(placa):
    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        return jsonify({'error': 'Vehículo no encontrado'}), 404

    cliente = Cliente.query.filter_by(id_cliente=vehiculo.id_cliente).first()
    registro_activo = Registro.query.filter_by(id_vehiculo=vehiculo.id_vehiculo, estado='abierto').first()

    return jsonify({
        'cliente': {
            'nombre': cliente.nombre if cliente else '',
            'apellido_paterno': cliente.apellido_paterno if cliente else '',
            'apellido_materno': cliente.apellido_materno if cliente else '',
            'telefono': cliente.telefono if cliente else '',
            'ci': cliente.ci if cliente else ''
        },
        'vehiculo': {
            'placa': vehiculo.placa,
            'tipo': vehiculo.tipo,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'color': vehiculo.color
        },
        'registro_activo': True if registro_activo else False
    })
