from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api
from Infrastructure.Repositories.asistentiRepo import *

nsAsistenti = Namespace("asistenti", description="Asistenti related operations")


@nsAsistenti.route("/<string:titularId>/<string:asistentId>")
class create_asistent(Resource):
    def post(self,titularId,asistentId):

        try:

            message = create_asistent_repo(titularId , asistentId)

            return message

        except Exception:

            abort(500, "Something went wrong")
@nsAsistenti.route("/<string:profesorId>")
class get_asistenti(Resource):
    def get(self, profesorId):

        try:

            assistants = get_asistenti_of_profesor_repo(profesorId)

            return assistants

        except Exception:

            abort(500, "Something went wrong")