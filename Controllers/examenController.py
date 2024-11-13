from flask_restx import Namespace, Resource
from flask_restx import abort
from Domain.extensions import api
from Infrastructure.Repositories.examRepo import *
from Models.Expect.createExamenExpect import *

nsExamen = Namespace("examen", description="Examen related operations")


@nsExamen.route("")
class createExamen(Resource):
    @nsExamen.expect(createStudentExamene)
    def post(self):

        try:

            message = create_examen_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")