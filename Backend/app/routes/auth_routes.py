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
    rol = data.get('rol', 'usuario')  

    if not all([nombre, email, contraseña]):
        return jsonify({"error": "Faltan datos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Correo ya registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, rol=rol)
    nuevo_usuario.set_password(contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    
    return jsonify({
        "mensaje": "Usuario registrado con éxito",
        "id": nuevo_usuario.id
    }), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    contraseña = data.get('contraseña')

    usuario = User.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(contraseña):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Enviamos solo el ID como identidad (debe ser string/int)
    identity_data = {"id": usuario.id, "rol": usuario.rol}
    access_token = create_access_token(identity=identity_data)

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token
    }), 200


@auth_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(id):
    identidad = get_jwt_identity()      # ID como string
    claims = get_jwt()                  # Claims del token (rol)

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


@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({"error": "No tienes permisos para ver todos los usuarios"}), 403

    usuarios = User.query.all()
    lista = [{
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email,
        "rol": u.rol
    } for u in usuarios]

    return jsonify(lista), 200


@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    identidad = get_jwt_identity()
    usuario = User.query.get(int(identidad))

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol
    }), 200


@auth_bp.route('/perfil', methods=['PUT'])
@jwt_required()
def editar_perfil():
    identidad = get_jwt_identity()
    usuario = User.query.get(int(identidad))

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    data = request.get_json()
    nuevo_nombre = data.get('nombre')
    nuevo_email = data.get('email')

    if nuevo_nombre:
        usuario.nombre = nuevo_nombre
    if nuevo_email:
        usuario.email = nuevo_email

    db.session.commit()
    return jsonify({"mensaje": "Perfil actualizado"}), 200
