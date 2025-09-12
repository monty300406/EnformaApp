from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.orm import relationship
from . import db
from .user import User   

class Rutina(db.Model):
    __tablename__ = "rutinas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dia = db.Column(db.String(20), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_min = db.Column(db.Integer)
    enfoque = db.Column(db.String(100))
    ejercicios = db.Column(JSON, nullable=False)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

   
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    usuario = relationship("User", back_populates="rutinas")
