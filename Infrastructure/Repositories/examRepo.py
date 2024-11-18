import uuid
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.extensions import session
from Domain.Entities.materie import Materii
from datetime import datetime,timedelta
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.saliCereri import SaliCereri
from Domain.Entities.student import Student
from Domain.Entities.grupa import Grupe
from datetime import datetime, date

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

            sef = session.query(Student).filter(Student.id == exam.sefid).first()
            grupa = session.query(Grupe).filter(Grupe.id == sef.idgrupa).first()

            sefData = {
                "id": sef.id,
                "nume": sef.nume,
                "telefon": sef.telefon,
                "facultatea": sef.facultatea,
                "specializarea": sef.specializarea,
                "idgrupa": sef.idgrupa,
                "grupa": grupa.grupa,
            }

            if isinstance(exam.data, (datetime, date)):

                data_serialized = exam.data.strftime("%Y-%m-%d")

            else:

                data_serialized = exam.data

            examList.append({
                "id": exam.id,
                "sef": sefData,
                "profesorid": exam.profesorid,
                "materie": materiaToAdd,
                "data": data_serialized,
                "starea": exam.starea
            })

        return examList, 200

    except Exception as e:

        raise Exception(f"Error while getting exams: {str(e)}")

def get_approved_exams_of_profesor_repo(profesorId):
    try:
        exams = session.query(Examene).filter(
            Examene.profesorid == profesorId,
            Examene.starea == Status.APPROVED.name.lower()
        ).all()

        examList = []

        for exam in exams:
            # Fetch Materii (Subjects)
            materia = session.query(Materii).filter(Materii.id == exam.materieid).first()

            materiaToAdd = {
                "id": materia.id,
                "nume": materia.nume,
                "credite": materia.numarcredite,
                "abreviere": materia.abreviere,
                "tipevaluare": materia.tipevaluare,
            }

            # Fetch Sef and Grupa
            sef = session.query(Student).filter(Student.id == exam.sefid).first()
            grupa = session.query(Grupe).filter(Grupe.id == sef.idgrupa).first()

            sefData = {
                "id": sef.id,
                "nume": sef.nume,
                "telefon": sef.telefon,
                "facultatea": sef.facultatea,
                "specializarea": sef.specializarea,
                "idgrupa": sef.idgrupa,
                "grupa": grupa.grupa,
            }

            # Convert 'data' to string format if it's a date
            if isinstance(exam.data, (datetime, date)):
                data_serialized = exam.data.strftime("%Y-%m-%d")
            else:
                data_serialized = exam.data

            # 'orastart' time remains unchanged
            orastart_serialized = exam.orastart.strftime("%H:%M") if exam.orastart else None

            # Add one minute to 'orafinal' if it's not None
            if exam.orafinal:
                orafinal_time = datetime.combine(datetime.today(), exam.orafinal) + timedelta(minutes=1)
                orafinal_serialized = orafinal_time.strftime("%H:%M")
            else:
                orafinal_serialized = None

            # Add exam details to list
            examList.append({
                "id": exam.id,
                "sef": sefData,
                "profesorid": exam.profesorid,
                "materie": materiaToAdd,
                "data": data_serialized,
                "starea": exam.starea,
                "orastart": orastart_serialized,
                "orafinal": orafinal_serialized
            })

        return examList, 200

    except Exception as e:
        raise Exception(f"Error while getting exams: {str(e)}")


def update_examen_repo(examenData):

    try:

        examen = session.query(Examene).filter(Examene.id == examenData['id']).first()

        if examen is None:

            raise Exception(f"Examen with id {examenData['id']} not found.")

        examen.orastart = examenData['orastart']
        examen.orafinal = examenData['orafinal']
        examen.actualizatde = examenData['actualizatde']
        examen.actualizatla = datetime.utcnow()
        examen.asistentid = examenData['asistentid']
        examen.data = examenData['data']

        update_salacere = session.query(SaliCereri).filter(SaliCereri.idcerere == examenData['id']).first()

        if update_salacere:

            update_salacere.idsala = examenData['salaid']

        else:

            raise Exception(f"SaliCereri entry with idcerere {examenData['id']} not found.")

        session.flush()
        session.commit()

        student_data = session.query(Utilizator).filter(Utilizator.id == examenData['sefid']).first()

        if student_data:
            pass

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while updating examen: {str(e)}")

def get_examene_grupa_repo(idGrupa):
    try:
        # Fetch the Sef for the group
        sefId = session.query(Student).filter(Student.idgrupa == idGrupa, Student.sef == True).first()

        # Fetch exams for that Sef
        examene = session.query(Examene).filter(Examene.sefid == sefId.id, Examene.starea == Status.APPROVED.name.lower()).all()

        examList = []

        for examen in examene:

            # Fetch Materie (Subject)
            materie = session.query(Materii).filter(Materii.id == examen.materieid).first()

            materiaToAdd = {
                "id": materie.id,
                "nume": materie.nume,
                "credite": materie.numarcredite,
                "abreviere": materie.abreviere,
                "tipevaluare": materie.tipevaluare,
            }

            # Fetch the Sef and their Grupa (Group)
            sef = session.query(Student).filter(Student.id == examen.sefid).first()
            grupa = session.query(Grupe).filter(Grupe.id == sef.idgrupa).first()

            sefData = {
                "id": sef.id,
                "nume": sef.nume,
                "telefon": sef.telefon,
                "facultatea": sef.facultatea,
                "specializarea": sef.specializarea,
                "idgrupa": sef.idgrupa,
                "grupa": grupa.grupa,
            }

            # Convert the 'data' field to string (if it's a date)
            if isinstance(examen.data, (datetime, date)):
                data_serialized = examen.data.strftime("%Y-%m-%d")
            else:
                data_serialized = examen.data

            # 'orastart' remains unchanged
            orastart_serialized = examen.orastart.strftime("%H:%M") if examen.orastart else None

            # Add one minute to 'orafinal' time if it exists
            if examen.orafinal:
                orafinal_time = datetime.combine(datetime.today(), examen.orafinal) + timedelta(minutes=1)
                orafinal_serialized = orafinal_time.strftime("%H:%M")
            else:
                orafinal_serialized = None

            # Append exam data to list
            examList.append({
                "id": examen.id,
                "sef": sefData,
                "profesorid": examen.profesorid,
                "materie": materiaToAdd,
                "data": data_serialized,
                "starea": examen.starea,
                "orastart": orastart_serialized,
                "orafinal": orafinal_serialized
            })

        return examList, 200

    except Exception as e:
        raise Exception(f"Error while getting exams for group: {str(e)}")


