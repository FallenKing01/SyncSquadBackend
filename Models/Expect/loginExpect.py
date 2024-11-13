from flask_restx import fields
from Domain.extensions import api

loginExpect = api.model('LoginExpect', {
    "username": fields.String,
    "parola": fields.String,
})