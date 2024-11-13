from flask_restx import Namespace, Resource
from flask_restx import abort
from Domain.extensions import api
from Infrastructure.Repositories.saliRepo import *
from Models.Expect.createSaliExpect import *
nsSali = Namespace("sali", description="Sali related operations")

@nsSali.route("")
class createSala(Resource):
    @nsSali.expect(createSali)
    def post(self):

        try:

            message = create_sali_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsSali.route("/<string:departament_name>")
class getSaliFromDepartment(Resource):
    def get(self, departament_name):

        try:

            sali = get_sali_from_department_repo(departament_name)

            return sali

        except Exception:

            abort(500, "Something went wrong")