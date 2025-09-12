import pytest
import json
from app import create_app, db
from models.user import User
from models.rutina import Rutina
from flask_jwt_extended import create_access_token


@pytest.fixture
def client():
    app = create_app(testing=True)  
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  

    with app.app_context():
        db.create_all()

        # Crear usuario normal
        user = User(nombre="Test User", email="test@example.com", rol="usuario")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

        # Crear usuario admin
        admin = User(nombre="Admin User", email="admin@example.com", rol="admin")
        admin.set_password("123456")
        db.session.add(admin)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()


def get_token(client, email="test@example.com", rol="usuario"):
    with client.application.app_context():
        user = User.query.filter_by(email=email).first()
        token = create_access_token(identity=user.id, additional_claims={"rol": rol})
        return token


# -------------------------------
# TESTS
# -------------------------------

def test_crear_rutina(client):
    token = get_token(client)

    response = client.post(
        "/api/rutinas",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Rutina fuerza",
            "dia": "Lunes",
            "nivel": "Intermedio",
            "tipo": "Fuerza",
            "ejercicios": ["Press banca", "Sentadillas"]
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert "Rutina creada con éxito" in data["mensaje"]


def test_obtener_rutinas(client):
    token = get_token(client)

    response = client.get(
        "/api/rutinas",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_obtener_rutina(client):
    token = get_token(client)

    # Crear primero una rutina
    client.post(
        "/api/rutinas",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Rutina pecho",
            "dia": "Martes",
            "nivel": "Principiante",
            "tipo": "Hipertrofia",
            "ejercicios": ["Press banca"]
        },
    )

    response = client.get(
        "/api/rutinas/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["nombre"] == "Rutina pecho"


def test_editar_rutina(client):
    token = get_token(client)

    client.post(
        "/api/rutinas",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Rutina vieja",
            "dia": "Miercoles",
            "nivel": "Intermedio",
            "tipo": "Fuerza",
            "ejercicios": ["Sentadillas"]
        },
    )

    response = client.put(
        "/api/rutinas/1",
        headers={"Authorization": f"Bearer {token}"},
        json={"nombre": "Rutina actualizada"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["mensaje"] == "Rutina actualizada"


def test_eliminar_rutina(client):
    token = get_token(client)

    client.post(
        "/api/rutinas",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "nombre": "Rutina eliminar",
            "dia": "Viernes",
            "nivel": "Avanzado",
            "tipo": "Cardio",
            "ejercicios": ["Correr"]
        },
    )

    response = client.delete(
        "/api/rutinas/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "eliminada" in data["mensaje"]


def test_obtener_rutinas_de_usuario_admin(client):
    token_admin = get_token(client, email="admin@example.com", rol="admin")

    response = client.get(
        "/api/rutinas/usuario/1",
        headers={"Authorization": f"Bearer {token_admin}"}
    )

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
