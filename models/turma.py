from extensions import db


class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    alunos = db.relationship("Usuario", back_populates="turma", lazy="select")
