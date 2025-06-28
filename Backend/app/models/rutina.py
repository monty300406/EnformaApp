# models/rutina.py
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from . import db

class Rutina(db.Model):
    __tablename__ = 'rutinas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(20), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_min = db.Column(db.Integer)
    enfoque = db.Column(db.String(100))
    ejercicios = db.Column(JSON, nullable=False)

    usuario_id = db.Column(db.Integer, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
