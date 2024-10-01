from flask_restx import fields
from Domain.extensions import api

accountExpect = api.model('AccountExpect', {
    "nume": fields.String,
    "prenume" : fields.String,
    "password" : fields.String,
})