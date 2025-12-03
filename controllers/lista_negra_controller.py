from flask import Blueprint, render_template, request, redirect, url_for
from models.lista_negra_model import ListaNegra
from models import db
from datetime import datetime

lista_negra_bp = Blueprint(
    'lista_negra',
    __name__,
    url_prefix='/lista-negra',
    template_folder='../templates/administrador'
)

@lista_negra_bp.route('/')
def index():
    entradas = ListaNegra.query.all()
    return render_template('lista_negra.html', entradas=entradas)

@lista_negra_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        id_vehiculo = request.form.get('id_vehiculo')
        id_cliente = request.form.get('id_cliente')
        estado = request.form.get('estado')
        registrado_por = request.form.get('registrado_por')

        registro = ListaNegra(
            id_vehiculo=id_vehiculo,
            id_cliente=id_cliente,
            estado=estado,
            registrado_por=registrado_por,
            fecha_registro=datetime.utcnow()
        )
        db.session.add(registro)
        db.session.commit()
        return redirect(url_for('lista_negra.index'))

    # Cambia aquí el nombre del template a tu archivo real
    return render_template('lista_negra_form.html', entrada=None)
