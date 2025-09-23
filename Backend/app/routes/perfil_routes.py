from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User, db
from app.models.perfil_usuario import PerfilUsuario

perfil_bp = Blueprint("perfil", __name__, url_prefix="/api")

# ------------------------------
# CONSULTAR PERFIL (GET)
# ------------------------------
@perfil_bp.route("/perfil", methods=["GET"])
@jwt_required()
def consultar_perfil():
    usuario_id = int(get_jwt_identity()) 
    claims = get_jwt()

    usuario = User.query.filter_by(id=usuario_id).first()
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    perfil = PerfilUsuario.query.filter_by(usuario_id=usuario.id).first()
    if not perfil:
        return jsonify({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": claims["rol"],
            "perfil": None
        }), 200

    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": claims["rol"],
        "perfil": {
            "sexo": perfil.sexo,
            "edad": perfil.edad,
            "peso": perfil.peso,
            "altura": perfil.altura,
            "nivel_actividad": perfil.nivel_actividad,
            "objetivo": perfil.objetivo
        }
    }), 200

# ------------------------------
# CREAR PERFIL (POST)
# ------------------------------
@perfil_bp.route("/perfil", methods=["POST"])
@jwt_required()
def crear_perfil():
    usuario_id = int(get_jwt_identity())

    if PerfilUsuario.query.filter_by(usuario_id=usuario_id).first():
        return jsonify({"error": "El perfil ya existe"}), 400

    data = request.get_json()
    nuevo_perfil = PerfilUsuario(
        usuario_id=usuario_id,
        sexo=data.get("sexo"),
        edad=data.get("edad"),
        peso=data.get("peso"),
        altura=data.get("altura"),
        nivel_actividad=data.get("nivel_actividad"),
        objetivo=data.get("objetivo"),
    )

    db.session.add(nuevo_perfil)
    db.session.commit()

    return jsonify({"mensaje": "Perfil creado con éxito"}), 201

# ------------------------------
# ACTUALIZAR PERFIL (PUT)
# ------------------------------
@perfil_bp.route("/perfil", methods=["PUT"])
@jwt_required()
def actualizar_perfil():
    usuario_id = int(get_jwt_identity())

    perfil = PerfilUsuario.query.filter_by(usuario_id=usuario_id).first()
    if not perfil:
        return jsonify({"error": "Perfil no encontrado"}), 404

    data = request.get_json()
    perfil.sexo = data.get("sexo", perfil.sexo)
    perfil.edad = data.get("edad", perfil.edad)
    perfil.peso = data.get("peso", perfil.peso)
    perfil.altura = data.get("altura", perfil.altura)
    perfil.nivel_actividad = data.get("nivel_actividad", perfil.nivel_actividad)
    perfil.objetivo = data.get("objetivo", perfil.objetivo)

    db.session.commit()

    return jsonify({"mensaje": "Perfil actualizado con éxito"}), 200

# ------------------------------
# ELIMINAR PERFIL (DELETE) SOLO ADMIN
# ------------------------------
@perfil_bp.route("/perfil/<int:usuario_id>", methods=["DELETE"])
@jwt_required()
def eliminar_perfil(usuario_id):
    claims = get_jwt()
    rol = claims["rol"]

    if rol != "admin":
        return jsonify({"error": "No tienes permisos para eliminar perfiles"}), 403

    perfil = PerfilUsuario.query.filter_by(usuario_id=usuario_id).first()
    if not perfil:
        return jsonify({"error": "Perfil no encontrado"}), 404

    db.session.delete(perfil)
    db.session.commit()

    return jsonify({"mensaje": f"Perfil del usuario {usuario_id} eliminado con éxito"}), 200

