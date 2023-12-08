from flask import make_response, jsonify, request, g
from flask import Flask
from models import db, Student, Course, Enrollment

from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def root():
    return "<h1>Registrar</h1>"


@app.get("/students")
def get_students():
    students = Student.query.all()
    if not students:
        return make_response(jsonify({"error": "students not found"}), 404)
    data = [student.to_dict(rules=("-enrollments",)) for student in students]
    return make_response(jsonify(data), 200)


@app.get("/students/<int:id>")
def get_student_by_id(id: int):
    student = db.session.get(Student, id)
    if not student:
        return make_response(jsonify({"error": f"student id {id} not found"}))
    # or: student = Student.query.filter(Student.id == id).first()

    return make_response(jsonify(student.to_dict()), 200)


def patch_student(id: int):
    student = db.session.get(Student, id)
    if not student:
        return make_response(jsonify({"error": f"student id {id} not found"}), 404)
    try:
        patch_data = request.json
        for key in patch_data:
            setattr(student, key, patch_data[key])
        db.session.add(student)
        db.session.commit()
        return make_response(jsonify(student.to_dict()), 200)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": f"application threw error: {e}"}), 405)





@app.patch("/courses/<int:id>")
def patch_course(id: int):
    course = db.session.get(Course, id)
    if not course:
        return make_response(jsonify({"error": f"course id {id} not found"}), 404)
    try:
        course_patch:dict = request.get_json()

        for key in course_patch:
            setattr(course, key, course_patch[key])

        db.session.add(course)
        db.session.commit()

        return make_response(jsonify(course.to_dict(rules=["-enrollments"])), 200)
    except Exception as e:
        return make_response(
            jsonify({"error": f"Error {e} occurred when trying to update course."})
        )


@app.delete("/students/<int:id>")
def delete_student(id: int):
    student = db.session.get(Student, id)
    if not student:
        return make_response(jsonify({"error": f"student id {id} not found"}), 400)
    db.session.delete(student)
    db.session.commit()

    return make_response(jsonify({}), 200)


@app.get("/students/<int:student_id>/courses")
def get_courses_for_student(student_id: int):
    student = db.session.get(Student, student_id)
    if not student:
        return make_response(
            jsonify({"error": f"student id {student_id} not found"}), 404
        )
    # courses = [e.course.to_dict() for e in student.enrollments]
    courses = [c.to_dict(rules=["-enrollments"]) for c in student.courses]
    return make_response(jsonify(courses), 200)


@app.post("/enrollments")
def enroll_student():
    # get the data from the enrollment
    request_data = request.get_json()
    # print(request_data)
    student = db.session.get(Student, request_data.get("student_id"))
    if not student:
        return make_response(jsonify({"error": f"student id not found"}), 404)

    course = db.session.get(Course, request_data.get("course_id"))
    if not course:
        return make_response(jsonify({"error": f"course id not found"}), 404)
    try:
        new_enrollment = Enrollment(
            student_id=student.id,
            course_id=request_data.get("course_id"),
            term=request_data.get("term"),
        )


        db.session.add(new_enrollment)
        db.session.commit()

        return make_response(jsonify(new_enrollment), 200)
    except Exception as e:
        print(f"error on line 124 {e}")
        return make_response(jsonify({"error":f"{e}"}),405)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
