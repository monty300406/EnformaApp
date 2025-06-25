from flask import Flask
from flask_cors import CORS
from config import Config
from models.user import db
from routes.auth_routes import auth_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)


db.init_app(app)


app.register_blueprint(auth_bp)


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
