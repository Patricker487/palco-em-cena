
from datetime import datetime

from extensions import db


CRITERIOS_AVALIACAO = {
    "interpretacao": "Interpretação",
    "expressao_corporal": "Expressão corporal",
    "diccao": "Dicção",
    "criatividade": "Criatividade",
    "presenca_palco": "Presença de palco",
}


# Alunos participantes de uma apresentação
participantes_apresentacao = db.Table(
    "participantes_apresentacao",

    db.Column(
        "apresentacao_id",
        db.Integer,
        db.ForeignKey("apresentacoes.id"),
        primary_key=True
    ),

    db.Column(
        "aluno_id",
        db.Integer,
        db.ForeignKey("usuarios.id"),
        primary_key=True
    )
)


class Apresentacao(db.Model):
    __tablename__ = "apresentacoes"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(
        db.String(140),
        nullable=False
    )

    data = db.Column(
        db.Date,
        nullable=False
    )

    descricao = db.Column(db.Text)

    criada_por_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    criada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    participantes = db.relationship(
        "Usuario",
        secondary=participantes_apresentacao
    )

    criador = db.relationship(
        "Usuario",
        foreign_keys=[criada_por_id]
    )


class Avaliacao(db.Model):
    __tablename__ = "avaliacoes"

    id = db.Column(db.Integer, primary_key=True)

    apresentacao_id = db.Column(
        db.Integer,
        db.ForeignKey("apresentacoes.id"),
        nullable=False
    )

    professor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    aluno_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    # individual ou coletiva
    tipo = db.Column(
        db.String(20),
        nullable=False
    )

    observacoes = db.Column(
        db.Text,
        default=""
    )

    publicada = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    criada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    apresentacao = db.relationship(
        "Apresentacao",
        backref=db.backref(
            "avaliacoes",
            cascade="all, delete-orphan"
        )
    )

    professor = db.relationship(
        "Usuario",
        foreign_keys=[professor_id]
    )

    aluno = db.relationship(
        "Usuario",
        foreign_keys=[aluno_id]
    )

    notas = db.relationship(
        "NotaAvaliacao",
        backref="avaliacao",
        cascade="all, delete-orphan"
    )


class NotaAvaliacao(db.Model):
    __tablename__ = "notas_avaliacao"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    avaliacao_id = db.Column(
        db.Integer,
        db.ForeignKey("avaliacoes.id"),
        nullable=False
    )

    criterio = db.Column(
        db.String(40),
        nullable=False
    )

    pontuacao = db.Column(
        db.Integer,
        nullable=False
    )
