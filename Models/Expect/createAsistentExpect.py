from flask_restx import fields
from Domain.extensions import api

createAsistent = api.model('Create Asistent', {
    "idprof": fields.String(required=True, description="ID of the professor associated with the assistant"),
    "idasistent": fields.String(required=True, description="ID of the assistant"),
})