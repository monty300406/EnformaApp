from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.models.user import db
from app.routes.auth_routes import auth_bp
from app.routes.rutina_routes import rutina_bp  
from app.routes.ejercicio_routes import ejercicio_bp
from app.routes.perfil_routes import perfil_bp
from flask_jwt_extended import JWTManager


jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)

    
    app.config.from_object(config_class)
    


    
    db.init_app(app)
    jwt.init_app(app)


    
    app.register_blueprint(auth_bp)
    app.register_blueprint(rutina_bp)
    app.register_blueprint(ejercicio_bp)
    app.register_blueprint(perfil_bp)

   
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
