from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api
from Infrastructure.Repositories.professorRepo import *

nsProfessor = Namespace("professor", description="Professor related operations")

@nsProfessor.route("/creatematerie")
class create_materie(Resource):
    @nsProfessor.expect(materiiExpect)
    def post(self):

        try:

            message = create_subject_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")
@nsProfessor.route("/getmaterii/<string:profesorId>")
class get_materii(Resource):
    def get(self, profesorId):

        try:

            subjects = get_subjects_of_profesor_repo(profesorId)

            return subjects

        except Exception:

            abort(500, "Something went wrong")

@nsProfessor.route("/createasistent/<string:titularId>/<string:asistentId>")
class create_asistent(Resource):
    def post(self,titularId,asistentId):
        try:

            message = create_asistent_repo(titularId , asistentId)

            return message

        except Exception:
            abort(500, "Something went wrong")
@nsProfessor.route("/getasistenti/<string:profesorId>")
class get_asistenti(Resource):
    def get(self, profesorId):

        try:

            assistants = get_asistenti_of_profesor_repo(profesorId)

            return assistants

        except Exception:

            abort(500, "Something went wrong")
