from Infrastructure.Repositories.grupaRepo import *
from flask_restx import Namespace, Resource
from flask_restx import abort
from Domain.extensions import authorizations,api
from Models.Expect.grupaExpect import createGrupa

nsGrupe = Namespace("grupe", description="Grupe related operations",authorizations=authorizations)

@nsGrupe.route("/new")
class createGrupa(Resource):
    @nsGrupe.doc(description="Create a group")
    @nsGrupe.expect(createGrupa)
    def post(self):

        try:

            data = api.payload

            grupa = create_grupa_repo(data)

            return grupa

        except Exception:

            abort(500, "Something went wrong")

@nsGrupe.route("")
class getGrupe(Resource):
    @nsGrupe.doc(description="Get all the groups")
    def get(self):

        try:

            grupe = get_grupe_from_repo()

            return grupe

        except Exception:

            abort(500, "Something went wrong")

@nsGrupe.route("/<string:nume>")
class getGrupeDupaNume(Resource):
    @nsGrupe.doc(description="Get the groups by name")
    def get(self,nume):

        try:

            grupe = get_grupa_dupa_nume(nume)

            return grupe

        except Exception:

            abort(500, "Something went wrong")




