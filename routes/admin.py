from functools import wraps
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from extensions import db
from models.usuario import Usuario
from models.turma import Turma

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
PERFIS = {"professor": "Professor", "aluno": "Aluno"}

def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.perfil != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped

def dados_formulario(usuario=None):
    return render_template("admin/usuario_form.html", usuario=usuario, perfis=PERFIS, turmas=Turma.query.order_by(Turma.id).all())

@admin_bp.route("/usuarios")
@admin_required
def usuarios():
    termo = request.args.get("q", "").strip()
    consulta = Usuario.query
    if termo:
        busca = f"%{termo}%"
        consulta = consulta.filter(or_(Usuario.nome.ilike(busca), Usuario.email.ilike(busca)))
    lista = consulta.order_by(Usuario.nome.asc()).all()
    return render_template("admin/usuarios.html", usuarios=lista, termo=termo)

@admin_bp.route("/usuarios/novo", methods=["GET", "POST"])
@admin_required
def novo_usuario():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "")
        senha = request.form.get("senha", "")
        turma_id = request.form.get("turma_id", type=int)
        if not nome or not email or perfil not in PERFIS or len(senha) < 8:
            flash("Confira os campos. A senha deve ter pelo menos 8 caracteres.", "error")
            return dados_formulario()
        turma = db.session.get(Turma, turma_id) if turma_id else None
        if perfil == "aluno" and turma is None:
            flash("Selecione uma turma para o aluno.", "error")
            return dados_formulario()
        if Usuario.query.filter_by(email=email).first():
            flash("Já existe uma conta com esse e-mail.", "error")
            return dados_formulario()
        usuario = Usuario(nome=nome, email=email, perfil=perfil, ativo=True, turma=turma if perfil == "aluno" else None)
        usuario.set_password(senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso.", "success")
        return redirect(url_for("admin.usuarios"))
    return dados_formulario()

@admin_bp.route("/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
@admin_required
def editar_usuario(usuario_id):
    usuario = db.get_or_404(Usuario, usuario_id)
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        perfil = request.form.get("perfil", "")
        senha = request.form.get("senha", "")
        turma_id = request.form.get("turma_id", type=int)
        if not nome or not email or (perfil not in PERFIS and not (usuario.perfil == "admin" and perfil == "admin")):
            flash("Preencha nome, e-mail e perfil corretamente.", "error")
            return dados_formulario(usuario)
        existente = Usuario.query.filter(Usuario.email == email, Usuario.id != usuario.id).first()
        if existente:
            flash("Esse e-mail já está sendo usado por outra conta.", "error")
            return dados_formulario(usuario)
        if usuario.id == current_user.id and perfil != "admin":
            flash("Você não pode remover seu próprio perfil de administrador.", "error")
            return dados_formulario(usuario)
        if senha and len(senha) < 8:
            flash("A nova senha precisa ter pelo menos 8 caracteres.", "error")
            return dados_formulario(usuario)
        turma = db.session.get(Turma, turma_id) if turma_id else None
        if perfil == "aluno" and turma is None:
            flash("Selecione uma turma para o aluno.", "error")
            return dados_formulario(usuario)
        usuario.nome, usuario.email, usuario.perfil = nome, email, perfil
        usuario.turma = turma if perfil == "aluno" else None
        if senha:
            usuario.set_password(senha)
        db.session.commit()
        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for("admin.usuarios"))
    return dados_formulario(usuario)

@admin_bp.route("/usuarios/<int:usuario_id>/alternar-status", methods=["POST"])
@admin_required
def alternar_status(usuario_id):
    usuario = db.get_or_404(Usuario, usuario_id)
    if usuario.id == current_user.id:
        flash("Você não pode desativar sua própria conta.", "error")
        return redirect(url_for("admin.usuarios"))
    if usuario.ativo and usuario.perfil == "admin":
        total = Usuario.query.filter_by(perfil="admin", ativo=True).count()
        if total <= 1:
            flash("Não é possível desativar o único administrador ativo.", "error")
            return redirect(url_for("admin.usuarios"))
    usuario.ativo = not usuario.ativo
    db.session.commit()
    flash("Status da conta atualizado.", "success")
    return redirect(url_for("admin.usuarios"))
