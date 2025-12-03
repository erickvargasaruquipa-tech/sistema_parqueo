import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import db, app
from models.parqueo_model import Parqueo

ajustes_parqueo_bp = Blueprint("ajustes_parqueo", __name__, url_prefix="/ajustes/parqueo")

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ========================
# LISTA / VER DATOS
# ========================
@ajustes_parqueo_bp.route("/")
def index():
    parqueo = Parqueo.query.first()
    return render_template("ajustes/parqueo/index.html", parqueo=parqueo)


# ========================
# FORMULARIO EDITAR
# ========================
@ajustes_parqueo_bp.route("/editar", methods=["GET", "POST"])
def editar():
    parqueo = Parqueo.query.first()

    if request.method == "POST":
        parqueo.nombre = request.form["nombre"]
        parqueo.direccion = request.form["direccion"]
        parqueo.telefono = request.form["telefono"]
        parqueo.horario_apertura = request.form["horario_apertura"]
        parqueo.horario_cierre = request.form["horario_cierre"]
        parqueo.capacidad_autos = request.form["capacidad_autos"]
        parqueo.capacidad_motos = request.form["capacidad_motos"]
        parqueo.descripcion = request.form["descripcion"]

        # Manejo del logo — OPCIONAL
        if "logo" in request.files:
            file = request.files["logo"]
            if file.filename != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                parqueo.logo = filename

        db.session.commit()
        flash("Datos del parqueo actualizados correctamente", "success")
        return redirect(url_for("ajustes_parqueo.index"))

    return render_template("ajustes/parqueo/editar.html", parqueo=parqueo)
