from flask_restx import Namespace, Resource
from flask_restx import abort
from Models.Expect.accountsExpect import *
from Domain.extensions import api,authorizations
from Infrastructure.Repositories.userRepo import *



nsUser = Namespace("user", description="User related operations" , authorizations=authorizations)
@nsUser.route("/student")
class createStudent(Resource):
    @nsUser.expect(accountStudentExpect)
    def post(self):

        try:

            message = create_student_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsUser.route("/profesor")
class createProfesor(Resource):
    @nsUser.expect(accountProfesorExpect)
    def post(self):

        try:

            message = create_profesor_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsUser.route("/secretar")
class createSecretar(Resource):
    @nsUser.expect(accountSecretarExpect)
    def post(self):

        try:

            message = create_secretar_repo(api.payload)

            return message

        except Exception:

            abort(500, "Something went wrong")

@nsUser.route("/info/<string:id>")
class getUserInfo(Resource):
    def get(self, id):

        try:

            user_data = get_info_user_repo(id)

            return user_data, 200

        except Exception as e:

            abort(204, str(e))


@nsUser.route("")
class getUsersFromDb(Resource):
    def get(self):

        try:

            user_data = get_users_repo()
            return user_data, 200

        except Exception as e:

            abort(204, str(e))


