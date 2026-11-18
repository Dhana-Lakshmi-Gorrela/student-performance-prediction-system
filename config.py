from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = "student_performance_secret_key"

    DB_USER = "student_app"
    DB_PASSWORD = "DhanaNew@2026" 
    DB_HOST = "localhost"
    DB_NAME = "student_performance_db"

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:"
        f"{quote_plus(DB_PASSWORD)}@{DB_HOST}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
