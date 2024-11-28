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
    "orastart": fields.String(required=False, description="Start time of the exam (HH:mm)"),
    "orafinal": fields.String(required=False, description="End time of the exam (HH:mm)"),
    "actualizatde": fields.String(required=False, description="ID of the user who last updated the exam"),
    "salaid": fields.String(required=True, description="ID of the room where the exam will take place"),
})


updateExamen = api.model('Reprogrameaza examen', {
    "id": fields.String(required=True, description="ID of the exam"),
    "asistentid": fields.String(required=False, description="ID of the assistant for the exam"),
    "orastart": fields.String(required=False, description="Start time of the exam"),
    "orafinal": fields.String(required=False, description="End time of the exam"),
    "actualizatde": fields.String(required=False, description="ID of the user who last updated the exam"),
    "salaid": fields.String(required=True, description="ID of the room where the exam will take place"),
    "data": fields.Date(required=False, description="Date of the exam"),
    "sefid": fields.String(required=True, description="ID of the chief examiner"),
    "motiv": fields.String(required=False, description="Reason for declining the exam"),

})

declineExamen = api.model('Decline Examene', {

    "motiv": fields.String(required=True, description="Reason for declining the exam"),
})

createExamenFortat = api.model('Create Examene Fortat', {
    "profesorid": fields.String(required=True, description="ID of the professor in charge of the exam"),
    "grupaid": fields.String(required=True, description="ID of the chief examiner"),
    "materieid": fields.String(required=False, description="ID of the subject"),
    "data": fields.Date(required=False, description="Date of the exam"),
    "asistentid": fields.String(required=False, description="ID of the assistant for the exam"),
    "orastart": fields.String(required=False, description="Start time of the exam"),
    "orafinal": fields.String(required=False, description="End time of the exam"),
    "actualizatde": fields.String(required=False, description="ID of the user who last updated the exam"),
    "salaid": fields.String(required=True, description="ID of the room where the exam will take place"),
})

asistentDisponibil = api.model('Asistent Disponibil', {
    "profesorid": fields.String(required=True, description="ID of the professor"),
    "data": fields.Date(required=True, description="Date of the exam"),
    "orastart": fields.String(required=True, description="Start time of the exam"),
    "orafinal": fields.String(required=True, description="End time of the exam"),
})
