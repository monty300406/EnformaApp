from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicializa la base de datos
db.init_app(app)

# Registra las rutas de autenticación
app.register_blueprint(auth_bp)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
