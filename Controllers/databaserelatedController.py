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

@nsDatabase.route("/generatepdf")
class generatePdf(Resource):
    def get(self):
        try:

            generate_pdf_secretariat_repo()

            return {"message": "PDF generated successfully!"}

        except Exception:

            abort(500, "Something went wrong")

@nsDatabase.route("/addgroups")
class addgroups(Resource):

    def post(self):

        try:

            insert_grupe_repo()

            return {"message":"Grupele au fost adaugate cu succes"}

        except Exception:

            abort(500, "Something went wrong")
