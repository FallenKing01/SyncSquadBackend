from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.accountsExpect import accountExpect
from Domain.extensions import api
from Infrastructure.Repositories.userRepo import *



nsUser = Namespace("user", description="User related operations")
@nsUser.route("/create")
class userCreate(Resource):

    @nsUser.expect(accountExpect)
    def post(self):
        try:
            insertedId=create_user_repo(api.payload)

            return insertedId, 201

        except Exception:
            abort(500, "Something went wrong")

@nsUser.route("/")
class getUsersFromDb(Resource):
    def get(self):

        try:

            user_data = get_users_repo()
            return user_data, 200

        except Exception as e:
            abort(404, str(e))