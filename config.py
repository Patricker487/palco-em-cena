import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(INSTANCE_DIR / 'palco.db').as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
