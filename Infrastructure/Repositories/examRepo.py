import uuid
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.extensions import session
from Domain.Entities.materie import Materii
from datetime import datetime

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


from datetime import datetime, date

def get_pending_exams_of_profesor_repo(profesorId):
    try:
        exams = session.query(Examene).filter(
            Examene.profesorid == profesorId,
            Examene.starea == Status.PENDING.name.lower()
        ).all()

        examList = []
        for exam in exams:
            materia = session.query(Materii).filter(Materii.id == exam.materieid).first()

            materiaToAdd = {
                "id": materia.id,
                "nume": materia.nume,
                "credite": materia.numarcredite,
                "abreviere": materia.abreviere,
                "tipevaluare": materia.tipevaluare,
            }

            if isinstance(exam.data, (datetime, date)):

                data_serialized = exam.data.strftime("%Y-%m-%d")

            else:

                data_serialized = exam.data

            examList.append({
                "id": exam.id,
                "sefid": exam.sefid,
                "profesorid": exam.profesorid,
                "materie": materiaToAdd,
                "data": data_serialized,
                "starea": exam.starea
            })

        return examList, 200

    except Exception as e:
        raise Exception(f"Error while getting exams: {str(e)}")
