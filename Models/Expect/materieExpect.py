from flask_restx import fields
from Domain.extensions import api

materiiExpect = api.model('Create subject', {
    "nume": fields.String(required=True, description="Name of the subject"),
    "abreviere": fields.String(required=True, description="Abbreviation of the subject"),
    "tipevaluare": fields.String(required=True, description="Type of evaluation (e.g., Exam, Quiz)"),
    "numarcredite": fields.Integer(required=True, description="Number of credits for the subject"),
    "profesorid": fields.String(required=True, description="Name of the professor in charge"),
})
