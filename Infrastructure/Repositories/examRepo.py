import uuid
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.extensions import open_session
from Domain.Entities.materie import Materii
from datetime import datetime,timedelta
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.saliCereri import SaliCereri
from Domain.Entities.student import Student
from Domain.Entities.grupa import Grupe
from Domain.Entities.profesor import Profesor
from datetime import datetime, date
from Services.EmailSenderService import sendEmail
from Domain.Entities.sala import Sali
from Domain.Entities.asistent import Asistenti
from sqlalchemy import asc


def add_examen_repo(exam_data,session):

    exam = Examene(Id=exam_data["id"],SefId=exam_data["sefid"],ProfesorId=exam_data["profesorid"], MaterieId=exam_data["materieid"], Data=exam_data["data"],Starea=Status.PENDING.name.lower())
    session.add(exam)

def add_examen_fortat_repo(exam_data,session):

    exam = Examene(Id=exam_data["id"],SefId=exam_data["sefid"],ProfesorId=exam_data["profesorid"], MaterieId=exam_data["materieid"], Data=exam_data["data"],Starea=Status.APPROVED.name.lower(),OraStart=exam_data["orastart"],OraFinal=exam_data["orafinal"],ActualizatDe=exam_data["actualizatde"],AsistentId=exam_data["asistentid"],ActualizatLa=datetime.utcnow())
    session.add(exam)

def create_examen_repo(exam_data):

    id = str(uuid.uuid4())

    try:

        session = open_session()
        exam_data["id"] = id

        add_examen_repo(exam_data,session)
        session.commit()

        return {"message": "Exam added successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while inserting exam: {str(e)}")

    finally:

        session.close()

def get_pending_exams_of_profesor_repo(profesorId):

    try:

        session = open_session()

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

    finally:

        session.close()

