from flask import Blueprint, request, jsonify
from models.user import User, db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')
    rol = data.get('rol', 'usuario')  # Por defecto es 'usuario'

    if not all([nombre, email, contraseña]):
        return jsonify({"error": "Faltan datos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Correo ya registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, rol=rol)
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

    identity_data = {"id": usuario.id, "rol": usuario.rol}
    access_token = create_access_token(identity=identity_data)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token
    }), 200


@auth_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(id):
    identidad = get_jwt_identity()      # Solo el id del usuario (como string)
    claims = get_jwt()                  # Contiene los claims extras, como el rol

    if claims.get('rol') != 'admin':
        return jsonify({"error": "No tienes permisos para realizar esta acción"}), 403

    if int(identidad) == id:
        return jsonify({"error": "No puedes eliminar tu propio usuario"}), 403

    usuario = User.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"mensaje": f"Usuario con ID {id} eliminado correctamente"}), 200
