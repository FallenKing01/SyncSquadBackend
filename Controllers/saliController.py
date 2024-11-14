from flask_restx import Namespace, Resource
from flask_restx import abort
from pyexpat.errors import messages

from Domain.extensions import api,authorizations
from Infrastructure.Repositories.saliRepo import *
from Models.Expect.createSaliExpect import *
from flask_jwt_extended import jwt_required

nsSali = Namespace("sali", description="Sali related operations",authorizations=authorizations)

@nsSali.route("")
class createSala(Resource):
    method_decorators = [jwt_required()]
    @nsSali.doc(security="jsonWebToken")
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

@nsSali.route("/<string:sala_id>/<string:data_examen>")
class getLiberSala(Resource):
    def get(self, sala_id, data_examen):

        try:

            liber = get_liber_sala(sala_id, data_examen)

            return liber

        except Exception:

            abort(500, "Something went wrong")

@nsSali.route("/<string:sala_id>")
class deleteSala(Resource):
    def delete(self, sala_id):

        try:

            message = delete_sala_repo(sala_id)

            return message

        except Exception:

            abort(500, "Something went wrong")

