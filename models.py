from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("student", "faculty"),
        default="student"
    )
# Student Model
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(30), unique=True, nullable=False)
    course = db.Column(db.String(100))
    semester = db.Column(db.Integer)

# Academic Record Model
class AcademicRecord(db.Model):
    __tablename__ = "academic_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    attendance = db.Column(db.Float, default=0)
    previous_marks = db.Column(db.Float, default=0)
    study_hours = db.Column(db.Float, default=0)
    assignment_score = db.Column(db.Float, default=0)

# Prediction Model
class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )
    predicted_performance = db.Column(db.String(30))
    risk_level = db.Column(db.String(30))