# ------------------------------
# OBTENER TODOS LOS PERFILES (GET) SOLO ADMIN
# ------------------------------
@perfil_bp.route("/perfiles", methods=["GET"])
@jwt_required()
def obtener_todos_los_perfiles():
    claims = get_jwt()
    if claims["rol"] != "admin":
        return jsonify({"error": "No tienes permisos para ver esta información"}), 403

    usuarios = User.query.all()
    lista_usuarios_con_perfil = []
    for usuario in usuarios:
        perfil = PerfilUsuario.query.filter_by(usuario_id=usuario.id).first()
        perfil_data = {
            "sexo": perfil.sexo if perfil else None,
            "edad": perfil.edad if perfil else None,
            "peso": perfil.peso if perfil else None,
            "altura": perfil.altura if perfil else None,
            "nivel_actividad": perfil.nivel_actividad if perfil else None,
            "objetivo": perfil.objetivo if perfil else None
        }

        lista_usuarios_con_perfil.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol": usuario.rol,
            "perfil": perfil_data
        })

    return jsonify(lista_usuarios_con_perfil), 200

# ------------------------------
# RECOMENDACION DE NUTRICION Y RUTINA
# ------------------------------
@perfil_bp.route("/perfil/recomendacion", methods=["GET"])
@jwt_required()
def recomendacion_perfil():
    usuario_id = int(get_jwt_identity())

    perfil = PerfilUsuario.query.filter_by(usuario_id=usuario_id).first()
    if not perfil:
        return jsonify({"error": "Perfil no encontrado"}), 404

    # Calculo TMB (Harris-Benedict simplificado)
    if perfil.sexo.lower() == "masculino":
        tmb = 10 * perfil.peso + 6.25 * perfil.altura - 5 * perfil.edad + 5
    else:
        tmb = 10 * perfil.peso + 6.25 * perfil.altura - 5 * perfil.edad - 161

    # Factor de actividad
    nivel = perfil.nivel_actividad.lower() if perfil.nivel_actividad else "bajo"
    factor_actividad = 1.2
    if nivel == "medio":
        factor_actividad = 1.55
    elif nivel == "alto":
        factor_actividad = 1.9

    calorias_mantenimiento = tmb * factor_actividad
    calorias_finales = calorias_mantenimiento
    mensaje = "Tu objetivo es mantener peso, por lo que se mantienen las calorías de mantenimiento."

    # Ajuste según objetivo
    objetivo = perfil.objetivo.lower() if perfil.objetivo else ""
    if objetivo in ["perder peso", "perder_peso"]:
        calorias_finales -= 500
        mensaje = "Debido a tu objetivo de perder peso, se restaron 500 kcal a tus calorías de mantenimiento."
    elif objetivo in ["ganar músculo", "ganar_musculo"]:
        calorias_finales += 300
        mensaje = "Debido a tu objetivo de ganar músculo, se añadieron 300 kcal a tus calorías de mantenimiento."

    # ---------------------------
    # MACROS (reparto sencillo)
    # ---------------------------
    proteinas_g = perfil.peso * 2  # g/kg peso
    proteinas_kcal = proteinas_g * 4

    grasas_kcal = calorias_finales * 0.25
    grasas_g = grasas_kcal / 9

    carbohidratos_kcal = calorias_finales - (proteinas_kcal + grasas_kcal)
    carbohidratos_g = carbohidratos_kcal / 4

    # ---------------------------
    # RECOMENDACION DE RUTINA
    # ---------------------------
    tipo_rutina = "Full-Body"
    if objetivo in ["ganar músculo", "ganar_musculo"]:
        tipo_rutina = "Upper-Lower" if nivel != "alto" else "Push-Pull-Legs"

    return jsonify({
        "nutricion": {
            "calorias": round(calorias_finales),
            "mensaje": mensaje,
            "macronutrientes": {
                "proteinas_g": round(proteinas_g, 1),
                "carbohidratos_g": round(carbohidratos_g, 1),
                "grasas_g": round(grasas_g, 1)
            }
        },
        "rutina": {
            "tipo": tipo_rutina,
            "descripcion": f"Se recomienda la rutina {tipo_rutina} según tu objetivo y nivel de actividad."
        }
    }), 200
