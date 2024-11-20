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

@nsExamen.route("/grupaexamene/<string:grupaId>")
class getExamenByGrupa(Resource):
    def get(self, grupaId):

        try:

            examene = get_examene_grupa_repo(grupaId)

            return examene

        except Exception:

            abort(500, "Something went wrong")

@nsExamen.route("/studentdupastare/<string:studentId>/<string:stare>")
class getExamenByStare(Resource):
    def get(self, studentId, stare):

        try:

            examene = get_examene_sef_semigrupa_stare(studentId, stare)

            return examene

        except Exception:

            abort(500, "Something went wrong")
