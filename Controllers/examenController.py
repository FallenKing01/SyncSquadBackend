from flask_restx import Namespace, Resource
from flask_restx import abort
from Domain.extensions import api,authorizations
from Infrastructure.Repositories.examRepo import *
from Models.Expect.createExamenExpect import *

nsExamen = Namespace("examen", description="Examen related operations",authorizations=authorizations)


@nsExamen.route("/programaeazastudent")
class createExamen(Resource):
    @nsExamen.expect(createStudentExamene)
    def post(self):

        try:

            message = create_examen_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsExamen.route("/<string:profesorId>")
class getExamen(Resource):
    def get(self, profesorId):

        try:

            examene = get_pending_exams_of_profesor_repo(profesorId)

            return examene

        except Exception:

            abort(500, "Something went wrong")

@nsExamen.route("/programate/<string:profesorId>")
class getExameneProgramate(Resource):
    def get(self, profesorId):

        try:

            examene = get_approved_exams_of_profesor_repo(profesorId)

            return examene

        except Exception:

            abort(500, "Something went wrong")

@nsExamen.route("")
class updateExamen(Resource):
    @nsExamen.expect(updateExamen)
    def put(self):

        try:

            update_examen_repo(api.payload)

            return {"message": "Examen updated successfully"}

        except Exception:

            abort(500, "Something went wrong")
