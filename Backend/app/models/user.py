from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default='usuario')

   
    rutinas = db.relationship("Rutina", back_populates="usuario", cascade="all, delete-orphan")

    def set_password(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)
