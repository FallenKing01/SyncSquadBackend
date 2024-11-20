from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api,authorizations
from Infrastructure.Repositories.materiiRepo import *

nsMaterii = Namespace("materii", description="Materii related operations",authorizations=authorizations)

@nsMaterii.route("")
class create_materie(Resource):
    @nsMaterii.expect(materiiExpect)
    def post(self):

        try:

            message = create_subject_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsMaterii.route("/<string:profesorId>")
class get_materii(Resource):
    def get(self, profesorId):

        try:

            subjects = get_subjects_of_profesor_repo(profesorId)

            return subjects

        except Exception:

            abort(500, "Something went wrong")

@nsMaterii.route("/<string:idMaterie>")
class delete_materie(Resource):
    def delete(self,idMaterie):

        try:

            message = delete_subject_repo(idMaterie)

            print(message)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsMaterii.route("/<string:idMaterie>")
class update_materie(Resource):
    @nsMaterii.expect(materiiExpect)  # Validează payload-ul primit
    def put(self, idMaterie):
        try:
            # Apelează funcția de actualizare din repository
            message = update_subject_repo(idMaterie, api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsMaterii.route("/studentmateriifaraexamen/<string:profesorId>/<string:studentId>")
class get_materii_fara_examen(Resource):
    def get(self, profesorId, studentId):

        try:

            subjects = get_materii_examene_neprogramate_repo(profesorId,studentId)

            return subjects

        except Exception:

            abort(500, "Something went wrong")