from flask_restx import fields
from Domain.extensions import api

accountStudentExpect= api.model('CreateStudent', {
    "nume": fields.String,
    "email": fields.String,
    "parola" : fields.String,
    "telefon" : fields.String,
    "facultatea" : fields.String,
    "specializarea" : fields.String,
    "idgrupa" : fields.String,
})


accountProfesorExpect = api.model('AccountExpect', {
    "nume": fields.String,
    "email": fields.String,
    "parola" : fields.String,
    "telefon" : fields.String,
    "departament" : fields.String,
})

accountSecretarExpect = api.model('AccountExpect', {
    "email": fields.String,
    "parola": fields.String,
    "nume": fields.String,
    "telefon" : fields.String,
})