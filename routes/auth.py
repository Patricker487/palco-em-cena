from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("dashboard.index"))

        flash("E-mail ou senha incorretos.", "error")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.login"))
