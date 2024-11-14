from flask_restx import fields
from Domain.extensions import api

createStudentExamene = api.model('Create Examene', {
    "profesorid": fields.String(required=True, description="ID of the professor in charge of the exam"),
    "sefid": fields.String(required=True, description="ID of the chief examiner"),
    "materieid": fields.String(required=False, description="ID of the subject"),
    "data": fields.Date(required=False, description="Date of the exam"),
})

acceptProfesorExamene = api.model('Update Examene', {
    "id": fields.String(required=True, description="ID of the exam"),
    "asistentid": fields.String(required=False, description="ID of the assistant for the exam"),
    "orastart": fields.DateTime(required=False, description="Start time of the exam"),
    "orafinal": fields.DateTime(required=False, description="End time of the exam"),
    "actualizatde": fields.String(required=False, description="ID of the user who last updated the exam"),
    "actualizatla": fields.Date(required=True, description="Date when the exam was last updated"),
    "salaid": fields.String(required=True, description="ID of the room where the exam will take place"),

})

