import uuid
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.extensions import session

def add_examen_repo(exam_data):


    exam = Examene(Id=exam_data["id"],SefId=exam_data["sefid"],ProfesorId=exam_data["profesorid"], MaterieId=exam_data["materieid"], Data=exam_data["data"],Starea=Status.PENDING.name.lower())
    session.add(exam)

def create_examen_repo(exam_data):

    id = str(uuid.uuid4())

    try:

        exam_data["id"] = id

        add_examen_repo(exam_data)
        session.commit()

        return {"message": "Exam added successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while inserting exam: {str(e)}")