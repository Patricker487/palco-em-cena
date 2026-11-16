from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)  # admin, professor, aluno
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    turma_id = db.Column(db.Integer, db.ForeignKey("turmas.id"), nullable=True)
    turma = db.relationship("Turma", back_populates="alunos")

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))
