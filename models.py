import os
from flask_sqlalchemy import SQLAlchemy




db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name=db.Column(db.String)


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code= db.Column(db.String, nullable=False, unique=True)
    course_name = db.Column(db.String, nullable=False)
    course_description=db.Column(db.String)
    enrolled_students=db.relationship("Student",secondary="enrollment")

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"),nullable=False)
    ecourse_id = db.Column(db.String, db.ForeignKey("course.course_id"),nullable=False)
    