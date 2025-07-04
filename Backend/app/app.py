from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp
from routes.rutina_routes import rutina_bp  
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(identity):
    return str(identity["id"])

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {"rol": identity["rol"]}

# 👇 Primero se crea la app, luego se registran los blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(rutina_bp)

@app.route('/')
def home():
    return "¡Bienvenido a EnFormaAPP!"

@app.route('/test')
def test():
    return "Ruta de prueba OK"

with app.app_context():
    db.create_all()
    print("Tablas creadas:", db.metadata.tables.keys())

if __name__ == '__main__':
    app.run(debug=True)
