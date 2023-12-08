from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
import re
from datetime import datetime
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Student(db.Model, SerializerMixin):
    __tablename__ = "student_table"
    serialize_rules = ["-enrollments.student"]
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    grad_year = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="student",cascade="all, delete-orphan")
    courses = association_proxy("enrollments", "course")

    @validates('grad_year')
    def validate_grad_year(self, key: int, value: int):
        
        current_date = 2023
        
        if not value >= current_date:
            raise ValueError('Grad year must be {current_date} or later.')
        else:
            return current_date

class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollment_table"

    serialize_rules = ["-student.enrollments", "-course.enrollments"]
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student_table.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course_table.id"), nullable=False)
    term = db.Column(db.String, nullable=False)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    @validates('term')
    def validate_term(self, key: str, term: str):
        #check the first characters
        # if term.startswith('F') or term.startswith('S'):
        #     print('startwith worked')
        #     #check that the rest of the characters are numbers
        #     year = term[1:]
        #     print(year)
        #     if year.isdecimal() and len(year) == 4:
        #         return term
        # raise ValueError("bad term value")
            
        pattern = re.compile(r'(?P<term>[FS]{1})(?P<year>[0-9]{4})')
        
        # pattern = '[A-Z]{1}[0-9]{4}'
        # if not re.match(pattern, value):
        #     raise ValueError('values must be formatted as a capital letter followed by four integers')
        # else:
        #     return value
        
        match = pattern.search(term)

        if match:
            year_group = match.group('year')
            current_year = datetime.now().year

            if int(year_group) >= current_year:
                return term
            else:
                raise ValueError('Term year must be four digits long and equal to this year or later.')
        else:
            raise ValueError('Term must be formated as: capital F,S,W and a four digit year.')


class Course(db.Model, SerializerMixin):
    __tablename__ = "course_table"

    serialize_rules = ["-enrollments.course"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    instructor = db.Column(db.String)
    credits = db.Column(db.Integer, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="course",cascade="all, delete-orphan")
    students = association_proxy("enrollments", "student")

    @validates('title')
    def validate_title(self, key: str, value: str):
        if not value:
            raise ValueError('A title is required.')
        else:
            return value