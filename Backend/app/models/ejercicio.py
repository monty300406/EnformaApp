from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    musculo = db.Column(db.String(50), nullable=False) 
    tipo = db.Column(db.String(50))  
    equipo = db.Column(db.String(100))  
    dificultad = db.Column(db.String(20)) 
    descripcion = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
