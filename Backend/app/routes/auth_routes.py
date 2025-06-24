from flask import Blueprint, request, jsonify
from models.user import User, db

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not all([nombre, email, contraseña]):
        return jsonify({"error": "Faltan datos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Correo ya registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email)
    nuevo_usuario.set_password(contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    contraseña = data.get('contraseña')

    usuario = User.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(contraseña):
        return jsonify({"error": "Credenciales inválidas"}), 401

    return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
