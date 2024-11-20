from flask_restx import Namespace, Resource
from flask_restx import abort
from pyexpat.errors import messages
from Domain.extensions import api
from Infrastructure.Repositories.saliRepo import *
from Models.Expect.createSaliExpect import *
from Infrastructure.Repositories.databaseRepo import *
nsDatabase = Namespace("database", description="Database related operations")

@nsDatabase.route("/insert/sali")
class insertSali(Resource):
    def post(self):
        try:
            insert_database_sali_from_api_repo()
            return {"message": "Sali inserted successfully!"}
        except Exception:
            abort(500, "Something went wrong")

@nsDatabase.route("/insert/profesori")
class insertProfesori(Resource):
    def post(self):
        try:
            insert_profesori_from_api_repo()
            return {"message": "Profesori inserted successfully!"}
        except Exception:
            abort(500, "Something went wrong")
