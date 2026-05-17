from app.database.db import db
from datetime import datetime
from zoneinfo import ZoneInfo

class Encomenda(db.Model):
    __tablename__ = 'encomendas'

    id = db.Column(db.Integer, primary_key=True)

    destinatario = db.Column(
        db.String(100),
        nullable=False
    )

    bloco = db.Column(
        db.String(10),
        nullable=False
    )

    apartamento = db.Column(
        db.String(10),
        nullable=False
    )

    descricao = db.Column(
        db.String(255)
    )

    retirado = db.Column(
        db.Boolean,
        default=False
    )

    data_recebimento = db.Column(
        db.DateTime,
        default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")).replace(tzinfo=None)
    )