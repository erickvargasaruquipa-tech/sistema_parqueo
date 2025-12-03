from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.cliente_model import Cliente
from models.vehiculo_model import Vehiculo
from models.registro_model import Registro
from models.tarifa_model import Tarifa
from models.parqueo_model import Parqueo
from models import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timezone, timedelta

administrador_bp = Blueprint('administrador', __name__, url_prefix='/administrador')
UPLOAD_FOLDER = 'static/uploads/vehiculos'

def requiere_admin():
    return 'rol' in session and session.get('rol') in ['superadmin', 'admin']

# --- DASHBOARD / INICIO ---
@administrador_bp.route('/inicio')
def inicio():
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    fecha = request.args.get('fecha', datetime.utcnow().date().strftime("%Y-%m-%d"))
    filtro = request.args.get('filtro', 'activos')
    busqueda = request.args.get('busqueda', '').strip()

    registros_query = Registro.query.join(Vehiculo).join(Cliente).filter(
        db.func.date(Registro.fecha_ingreso) == fecha
    )
    if filtro == 'activos':
        registros_query = registros_query.filter(Registro.estado=='abierto')
    elif filtro == 'salidos':
        registros_query = registros_query.filter(Registro.estado=='cerrado')

    if busqueda:
        registros_query = registros_query.filter(
            db.or_(
                Vehiculo.placa.ilike(f"%{busqueda}%"),
                Cliente.ci.ilike(f"%{busqueda}%")
            )
        )

    registros = registros_query.order_by(Registro.fecha_ingreso.desc()).all()

    parqueo = Parqueo.query.first()
    if parqueo:
        autos_ocupados = sum(1 for r in Registro.query.filter(Registro.estado=='abierto').all() if r.vehiculo.tipo.lower()=='auto')
        motos_ocupadas = sum(1 for r in Registro.query.filter(Registro.estado=='abierto').all() if r.vehiculo.tipo.lower()=='moto')
        capacidad = {
            'autos': parqueo.capacidad_autos - autos_ocupados,
            'motos': parqueo.capacidad_motos - motos_ocupadas
        }
    else:
        capacidad = {'autos': 0, 'motos': 0}

    return render_template('administrador/inicio.html',
                           registros=registros,
                           fecha=fecha,
                           filtro=filtro,
                           busqueda=busqueda,
                           capacidad=capacidad)

# --- INGRESO ---
@administrador_bp.route('/ingreso')
def ingreso():
    if not requiere_admin():
        return redirect(url_for('auth.login'))
    
    tipos_disponibles = [t.tipo_vehiculo for t in Tarifa.query.distinct(Tarifa.tipo_vehiculo).all()]
    
    return render_template('administrador/ingreso.html', tipos=tipos_disponibles)

# --- GUARDAR INGRESO ---
@administrador_bp.route('/guardar_ingreso', methods=['POST'])
def guardar_ingreso():
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    ci = request.form.get('ci','').strip()
    nombre = request.form.get('nombre','').strip()
    apellido_paterno = request.form.get('apellido_paterno','').strip()
    apellido_materno = request.form.get('apellido_materno','').strip()
    telefono = request.form.get('telefono','').strip()

    if telefono and (not telefono.isdigit() or len(telefono)>8):
        flash("El teléfono debe ser numérico y máximo 8 dígitos")
        return redirect(url_for('administrador.ingreso'))

    cliente = Cliente.query.filter_by(ci=ci).first()
    if not cliente:
        cliente = Cliente(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefono=telefono,
            ci=ci
        )
        db.session.add(cliente)
        db.session.commit()

    placa = request.form.get('placa','').strip()
    tipo = request.form.get('tipo')
    marca = request.form.get('marca','').strip()
    modelo = request.form.get('modelo','').strip()
    color = request.form.get('color','').strip()
    foto = request.files.get('foto')

    vehiculo = Vehiculo.query.filter_by(placa=placa).first()
    if not vehiculo:
        vehiculo = Vehiculo(
            placa=placa,
            tipo=tipo,
            marca=marca,
            modelo=modelo,
            color=color,
            id_cliente=cliente.id_cliente
        )
        if foto and foto.filename != '':
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(foto.filename)
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            foto.save(ruta)
            vehiculo.foto = ruta
        db.session.add(vehiculo)
        db.session.commit()
    else:
        if not vehiculo.marca: vehiculo.marca = marca
        if not vehiculo.modelo: vehiculo.modelo = modelo
        if not vehiculo.color: vehiculo.color = color
        if foto and foto.filename != '':
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(foto.filename)
            ruta = os.path.join(UPLOAD_FOLDER, filename)
            foto.save(ruta)
            vehiculo.foto = ruta
        db.session.commit()

    registro_activo_cliente = Registro.query.filter_by(id_cliente=cliente.id_cliente, estado='abierto').first()
    registro_activo_vehiculo = Registro.query.filter_by(id_vehiculo=vehiculo.id_vehiculo, estado='abierto').first()
    if registro_activo_cliente or registro_activo_vehiculo:
        flash("No se puede registrar el ingreso. El cliente o el vehículo ya se encuentran dentro del parqueo.")
        return redirect(url_for('administrador.ingreso'))

    # --- Fecha ingreso UTC-4 ---
    hora_actual = datetime.now(timezone(timedelta(hours=-4)))
    registro = Registro(
        id_cliente=cliente.id_cliente,
        id_vehiculo=vehiculo.id_vehiculo,
        fecha_ingreso=hora_actual,
        estado='abierto'
    )
    db.session.add(registro)
    db.session.commit()

    flash("Ingreso registrado correctamente")
    return redirect(url_for('administrador.inicio'))

# --- SALIDA ---
@administrador_bp.route('/salida')
def salida():
    if not requiere_admin():
        return redirect(url_for('auth.login'))
    return render_template('administrador/salida.html')

# --- BUSCAR REGISTRO POR PLACA (AJAX) ---
@administrador_bp.route('/buscar_registro/<placa>')
def buscar_registro(placa):
    registro = Registro.query.join(Vehiculo).join(Cliente)\
        .filter(Vehiculo.placa==placa, Registro.estado=='abierto').first()
    if registro:
        tiempo_minutos = int((datetime.now(timezone(timedelta(hours=-4))) - registro.fecha_ingreso).total_seconds() / 60)
        tarifa = Tarifa.query.filter_by(tipo_vehiculo=registro.vehiculo.tipo).first()
        return jsonify({
            'registro': {
                'id_registro': registro.id_registro
            },
            'cliente': {
                'nombre': registro.cliente.nombre,
                'apellido_paterno': registro.cliente.apellido_paterno
            },
            'tiempo_minutos': tiempo_minutos,
            'tarifa_precio_hora': tarifa.precio_hora
        })
    return jsonify({'registro': None})

# --- GUARDAR SALIDA ---
@administrador_bp.route('/guardar_salida', methods=['POST'])
def guardar_salida():
    if not requiere_admin():
        return redirect(url_for('auth.login'))

    id_registro = request.form.get('id_registro')
    total_pagar = request.form.get('total_pagar')

    registro = Registro.query.get(id_registro)
    if registro and registro.estado=='abierto':
        registro.estado = 'cerrado'
        registro.total_pagar = float(total_pagar)
        registro.fecha_salida = datetime.now(timezone(timedelta(hours=-4)))
        db.session.commit()
        flash("Salida registrada correctamente")
    else:
        flash("Registro no encontrado o ya cerrado")
    return redirect(url_for('administrador.inicio'))
