from flask_restx import fields
from Domain.extensions import api

createGrupa = api.model('Create Grupa', {
    "nume": fields.String(required=True, description="Group name"),
})