def get_approved_exams_of_profesor_repo(profesorId):

    try:

        session = open_session()

        exams = session.query(Examene).filter(
            Examene.profesorid == profesorId,
            Examene.starea == Status.APPROVED.name.lower()
        ).order_by(
            asc(Examene.data),
            asc(Examene.orastart)
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

            # Convert 'data' to string format if it's a date
            if isinstance(exam.data, (datetime, date)):
                data_serialized = exam.data.strftime("%Y-%m-%d")
            else:
                data_serialized = exam.data

            orastart_serialized = exam.orastart.strftime("%H:%M") if exam.orastart else None

            if exam.orafinal:

                orafinal_time = datetime.combine(datetime.today(), exam.orafinal)
                orafinal_serialized = orafinal_time.strftime("%H:%M")

            else:

                orafinal_serialized = None

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

        session = open_session()

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

        materiaId = examen.materieid
        reactualizantId = examenData['actualizatde']
        salaId = examenData['salaid']

        reactualizant_data = session.query(Utilizator).filter(Utilizator.id == reactualizantId).first()
        sala_data = session.query(Sali).filter(Sali.id == salaId).first()

        if str(reactualizant_data.rol) == "secretar":

            rol = "secretariat."

        else:

            rol = "profesorul titular la curs."

        materie_data = session.query(Materii).filter(Materii.id == materiaId).first()


        if student_data:

                text = ("Examenul la materia " + str(materie_data.nume) + " a fost reprogramat pentru data de " + str(examenData['data'])
                        + " in intervalul orar " + str(examenData['orastart']) + " - " + str(examenData['orafinal']) +". Examenul se va sustine in sala " +
                        str(sala_data.nume) +" in corpul "+ str(sala_data.cladire) + ".\nVa adresez urmatoarele: \n" +
                        str(examenData['motiv']) + "\nExamenul a fost reactualizat de " + rol)

                titlu = "Reprogramare examen " + str(materie_data.nume)

                data = {
                    "text": text,
                    "titlu": titlu,
                    "email": str(student_data.email)
                }

                sendEmail(data)


    except Exception as e:

        session.rollback()

        raise Exception(f"Error while updating examen: {str(e)}")

    finally:

        session.close()

def get_examene_grupa_repo(idGrupa):

    try:

        session = open_session()

        sefId = session.query(Student).filter(Student.idgrupa == idGrupa, Student.sef == True).first()

        if sefId is None:

            return

        examene = session.query(Examene).filter(Examene.sefid == sefId.id, Examene.starea == Status.APPROVED.name.lower()).all()

        examList = []

        for examen in examene:

            materie = session.query(Materii).filter(Materii.id == examen.materieid).first()

            materiaToAdd = {
                "id": materie.id,
                "nume": materie.nume,
                "credite": materie.numarcredite,
                "abreviere": materie.abreviere,
                "tipevaluare": materie.tipevaluare,
            }

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

            if isinstance(examen.data, (datetime, date)):

                data_serialized = examen.data.strftime("%Y-%m-%d")

            else:

                data_serialized = examen.data

            orastart_serialized = examen.orastart.strftime("%H:%M") if examen.orastart else None

            if examen.orafinal:

                orafinal_time = datetime.combine(datetime.today(), examen.orafinal)
                orafinal_serialized = orafinal_time.strftime("%H:%M")

            else:

                orafinal_serialized = None

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

    finally:

            session.close()

def get_examene_sef_semigrupa_stare(student_id, starea):

    try:

        session = open_session()

        grupa_stud = session.query(Student).filter(Student.id == student_id).first()
        print(grupa_stud.idgrupa)
        sef_id = session.query(Student).filter(Student.idgrupa == grupa_stud.idgrupa, Student.sef == True).first().id
        print(sef_id)
        examene = session.query(Examene).filter(Examene.sefid == sef_id, Examene.starea == starea).all()
        print(examene)
        examList = []

        for examen in examene:

            materie = session.query(Materii).filter(Materii.id == examen.materieid).first()

            materiaToAdd = {
                "id": materie.id,
                "nume": materie.nume,
                "credite": materie.numarcredite,
                "abreviere": materie.abreviere,
                "tipevaluare": materie.tipevaluare,
            }

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

            # Serialize 'orastart' time
            orastart_serialized = examen.orastart.strftime("%H:%M") if examen.orastart else None

            # Add one minute to 'orafinal' time if it exists
            if examen.orafinal:
                orafinal_time = datetime.combine(datetime.today(), examen.orafinal)
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

        raise Exception(f"Error while getting exams for sef and starea: {str(e)}")

    finally:

            session.close()

def decline_examen_repo(examId,data):

    try:

        session = open_session()

        examen = session.query(Examene).filter(Examene.id == examId).first()

        if examen is None:

            raise Exception(f"Examen with id {examId} not found.")


        examen.starea = Status.REJECTED.name.lower()
        session.commit()

        profId = examen.profesorid
        materieId = examen.materieid
        studentId = examen.sefid

        dateProfesor = session.query(Profesor).filter(Profesor.id == profId).first()
        dateMaterie = session.query(Materii).filter(Materii.id == materieId).first()
        emailStudent = session.query(Utilizator).filter(Utilizator.id == studentId).first()

        text = "Rog reprogramarea examenului la materia " + str(dateMaterie.nume) + " pentru data de " + str(examen.data) + "\n Va adresez urmatoarele : \n" + data["motiv"] + "\n Cu respect, " + str(dateProfesor.nume)
        titlu = "Reprogramare examen " + str(dateMaterie.nume)

        data = {
            "text": text,
            "titlu": titlu,
            "email": emailStudent.email
        }

        sendEmail(data)

        return {"message": "Examen rejected successfully"}, 200

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while rejecting exam: {str(e)}")

    finally:

        session.close()


def create_examen_fortat(exam_data):

    id = str(uuid.uuid4())

    try:

        session = open_session()

        exam_data["id"] = id
        sef_data = session.query(Student).filter(Student.idgrupa == exam_data["grupaid"], Student.sef == True).first()

        if sef_data is None:

            return {"message": "Group leader not found"},418

        exam_data["sefid"] = sef_data.id

        add_examen_fortat_repo(exam_data,session)

        saliCereri = SaliCereri(str(uuid.uuid4()),idcerere=id,idsala=exam_data["salaid"])
        session.add(saliCereri)

        session.commit()

        return {"message": "Exam added successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while inserting exam: {str(e)}")

    finally:

        session.close()
def has_time_conflict(existing_start, existing_end, requested_start, requested_end):

    return not (requested_end <= existing_start or requested_start >= existing_end)

def get_profesor_disponibil_repo(examenData):

    try:

        session = open_session()

        # Parse requested exam time
        requested_start = datetime.strptime(examenData['orastart'], '%H:%M').time()
        requested_end = datetime.strptime(examenData['orafinal'], '%H:%M').time()

        print(f"Requested Time: {requested_start} - {requested_end}")

        # Fetch the professor's data
        profesor = session.query(Profesor).filter(Profesor.id == examenData['profesorid']).first()
        if profesor is None:
            raise Exception(f"Profesor with id {examenData['profesorid']} not found.")

        # Fetch all assistants for this professor
        asistenti = session.query(Asistenti).filter(Asistenti.idprof == examenData['profesorid']).all()
        asistentiIds = [asistent.idasistent for asistent in asistenti]

        # Fetch all approved exams for the requested date
        exams_on_date = session.query(Examene).filter(
            Examene.data == examenData['data'],
            Examene.starea == Status.APPROVED.name.lower()
        ).all()

        print(f"Exams on {examenData['data']}: {[{'prof': ex.profesorid, 'asist': ex.asistentid, 'start': ex.orastart, 'end': ex.orafinal} for ex in exams_on_date]}")

        available_ids = []

        # Check availability for each assistant
        for asistent_id in asistentiIds:

            is_available = True

            # Check for conflicts as assistant or professor
            for exam in exams_on_date:
                exam_start = exam.orastart  # Assuming datetime.time
                exam_end = exam.orafinal  # Assuming datetime.time

                # If assistant is involved in this exam
                if exam.asistentid == asistent_id or exam.profesorid == asistent_id:
                    if has_time_conflict(exam_start, exam_end, requested_start, requested_end):
                        is_available = False
                        break

            if is_available:

                available_ids.append(asistent_id)

        available_prof_list = []

        for prof_id in available_ids:

            prof_data = session.query(Profesor).filter(Profesor.id == prof_id).first()

            if prof_data:

                available_prof_list.append({
                    "nume": prof_data.nume,
                    "id": prof_data.id
                })

        return available_prof_list

    except Exception as e:

        return []

    finally:

        session.close()
def delete_examen_programat_repo(examen_id, data):
    try:
        session = open_session()

        # Fetch the exam
        examen = session.query(Examene).filter(Examene.id == examen_id).first()
        if examen is None:
            raise Exception(f"Examen with id {examen_id} not found.")

        # Notify the student
        sefid = examen.sefid
        acc_student = session.query(Utilizator).filter(Utilizator.id == sefid).first()
        email_to_send = {
            "text": f"Examenul la materia {examen.materieid} a fost anulat. Motivul: {data['motiv']}",
            "titlu": "Anulare examen",
            "email": acc_student.email,
        }
        sendEmail(email_to_send)

        # Delete related SaliCereri entries
        session.query(SaliCereri).filter(SaliCereri.idcerere == examen_id).delete()

        # Delete the exam
        session.delete(examen)

        session.commit()
        return {"message": "Examen deleted successfully"}, 200

    except Exception as e:
        session.rollback()
        raise Exception(f"Error while deleting exam: {str(e)}")

    finally:
        session.close()
