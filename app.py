
from flask import Flask
from Domain.extensions import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Infrastructure.Repositories.userRepo import get_user_by_id_repo
from Controllers.accountsController import nsUser
from Controllers.studentsController import nsStudent
from Controllers.professorsController import nsProfessor
from Controllers.secretariatController import nsSecretariat
from Controllers.materiiController import nsMaterii
from Controllers.asistentiController import nsAsistenti
from Controllers.saliController import nsSali
from Controllers.examenController import nsExamen
from Controllers.loginController import nsLogin
from Controllers.databaserelatedController import nsDatabase
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'cookiemonster'
jwt = JWTManager(app)
api.init_app(app)
CORS(app)

api.add_namespace(nsUser)
api.add_namespace(nsLogin)
api.add_namespace(nsStudent)
api.add_namespace(nsProfessor)
api.add_namespace(nsSecretariat)
api.add_namespace(nsMaterii)
api.add_namespace(nsAsistenti)
api.add_namespace(nsSali)
api.add_namespace(nsExamen)
api.add_namespace(nsDatabase)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user["id"]


# JWT User Lookup Callback
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data["sub"]

    user = get_user_by_id_repo(identity)
    return user

if __name__ == "__main__":
    app.run(debug=True)