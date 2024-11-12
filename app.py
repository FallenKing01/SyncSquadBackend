
from flask import Flask
from Domain.extensions import api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Controllers.accountsController import nsUser
from Controllers.studentsController import nsStudent
from Controllers.professorsController import nsProfessor
from Controllers.secretariatController import nsSecretariat

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'cookiemonster'
jwt = JWTManager(app)
api.init_app(app)
CORS(app)
api.add_namespace(nsUser)
api.add_namespace(nsStudent)
api.add_namespace(nsProfessor)
api.add_namespace(nsSecretariat)

if __name__ == "__main__":
    app.run(debug=True)