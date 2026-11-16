
from datetime import date
from functools import wraps
from sqlalchemy import or_

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from flask_login import current_user, login_required

from extensions import db
from models.avaliacao import (
    Apresentacao,
    Avaliacao,
    NotaAvaliacao,
    CRITERIOS_AVALIACAO
)
from models.usuario import Usuario


avaliacoes_bp = Blueprint(
    "avaliacoes",
    __name__,
    url_prefix="/avaliacoes"
)


def equipe_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.perfil not in ("admin", "professor"):
            abort(403)

        return view(*args, **kwargs)

    return wrapped


# LISTAR APRESENTAÇÕES
@avaliacoes_bp.route("/")
@login_required
def lista():

    if current_user.perfil in ("admin", "professor"):
        apresentacoes = (
            Apresentacao.query
            .order_by(Apresentacao.data.desc())
            .all()
        )
    else:
        apresentacoes = (
            Apresentacao.query
            .join(Apresentacao.participantes)
            .filter(Usuario.id == current_user.id)
            .order_by(Apresentacao.data.desc())
            .all()
        )

    return render_template(
        "avaliacoes/lista.html",
        apresentacoes=apresentacoes
    )


# CADASTRAR APRESENTAÇÃO
@avaliacoes_bp.route("/nova-apresentacao", methods=["GET", "POST"])
@equipe_required
def nova_apresentacao():

    alunos = (
        Usuario.query
        .filter_by(perfil="aluno", ativo=True)
        .order_by(Usuario.nome.asc())
        .all()
    )

    if request.method == "POST":

        titulo = request.form.get("titulo", "").strip()
        data_texto = request.form.get("data", "").strip()
        descricao = request.form.get("descricao", "").strip()
        participantes_ids = request.form.getlist("participantes")

        if not titulo or not data_texto or not participantes_ids:
            flash(
                "Preencha o título, a data e selecione os participantes.",
                "error"
            )
            return render_template(
                "avaliacoes/apresentacao_form.html",
                alunos=alunos
            )

        try:
            data_apresentacao = date.fromisoformat(data_texto)
        except ValueError:
            flash("Informe uma data válida.", "error")
            return render_template(
                "avaliacoes/apresentacao_form.html",
                alunos=alunos
            )

        try:
            ids = {int(valor) for valor in participantes_ids}
        except ValueError:
            flash("Seleção de participantes inválida.", "error")
            return render_template(
                "avaliacoes/apresentacao_form.html",
                alunos=alunos
            )

        participantes = (
            Usuario.query
            .filter(
                Usuario.id.in_(ids),
                Usuario.perfil == "aluno",
                Usuario.ativo.is_(True)
            )
            .all()
        )

        if len(participantes) != len(ids):
            flash("Um ou mais participantes são inválidos.", "error")
            return render_template(
                "avaliacoes/apresentacao_form.html",
                alunos=alunos
            )

        apresentacao = Apresentacao(
            titulo=titulo,
            data=data_apresentacao,
            descricao=descricao,
            criada_por_id=current_user.id,
            participantes=participantes
        )

        db.session.add(apresentacao)
        db.session.commit()

        flash("Apresentação cadastrada com sucesso!", "success")

        return redirect(url_for("avaliacoes.lista"))

    return render_template(
        "avaliacoes/apresentacao_form.html",
        alunos=alunos
    )


