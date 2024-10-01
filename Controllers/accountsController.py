from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.accountsExpect import accountExpect
from Domain.extensions import api
from Infrastructure.Repositories.userRepo import createUserRepo



nsUser = Namespace("user", description="User related operations")
@nsUser.route("/create")
class userCreate(Resource):

    @nsUser.expect(accountExpect)
    def post(self):
        try:
            insertedId=createUserRepo(api.payload)

            return insertedId, 201

        except Exception:
            abort(500, "Something went wrong")