import click
from sqlalchemy import inspect, text
from flask import Flask
from config import Config
from extensions import db, login_manager, csrf


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Entre na sua conta para continuar."
    login_manager.login_message_category = "info"

    from models.avaliacao import Apresentacao, Avaliacao, NotaAvaliacao
    from models.usuario import Usuario
    from models.turma import Turma
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.turmas import turmas_bp
    from routes.avaliacoes import avaliacoes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(turmas_bp)
    app.register_blueprint(avaliacoes_bp)

    @app.cli.command("init-db")
    def init_db():
        with app.app_context():
            db.create_all()
        click.echo("Banco de dados inicializado.")

    @app.cli.command("migrar-turmas")
    def migrar_turmas():
        """Cria as turmas fixas e adiciona turma_id sem apagar os dados existentes."""
        with app.app_context():
            db.create_all()
            inspector = inspect(db.engine)
            colunas = {col["name"] for col in inspector.get_columns("usuarios")}
            if "turma_id" not in colunas:
                with db.engine.begin() as conexao:
                    conexao.execute(text("ALTER TABLE usuarios ADD COLUMN turma_id INTEGER REFERENCES turmas(id)"))
            for nome in ("Juvenil", "Adolescentes", "Adultos"):
                if not Turma.query.filter_by(nome=nome).first():
                    db.session.add(Turma(nome=nome))
            db.session.commit()
        click.echo("Turmas criadas. Os usuários existentes foram preservados.")

    @app.cli.command("create-admin")
    @click.option("--nome", prompt="Nome do administrador")
    @click.option("--email", prompt="E-mail")
    @click.password_option()
    def create_admin(nome, email, password):
        email = email.strip().lower()
        with app.app_context():
            if Usuario.query.filter_by(email=email).first():
                raise click.ClickException("Já existe uma conta com esse e-mail.")
            admin = Usuario(nome=nome.strip(), email=email, perfil="admin")
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
        click.echo(f"Administrador {email} criado com sucesso.")
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
