from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.materieExpect import *
from Domain.extensions import api
from Infrastructure.Repositories.professorRepo import *

nsProfessor = Namespace("profesor", description="Professor related operations")


@nsProfessor.route("")
class getProfesori(Resource):

    def get(self):

        try:

            profesori = get_profesori_repo()

            return profesori

        except Exception:

            abort(500, "Something went wrong")

