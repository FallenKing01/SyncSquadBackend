from flask_restx import Namespace, Resource
from flask_restx import abort
from Infrastructure.Repositories.loginRepo import *
from Models.Expect.loginExpect import *
nsLogin= Namespace("login", description="Login")

@nsLogin.route("")

class login(Resource):
    @nsLogin.expect(loginExpect)
    def post(self):

        try:

            message = login_user(api.payload)
            return message

        except Exception:
            abort(500, "Something went wrong")

