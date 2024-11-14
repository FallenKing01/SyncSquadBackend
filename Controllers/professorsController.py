from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.createExamenExpect import *
from Domain.extensions import api,authorizations
from Infrastructure.Repositories.professorRepo import *

nsProfessor = Namespace("profesor", description="Professor related operations",authorizations=authorizations)


@nsProfessor.route("")
class getProfesori(Resource):

    def get(self):

        try:

            profesori = get_profesori_repo()

            return profesori

        except Exception:

            abort(500, "Something went wrong")
@nsProfessor.route("/acceptaexamen")
class acceptExamen(Resource):

    @nsProfessor.expect(acceptProfesorExamene)
    def put(self):

        try:

            accept_examen_by_profesor_repo(api.payload)

            return {"message": "Examen accepted successfully"}

        except Exception:

            abort(500, "Something went wrong")
