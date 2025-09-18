from flask import Blueprint, request, jsonify
from app.models.rutina import Rutina, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

rutina_bp = Blueprint('rutinas', __name__, url_prefix='/api')



@rutina_bp.route('/rutinas', methods=['POST'])
@jwt_required()
def crear_rutina():
    identidad = get_jwt_identity()
    claims = get_jwt()
    data = request.get_json()

    nombre = data.get('nombre')
    dia = data.get('dia')
    nivel = data.get('nivel')
    tipo = data.get('tipo')
    ejercicios = data.get('ejercicios')

    if not all([nombre, dia, nivel, tipo, ejercicios]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    if not isinstance(ejercicios, list):
        return jsonify({"error": "El campo 'ejercicios' debe ser una lista"}), 400


    usuario_id_destino = identidad
    if claims.get("rol") == "admin" and data.get("usuario_id"):
        usuario_id_destino = data.get("usuario_id")

    nueva_rutina = Rutina(
        nombre=nombre,
        dia=dia,
        nivel=nivel,
        tipo=tipo,
        descripcion=data.get('descripcion'),
        duracion_min=data.get('duracion_min'),
        enfoque=data.get('enfoque'),
        ejercicios=ejercicios,
        usuario_id=usuario_id_destino
    )

    db.session.add(nueva_rutina)
    db.session.commit()

    return jsonify({
        "mensaje": "Rutina creada con éxito",
        "id": nueva_rutina.id,
        "usuario_id": nueva_rutina.usuario_id
    }), 201



@rutina_bp.route('/rutinas', methods=['GET'])
@jwt_required()
def obtener_rutinas():
    identidad = get_jwt_identity()
    rutinas = Rutina.query.filter_by(usuario_id=identidad).all()

    resultado = []
    for r in rutinas:
        resultado.append({
            "id": r.id,
            "nombre": r.nombre,
            "dia": r.dia,
            "nivel": r.nivel,
            "tipo": r.tipo,
            "descripcion": r.descripcion,
            "duracion_min": r.duracion_min,
            "enfoque": r.enfoque,
            "ejercicios": r.ejercicios
        })

    return jsonify(resultado), 200



@rutina_bp.route('/rutinas/<int:id>', methods=['GET'])
@jwt_required()
def obtener_rutina(id):
    identidad = int(get_jwt_identity())
    claims = get_jwt()
    rutina = Rutina.query.get(id)

    if not rutina:
        return jsonify({"error": "Rutina no encontrada"}), 404

    if rutina.usuario_id != identidad and claims.get('rol') != 'admin':
        return jsonify({"error": "Acceso no autorizado"}), 403

    return jsonify({
        "id": rutina.id,
        "nombre": rutina.nombre,
        "dia": rutina.dia,
        "nivel": rutina.nivel,
        "tipo": rutina.tipo,
        "descripcion": rutina.descripcion,
        "duracion_min": rutina.duracion_min,
        "enfoque": rutina.enfoque,
        "ejercicios": rutina.ejercicios
    }), 200



@rutina_bp.route('/rutinas/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def obtener_rutinas_de_usuario(usuario_id):
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({"error": "No tienes permisos para ver esta información"}), 403

    rutinas = Rutina.query.filter_by(usuario_id=usuario_id).all()
    resultado = []

    for r in rutinas:
        resultado.append({
            "id": r.id,
            "nombre": r.nombre,
            "dia": r.dia,
            "nivel": r.nivel,
            "tipo": r.tipo,
            "descripcion": r.descripcion,
            "duracion_min": r.duracion_min,
            "enfoque": r.enfoque,
            "ejercicios": r.ejercicios
        })

    return jsonify(resultado), 200



@rutina_bp.route('/rutinas/<int:id>', methods=['PUT'])
@jwt_required()
def editar_rutina(id):
    identidad = int(get_jwt_identity())
    claims = get_jwt()
    rutina = Rutina.query.get(id)

    if not rutina or (rutina.usuario_id != identidad and claims.get('rol') != 'admin'):
        return jsonify({"error": "Rutina no encontrada o acceso no autorizado"}), 404

    data = request.get_json()
    rutina.nombre = data.get('nombre', rutina.nombre)
    rutina.dia = data.get('dia', rutina.dia)
    rutina.nivel = data.get('nivel', rutina.nivel)
    rutina.tipo = data.get('tipo', rutina.tipo)
    rutina.descripcion = data.get('descripcion', rutina.descripcion)
    rutina.duracion_min = data.get('duracion_min', rutina.duracion_min)
    rutina.enfoque = data.get('enfoque', rutina.enfoque)

    nuevos_ejercicios = data.get('ejercicios')
    if nuevos_ejercicios is not None:
        if not isinstance(nuevos_ejercicios, list):
            return jsonify({"error": "El campo 'ejercicios' debe ser una lista"}), 400
        rutina.ejercicios = nuevos_ejercicios

    db.session.commit()
    return jsonify({"mensaje": "Rutina actualizada"}), 200



@rutina_bp.route('/rutinas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_rutina(id):
    identidad = int(get_jwt_identity())
    claims = get_jwt()  
    rutina = Rutina.query.get(id)

    
    if not rutina or (rutina.usuario_id != identidad and claims.get('rol') != 'admin'):
        return jsonify({"error": "Rutina no encontrada o acceso no autorizado"}), 404

    db.session.delete(rutina)
    db.session.commit()

    return jsonify({
        "mensaje": f"Rutina {id} eliminada correctamente",
        "id": id,
        "usuario_id": rutina.usuario_id
    }), 200

