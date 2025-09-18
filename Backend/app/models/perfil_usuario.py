from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class PerfilUsuario(db.Model):
    __tablename__ = 'perfiles_usuario'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, ForeignKey("users.id"), unique=True, nullable=False)
    sexo = db.Column(db.String(10))
    edad = db.Column(db.Integer)
    peso = db.Column(db.Float)
    altura = db.Column(db.Integer)
    nivel_actividad = db.Column(db.String(50))
    objetivo = db.Column(db.String(50))
    
    # Relación inversa con el modelo User
    usuario = relationship("User", back_populates="perfil")