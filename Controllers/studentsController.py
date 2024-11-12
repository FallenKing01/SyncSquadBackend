from Infrastructure.Repositories.studentRepo import *
from flask_restx import Namespace, Resource
from flask_restx import abort

nsStudent = Namespace("student", description="Student related operations")


@nsStudent.route("/update/<string:studentId>")
class updateStudent(Resource):
    def put(self, studentId):

        try:

            message = update_student(studentId)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsStudent.route("/profesori")
class getProfesori(Resource):

    def get(self):

        try:

            profesori = get_profesori()

            return profesori

        except Exception:

            abort(500, "Something went wrong")
