from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp
from routes.rutina_routes import rutina_bp  
from routes.ejercicio_routes import ejercicio_bp
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)

    # Cargar configuración (por defecto usa Config, pero en tests se puede pasar TestConfig)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        return str(identity["id"])

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {"rol": identity["rol"]}

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(rutina_bp)
    app.register_blueprint(ejercicio_bp)

    # Rutas de prueba
    @app.route('/')
    def home():
        return "¡Bienvenido a EnFormaAPP!"

    @app.route('/test')
    def test():
        return "Ruta de prueba OK"

    with app.app_context():
        db.create_all()
        print("Tablas creadas:", db.metadata.tables.keys())

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
