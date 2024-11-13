from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api
from Infrastructure.Repositories.materiiRepo import *

nsMaterii = Namespace("materii", description="Materii related operations")

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