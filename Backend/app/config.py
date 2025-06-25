import os

class Config:
    JWT_SECRET_KEY = 'enforma_super_secreto'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:santy300406@localhost:5432/enforma_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
