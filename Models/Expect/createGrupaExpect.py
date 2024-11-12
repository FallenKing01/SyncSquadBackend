from flask_restx import fields
from Domain.extensions import api

createGrupaExpect = api.model('Create grupa', {
    "grupa": fields.String(required=True, description="Name of the group"),
})
