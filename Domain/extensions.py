from flask_restx import Api
import bcrypt
# vezi daca da eroare la bcrypt

salt = bcrypt.gensalt()
api = Api()

