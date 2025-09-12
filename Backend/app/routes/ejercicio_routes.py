from flask import Blueprint, request, jsonify
from models.ejercicio import Ejercicio, db
from flask_jwt_extended import jwt_required, get_jwt

ejercicio_bp = Blueprint('ejercicios', __name__, url_prefix='/api')

# Crear ejercicio (solo admin)
@ejercicio_bp.route('/ejercicios', methods=['POST'])
@jwt_required()
def crear_ejercicio():
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({"error": "Solo los administradores pueden crear ejercicios"}), 403

    data = request.get_json()
    nombre = data.get('nombre')
    musculo = data.get('musculo')

    if not nombre or not musculo:
        return jsonify({"error": "Nombre y músculo son obligatorios"}), 400

    nuevo = Ejercicio(
        nombre=nombre,
        musculo=musculo,
        tipo=data.get('tipo'),
        equipo=data.get('equipo'),
        dificultad=data.get('dificultad'),
        descripcion=data.get('descripcion')
    )

    db.session.add(nuevo)
    db.session.commit()

    
    return jsonify({
        "mensaje": "Ejercicio creado con éxito",
        "id": nuevo.id
    }), 201


# Obtener todos los ejercicios
@ejercicio_bp.route('/ejercicios', methods=['GET'])
@jwt_required()
def obtener_ejercicios():
    ejercicios = Ejercicio.query.all()
    resultado = [{
        "nombre": e.nombre,
        "id": e.id,
        "musculo": e.musculo,
        "tipo": e.tipo,
        "equipo": e.equipo,
        "dificultad": e.dificultad,
        "descripcion": e.descripcion
    } for e in ejercicios]

    return jsonify(resultado), 200

# Obtener ejercicio por ID
@ejercicio_bp.route('/ejercicios/<int:id>', methods=['GET'])
@jwt_required()
def obtener_ejercicio(id):
    ejercicio = Ejercicio.query.get(id)
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    return jsonify({
        "id": ejercicio.id,
        "nombre": ejercicio.nombre,
        "musculo": ejercicio.musculo,
        "tipo": ejercicio.tipo,
        "equipo": ejercicio.equipo,
        "dificultad": ejercicio.dificultad,
        "descripcion": ejercicio.descripcion
    }), 200

# Editar ejercicio (solo admin)
@ejercicio_bp.route('/ejercicios/<int:id>', methods=['PUT'])
@jwt_required()
def editar_ejercicio(id):
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({"error": "Solo los administradores pueden editar ejercicios"}), 403

    ejercicio = Ejercicio.query.get(id)
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    data = request.get_json()
    ejercicio.nombre = data.get('nombre', ejercicio.nombre)
    ejercicio.musculo = data.get('musculo', ejercicio.musculo)
    ejercicio.tipo = data.get('tipo', ejercicio.tipo)
    ejercicio.equipo = data.get('equipo', ejercicio.equipo)
    ejercicio.dificultad = data.get('dificultad', ejercicio.dificultad)
    ejercicio.descripcion = data.get('descripcion', ejercicio.descripcion)

    db.session.commit()
    return jsonify({"mensaje": "Ejercicio actualizado"}), 200

# Eliminar ejercicio (solo admin)
@ejercicio_bp.route('/ejercicios/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_ejercicio(id):
    claims = get_jwt()
    if claims.get('rol') != 'admin':
        return jsonify({"error": "Solo los administradores pueden eliminar ejercicios"}), 403

    ejercicio = Ejercicio.query.get(id)
    if not ejercicio:
        return jsonify({"error": "Ejercicio no encontrado"}), 404

    db.session.delete(ejercicio)
    db.session.commit()
    return jsonify({"mensaje": f"Ejercicio {id} eliminado"}), 200
