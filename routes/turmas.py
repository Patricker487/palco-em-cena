from functools import wraps
from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required
from sqlalchemy import func
from extensions import db
from models.turma import Turma
from models.usuario import Usuario

turmas_bp = Blueprint("turmas", __name__, url_prefix="/turmas")

def equipe_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.perfil not in ("admin", "professor"):
            abort(403)
        return view(*args, **kwargs)
    return wrapped

@turmas_bp.route("/")
@equipe_required
def lista():
    turmas = (db.session.query(Turma, func.count(Usuario.id))
              .outerjoin(Usuario, (Usuario.turma_id == Turma.id) & (Usuario.perfil == "aluno") & (Usuario.ativo.is_(True)))
              .group_by(Turma.id).order_by(Turma.id).all())
    return render_template("turmas/lista.html", turmas=turmas)

@turmas_bp.route("/<int:turma_id>")
@equipe_required
def detalhes(turma_id):
    turma = db.get_or_404(Turma, turma_id)
    alunos = (Usuario.query.filter_by(turma_id=turma.id, perfil="aluno", ativo=True)
              .order_by(Usuario.nome.asc()).all())
    return render_template("turmas/detalhes.html", turma=turma, alunos=alunos)
