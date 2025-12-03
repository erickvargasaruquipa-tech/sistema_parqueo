from flask import Flask, redirect, url_for
from config import Config
from models import db, init_models
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar db
    db.init_app(app)

    # Crear carpetas de uploads
    UPLOAD_FOLDER_PARQUEOS = os.path.join('static', 'uploads', 'parqueos')
    UPLOAD_FOLDER_LISTA_NEGRA = os.path.join('static', 'uploads', 'lista_negra')

    os.makedirs(UPLOAD_FOLDER_PARQUEOS, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER_LISTA_NEGRA, exist_ok=True)

    # Registrar Blueprints
    from controllers.auth_controller import auth_bp
    from controllers.admin_controller import admin_bp
    from controllers.administrador_controller import administrador_bp
    from controllers.parqueo_controller import parqueo_bp
    from controllers.tarifas_controller import tarifas_bp
    from controllers.lista_negra_controller import lista_negra_bp
    from controllers.ingreso_controller import ingreso_bp
    from controllers.salida_controller import salida_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(administrador_bp)
    app.register_blueprint(parqueo_bp)
    app.register_blueprint(tarifas_bp)
    app.register_blueprint(lista_negra_bp)
    app.register_blueprint(ingreso_bp)
    app.register_blueprint(salida_bp)

    @app.route('/')
    def index():
        return redirect(url_for('administrador.inicio'))

    @app.route('/dashboard')
    def dashboard():
        return redirect(url_for('administrador.inicio'))

    # Crear tablas y superusuario
    with app.app_context():
        db.create_all()
        init_models.create_superusuario()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
