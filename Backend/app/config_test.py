from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Base de datos en memoria
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "clave_secreta_test"  # clave solo para test
