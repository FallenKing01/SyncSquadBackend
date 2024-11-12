from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.createGrupaExpect import *
from Domain.extensions import api
from Infrastructure.Repositories.secretariatRepo import *

nsSecretariat = Namespace("secretariat", description="Secretariat related operations")

@nsSecretariat.route("/creategroup")
class create_group(Resource):
    @nsSecretariat.expect(createGrupaExpect)
    def post(self):

        try:

            message = create_grupa_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsSecretariat.route("/getstudentsfromgroup/<string:grupaId>")
class get_students_from_group(Resource):
    def get(self, grupaId):

        try:

            students = get_students_of_group_repo(grupaId)

            return students

        except Exception:

            abort(500, "Something went wrong")