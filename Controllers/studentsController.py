from Infrastructure.Repositories.studentRepo import *
from flask_restx import Namespace, Resource
from flask_restx import abort
from Domain.extensions import authorizations,api
nsStudent = Namespace("student", description="Student related operations",authorizations=authorizations)


@nsStudent.route("/promovare/<string:grupaId>/<string:studentId>")
class updateStudent(Resource):
    @nsStudent.doc(description="Update student status.Send the id of the group and the id of the student and the student will be promoted to the group leader and the last one will be demoted")
    def put(self, grupaId ,studentId):

        try:

            message = update_student(grupaId,studentId)

            return message

        except Exception:

            abort(500, "Something went wrong")

