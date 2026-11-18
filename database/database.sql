CREATE DATABASE IF NOT EXISTS student_performance_db;

USE student_performance_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'faculty') DEFAULT 'student'
);

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(30) UNIQUE NOT NULL,
    course VARCHAR(100),
    semester INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS academic_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    attendance FLOAT DEFAULT 0,
    previous_marks FLOAT DEFAULT 0,
    study_hours FLOAT DEFAULT 0,
    assignment_score FLOAT DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    predicted_performance VARCHAR(30),
    risk_level VARCHAR(30),
    FOREIGN KEY (student_id) REFERENCES students(id)
);