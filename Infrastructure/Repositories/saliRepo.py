import uuid
from Domain.extensions import session
from Domain.Entities.sala import Sali
from Domain.Entities.saliCereri import SaliCereri
from Domain.Entities.examen import Examene
from datetime import datetime,timedelta
from sqlalchemy.exc import SQLAlchemyError

def add_sali_repo(sali_data):

    sala = Sali(sali_data['id'], sali_data['nume'], sali_data['departament'])
    session.add(sala)

def create_sali_repo(sali_data):

    id = str(uuid.uuid4())

    try:

        sali_data['id'] = id
        add_sali_repo(sali_data)
        session.commit()

        return {"message": "Sala adaugata cu succes!"},201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while adding sala: {str(e)}")

def get_sali_from_department_repo(departament_name):

    try:

        sali = session.query(Sali).filter(Sali.departament == departament_name).all()

        sali_list = []

        for sala in sali:

            sali_list.append({
                "id": sala.id,
                "nume": sala.nume,
                "departament": sala.departament
            })

        return sali_list

    except Exception as e:
        raise Exception(f"Error while getting sali: {str(e)}")


def delete_sala_repo(sala_id):
    try:

        sala = session.query(Sali).filter(Sali.id == sala_id).first()

        if sala is None:

            raise Exception(f"Sala not found")

        session.delete(sala)
        session.commit()

        return {"message": "Sala  stearsa cu succes!" }

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while getting sali: {str(e)}")
from datetime import datetime, timedelta

from datetime import datetime, timedelta


from datetime import datetime

def get_liber_sala(sala_id, data_examen):
    # Define fixed available intervals
    morning_start = datetime.strptime("08:00", "%H:%M")
    morning_end = datetime.strptime("12:00", "%H:%M")
    evening_start = datetime.strptime("16:00", "%H:%M")
    evening_end = datetime.strptime("20:00", "%H:%M")

    # Fetch scheduled exams for the room and the given date
    exams = session.query(SaliCereri).filter(SaliCereri.idsala == sala_id).all()

    # If no exams are scheduled, return the fixed intervals
    if not exams:
        return [
            {"ora_start": morning_start.strftime("%H:%M"), "ora_end": morning_end.strftime("%H:%M")},
            {"ora_start": evening_start.strftime("%H:%M"), "ora_end": evening_end.strftime("%H:%M")}
        ]

    # Initialize the result
    available_slots = []

    # Process morning slot (08:00 - 12:00)
    is_morning_available = True
    for exam in exams:
        current_exam = session.query(Examene).filter(
            Examene.id == exam.idcerere,
            Examene.data == data_examen
        ).first()

        if current_exam:
            exam_start = datetime.strptime(str(current_exam.orastart), "%H:%M:%S")
            exam_end = datetime.strptime(str(current_exam.orafinal), "%H:%M:%S")

            # Check if the exam overlaps with the morning slot
            if exam_start < morning_end and exam_end > morning_start:
                is_morning_available = False

    if is_morning_available:
        available_slots.append({
            "ora_start": morning_start.strftime("%H:%M"),
            "ora_end": morning_end.strftime("%H:%M")
        })

    # Process evening slot (16:00 - 20:00)
    is_evening_available = True
    for exam in exams:
        current_exam = session.query(Examene).filter(
            Examene.id == exam.idcerere,
            Examene.data == data_examen
        ).first()

        if current_exam:
            exam_start = datetime.strptime(str(current_exam.orastart), "%H:%M:%S")
            exam_end = datetime.strptime(str(current_exam.orafinal), "%H:%M:%S")

            # Check if the exam overlaps with the evening slot
            if exam_start < evening_end and exam_end > evening_start:
                is_evening_available = False

    if is_evening_available:
        available_slots.append({
            "ora_start": evening_start.strftime("%H:%M"),
            "ora_end": evening_end.strftime("%H:%M")
        })

    return available_slots


# Example usage
