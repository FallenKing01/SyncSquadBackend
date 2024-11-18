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


def get_liber_sala(sala_id, data_examen):
    # Define the working hours for the day
    work_start = datetime.strptime("08:00", "%H:%M")
    work_end = datetime.strptime("20:00", "%H:%M")

    # Fetch scheduled exams for the given room and date
    exams = session.query(SaliCereri).filter(SaliCereri.idsala == sala_id).all()

    # If there are no exams scheduled, return the full default time slot
    if not exams:
        return [{
            "ora_start": work_start.strftime("%H:%M"),
            "ora_end": work_end.strftime("%H:%M")
        }]

    # Gather and process scheduled exams
    scheduled_exams = []
    for exam in exams:
        current_exam = session.query(Examene).filter(
            Examene.id == exam.idcerere,
            Examene.data == data_examen
        ).first()

        if current_exam:
            scheduled_exams.append({
                "ora_start": datetime.strptime(current_exam.orastart.strftime("%H:%M"), "%H:%M"),
                "ora_end": datetime.strptime(current_exam.orafinal.strftime("%H:%M"), "%H:%M")
            })

    # Sort exams by start time
    scheduled_exams.sort(key=lambda x: x["ora_start"])

    # Initialize available slots
    available_slots = []
    previous_end = work_start

    # Loop through the scheduled exams and find gaps
    for exam in scheduled_exams:
        start = exam["ora_start"]
        end = exam["ora_end"]

        # If there's a gap between the previous exam and the current one
        if previous_end < start:
            available_slots.append({
                "ora_start": (previous_end + timedelta(minutes=1)).strftime("%H:%M"),
                "ora_end": start.strftime("%H:%M")
            })

        # Update the end of the previous exam
        previous_end = end

    # After the last exam, check if there's time left until the end of the working hours
    if previous_end < work_end:
        available_slots.append({
            "ora_start": (previous_end + timedelta(minutes=1)).strftime("%H:%M"),
            "ora_end": work_end.strftime("%H:%M")
        })

    return available_slots

# Example usage
