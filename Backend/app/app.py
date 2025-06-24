from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicializar base de datos
db.init_app(app)

# Registrar blueprint
app.register_blueprint(auth_bp)

# Ruta de prueba (opcional)
@app.route('/')
def home():
    return "¡Bienvenido a EnFormaAPP!"

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
