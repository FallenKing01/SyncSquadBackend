
from flask import Flask
from Domain.extensions import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Controllers.accountsController import nsUser
from Controllers.studentsController import nsStudent
from Controllers.professorsController import nsProfessor
from Controllers.secretariatController import nsSecretariat
from Controllers.materiiController import nsMaterii
from Controllers.asistentiController import nsAsistenti
from Controllers.saliController import nsSali
from Controllers.examenController import nsExamen
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cookiemonster'
jwt = JWTManager(app)
api.init_app(app)
CORS(app)
api.add_namespace(nsUser)
api.add_namespace(nsStudent)
api.add_namespace(nsProfessor)
api.add_namespace(nsSecretariat)
api.add_namespace(nsMaterii)
api.add_namespace(nsAsistenti)
api.add_namespace(nsSali)
api.add_namespace(nsExamen)

if __name__ == "__main__":
    app.run(debug=True)