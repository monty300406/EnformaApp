from flask import Blueprint, request, jsonify
from app.models.user import User, db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# ------------------------------
# REGISTRO
# ------------------------------
@auth_bp.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    contrasena = data.get('contrasena')
    rol = data.get('rol', 'usuario')

    if not all([nombre, email, contrasena]):
        return jsonify({"error": "Faltan datos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Correo ya registrado"}), 400

    nuevo_usuario = User(nombre=nombre, email=email, rol=rol)
    nuevo_usuario.set_password(contrasena)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({
        "mensaje": "Usuario registrado con éxito",
        "id": nuevo_usuario.id
    }), 201


# ------------------------------
# LOGIN
# ------------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    contrasena = data.get('contrasena')

    usuario = User.query.filter_by(email=email).first()

    if not usuario or not usuario.check_password(contrasena):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Guardamos solo el ID en identity
    access_token = create_access_token(
    identity=str(usuario.id),  # el id del usuario en string
    additional_claims={"rol": usuario.rol, "email": usuario.email}
)


    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "token": access_token
    }), 200


# ------------------------------
# OBTENER TODOS LOS USUARIOS (SOLO ADMIN)
# ------------------------------
@auth_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def obtener_usuarios():
    identidad = get_jwt_identity()  # ahora es "1", un string con el id
    claims = get_jwt()              # contiene {"rol": "admin", "email": "...", ...}

    if claims["rol"] != 'admin':
        return jsonify({"error": "No tienes permisos para ver todos los usuarios"}), 403

    usuarios = User.query.all()
    lista = [{
        "id": u.id,
        "nombre": u.nombre,
        "email": u.email,
        "rol": u.rol
    } for u in usuarios]

    return jsonify(lista), 200


# ------------------------------
# ELIMINAR USUARIO (SOLO ADMIN)
# ------------------------------
@auth_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def eliminar_usuario(usuario_id):
    identidad = get_jwt_identity()
    claims = get_jwt()

    # Solo los admins pueden eliminar usuarios
    if claims["rol"] != "admin":
        return jsonify({"error": "No tienes permisos para eliminar usuarios"}), 403

    usuario = User.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)  # Esto elimina perfil y rutinas por cascade
    db.session.commit()

    return jsonify({"mensaje": f"Usuario {usuario_id} eliminado con éxito"}), 200
