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

@nsProfessor.route("/profesororar/<string:prof_id>/<string:data>")
class getOrar(Resource):

    def get(self,prof_id,data):

        try:

            orar = get_orar_of_prof_repo(prof_id,data)

            return orar

        except Exception:

            abort(500, "Something went wrong")

@nsProfessor.route("/profesoriancurent/<string:grupa_id>")
class getExamene(Resource):

    def get(self,grupa_id):

        try:

            examene = get_profesori_from_api(grupa_id)

            return examene

        except Exception:

            abort(500, "Something went wrong")