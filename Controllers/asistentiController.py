from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api,authorizations
from Infrastructure.Repositories.asistentiRepo import *

nsAsistenti = Namespace("asistenti", description="Asistenti related operations",authorizations=authorizations)


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

@nsAsistenti.route("/<string:asistent_id>/<string:profesor_id>")
class DeleteAsistent(Resource):
    def delete(self, asistent_id, profesor_id):

        try:


            message = delete_asistent_repo(asistent_id, profesor_id)

            return message, 200

        except Exception as e:

            abort(500, f"Something went wrong: {str(e)}")