# CRIAR AVALIAÇÃO
@avaliacoes_bp.route(
    "/<int:apresentacao_id>/avaliar",
    methods=["GET", "POST"]
)
@equipe_required
def avaliar(apresentacao_id):

    apresentacao = db.get_or_404(Apresentacao, apresentacao_id)

    alunos = sorted(
        apresentacao.participantes,
        key=lambda aluno: aluno.nome.lower()
    )

    if not alunos:
        flash(
            "Esta apresentação não possui participantes.",
            "error"
        )
        return redirect(url_for("avaliacoes.lista"))

    if request.method == "POST":

        tipo = request.form.get("tipo", "")
        aluno_id = request.form.get("aluno_id", type=int)
        observacoes = request.form.get("observacoes", "").strip()

        if tipo not in ("individual", "coletiva"):
            flash("Selecione um tipo de avaliação válido.", "error")
            return redirect(
                url_for(
                    "avaliacoes.avaliar",
                    apresentacao_id=apresentacao.id
                )
            )

        aluno = None

        if tipo == "individual":

            aluno = next(
                (
                    participante
                    for participante in alunos
                    if participante.id == aluno_id
                ),
                None
            )

            if aluno is None:
                flash("Selecione um participante válido.", "error")
                return redirect(
                    url_for(
                        "avaliacoes.avaliar",
                        apresentacao_id=apresentacao.id
                    )
                )

        notas = {}

        for criterio in CRITERIOS_AVALIACAO:

            pontuacao = request.form.get(criterio, type=int)

            if pontuacao is None or not 1 <= pontuacao <= 10:
                flash(
                    "Todas as notas devem estar entre 1 e 10.",
                    "error"
                )
                return redirect(
                    url_for(
                        "avaliacoes.avaliar",
                        apresentacao_id=apresentacao.id
                    )
                )

            notas[criterio] = pontuacao

        avaliacao = Avaliacao(
            apresentacao_id=apresentacao.id,
            professor_id=current_user.id,
            aluno_id=aluno.id if aluno else None,
            tipo=tipo,
            observacoes=observacoes,
            publicada=False
        )

        db.session.add(avaliacao)

        for criterio, pontuacao in notas.items():

            nota = NotaAvaliacao(
                avaliacao=avaliacao,
                criterio=criterio,
                pontuacao=pontuacao
            )

            db.session.add(nota)

        db.session.commit()

        flash(
            "Avaliação salva como rascunho.",
            "success"
        )

        return redirect(url_for("avaliacoes.lista"))

    return render_template(
        "avaliacoes/avaliacao_form.html",
        apresentacao=apresentacao,
        alunos=alunos,
        criterios=CRITERIOS_AVALIACAO
    )

# VISUALIZAR E REVISAR AVALIAÇÕES
@avaliacoes_bp.route("/<int:apresentacao_id>/resultados")
@login_required
def resultados(apresentacao_id):

    apresentacao = db.get_or_404(Apresentacao, apresentacao_id)

    equipe = current_user.perfil in ("admin", "professor")

    if not equipe:
        participa = any(
            aluno.id == current_user.id
            for aluno in apresentacao.participantes
        )

        if current_user.perfil != "aluno" or not participa:
            abort(403)

    consulta = Avaliacao.query.filter_by(
        apresentacao_id=apresentacao.id
    )

    if not equipe:
        consulta = consulta.filter(
            Avaliacao.publicada.is_(True)
        ).filter(
            or_(
                Avaliacao.tipo == "coletiva",
                Avaliacao.aluno_id == current_user.id
            )
        )

    avaliacoes = consulta.order_by(Avaliacao.criada_em.desc()).all()

    return render_template(
        "avaliacoes/resultados.html",
        apresentacao=apresentacao,
        avaliacoes=avaliacoes,
        equipe=equipe,
        criterios=CRITERIOS_AVALIACAO
    )


# PUBLICAR UMA AVALIAÇÃO
@avaliacoes_bp.route(
    "/avaliacao/<int:avaliacao_id>/publicar",
    methods=["POST"]
)
@equipe_required
def publicar(avaliacao_id):

    avaliacao = db.get_or_404(Avaliacao, avaliacao_id)

    avaliacao.publicada = True
    db.session.commit()

    flash("Avaliação publicada com sucesso!", "success")

    return redirect(
        url_for(
            "avaliacoes.resultados",
            apresentacao_id=avaliacao.apresentacao_id
        )
    )
