
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Student, AcademicRecord, Prediction
from predict import predict_performance
from suggestions import get_suggestions

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


# Login Protection
@app.before_request
def require_login():

    public_pages = ["login", "register", "static"]

    if request.endpoint in public_pages:
        return

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("user_role") == "student":

        student_allowed_pages = [
            "home",
            "student_dashboard",
            "logout"
        ]

        if request.endpoint not in student_allowed_pages:
            flash("You do not have permission to access this page.")
            return redirect(url_for("student_dashboard"))


# Registration
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        roll_number = request.form.get("roll_number", "").strip()

        if role not in ["student", "faculty"]:
            flash("Invalid account type.")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.")
            return redirect(url_for("register"))

        student_record = None

        if role == "student":

            if not roll_number:
                flash("Please enter your student roll number.")
                return redirect(url_for("register"))

            student_record = Student.query.filter_by(
                roll_number=roll_number
            ).first()

            if not student_record:
                flash("Student roll number not found. Contact faculty.")
                return redirect(url_for("register"))

            if student_record.user_id is not None:
                flash("This student roll number is already registered.")
                return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(user)

        if role == "student":
            db.session.flush()
            student_record.user_id = user.id

        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session.clear()
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role

            if user.role == "student":
                return redirect(url_for("student_dashboard"))

            return redirect(url_for("home"))

        flash("Invalid email or password.")

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


# Faculty Dashboard
@app.route("/")
def home():

    if session.get("user_role") == "student":
        return redirect(url_for("student_dashboard"))

    total_students = Student.query.count()
    total_records = AcademicRecord.query.count()
    total_predictions = Prediction.query.count()

    high_risk_students = Prediction.query.filter_by(
        risk_level="High"
    ).count()

    excellent_count = Prediction.query.filter_by(
        predicted_performance="Excellent"
    ).count()

    good_count = Prediction.query.filter_by(
        predicted_performance="Good"
    ).count()

    average_count = Prediction.query.filter_by(
        predicted_performance="Average"
    ).count()

    poor_count = Prediction.query.filter_by(
        predicted_performance="Poor"
    ).count()

    medium_risk = Prediction.query.filter_by(
        risk_level="Medium"
    ).count()

    low_risk = Prediction.query.filter_by(
        risk_level="Low"
    ).count()

    return render_template(
        "index.html",
        total_students=total_students,
        total_records=total_records,
        total_predictions=total_predictions,
        high_risk_students=high_risk_students,
        excellent_count=excellent_count,
        good_count=good_count,
        average_count=average_count,
        poor_count=poor_count,
        medium_risk=medium_risk,
        low_risk=low_risk
    )


# Student Dashboard
@app.route("/student_dashboard")
def student_dashboard():

    student = Student.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if not student:
        return "Student record not found. Please contact faculty."

    records = AcademicRecord.query.filter_by(
        student_id=student.id
    ).all()

    predictions = Prediction.query.filter_by(
        student_id=student.id
    ).all()

    return render_template(
        "student_dashboard.html",
        student=student,
        records=records,
        predictions=predictions
    )


# Add Student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        student = Student(
            name=request.form["name"],
            roll_number=request.form["roll_number"],
            course=request.form["course"],
            semester=request.form["semester"]
        )

        db.session.add(student)
        db.session.commit()

        return "Student Added Successfully!"

    return render_template("add_student.html")


# View Students
@app.route("/view_students")
def view_students():

    students = Student.query.all()

    return render_template(
        "view_students.html",
        students=students
    )


# Add Academic Records
@app.route("/academic_records", methods=["GET", "POST"])
def academic_records():

    students = Student.query.all()

    if request.method == "POST":

        record = AcademicRecord(
            student_id=request.form["student_id"],
            attendance=request.form["attendance"],
            previous_marks=request.form["previous_marks"],
            study_hours=request.form["study_hours"],
            assignment_score=request.form["assignment_score"]
        )

        db.session.add(record)
        db.session.commit()

        return "Academic Record Saved Successfully!"

    return render_template(
        "academic_records.html",
        students=students
    )


# View Academic Records
@app.route("/view_academic_records")
def view_academic_records():

    records = AcademicRecord.query.all()

    return render_template(
        "view_academic_records.html",
        records=records
    )


# Predict Performance
@app.route("/predict", methods=["GET", "POST"])
def predict_student():

    students = Student.query.all()

    if request.method == "POST":

        student_id = request.form["student_id"]
        attendance = float(request.form["attendance"])
        previous_marks = float(request.form["previous_marks"])
        study_hours = float(request.form["study_hours"])
        assignment_score = float(request.form["assignment_score"])

        result = predict_performance(
            attendance,
            previous_marks,
            study_hours,
            assignment_score
        )

        suggestions = get_suggestions(
            attendance,
            previous_marks,
            study_hours,
            assignment_score
        )

        if result == "Poor":
            risk_level = "High"
        elif result == "Average":
            risk_level = "Medium"
        else:
            risk_level = "Low"

        prediction = Prediction(
            student_id=student_id,
            predicted_performance=result,
            risk_level=risk_level
        )

        db.session.add(prediction)
        db.session.commit()

        return render_template(
            "predict.html",
            students=students,
            result=result,
            risk_level=risk_level,
            suggestions=suggestions
        )

    return render_template(
        "predict.html",
        students=students,
        result=None,
        risk_level=None,
        suggestions=None
    )


# Prediction History
@app.route("/prediction_history")
def prediction_history():

    predictions = Prediction.query.all()

    return render_template(
        "prediction_history.html",
        predictions=predictions
    )


# Run Application
if __name__ == "__main__":
    app.run(debug=True)
