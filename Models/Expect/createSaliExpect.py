from flask_restx import fields
from Domain.extensions import api

createSali = api.model('Create Sali', {
    "nume": fields.String(required=True, description="Name of the room"),
    "departament": fields.String(required=True, description="Department to which the room belongs"),
})
