import uuid

from Domain.Entities.materie import Materii
from Domain.extensions import open_session
from Domain.Entities.sala import Sali
from Domain.Entities.saliCereri import SaliCereri
from Domain.Entities.examen import Examene
from datetime import datetime,timedelta
from Utils.enums.statusExam import Status
def add_sali_repo(sali_data,session):

    sala = Sali(sali_data['id'], sali_data['nume'], sali_data['departament'])
    session.add(sala)

def create_sali_repo(sali_data):

    id = str(uuid.uuid4())

    try:

        session = open_session()

        sali_data['id'] = id
        add_sali_repo(sali_data,session)
        session.commit()

        return {"message": "Sala adaugata cu succes!"},201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while adding sala: {str(e)}")

    finally:

        session.close()

def get_sali_from_department_repo(departament_name):

    try:

        session = open_session()

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

    finally:

        session.close()



def delete_sala_repo(sala_id):

    try:

        session = open_session()

        sala = session.query(Sali).filter(Sali.id == sala_id).first()

        if sala is None:

            raise Exception(f"Sala not found")

        session.delete(sala)
        session.commit()

        return {"message": "Sala  stearsa cu succes!" }

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while getting sali: {str(e)}")

    finally:

        session.close()



def round_to_nearest_5_minutes(dt):
    """Rounds a datetime object to the nearest 5 minutes."""
    minutes = (dt.minute + 2) // 5 * 5  # Round to the nearest 5
    return dt.replace(minute=minutes % 60, second=0, microsecond=0) + timedelta(hours=minutes // 60)

def get_liber_sala_repo(sala_id, data_examen):

    try:
        session = open_session()

        work_start = round_to_nearest_5_minutes(datetime.strptime("08:00", "%H:%M"))
        work_end = round_to_nearest_5_minutes(datetime.strptime("20:00", "%H:%M"))

        exams = session.query(SaliCereri).filter(SaliCereri.idsala == sala_id).all()

        # Check if there are any exams scheduled on the given date
        scheduled_exams = []

        for exam in exams:
            current_exam = session.query(Examene).filter(
                Examene.id == exam.idcerere,
                Examene.data == data_examen
            ).first()

            if current_exam:  # If a valid exam is found, add it to the list
                scheduled_exams.append({
                    "ora_start": round_to_nearest_5_minutes(datetime.strptime(current_exam.orastart.strftime("%H:%M"), "%H:%M")),
                    "ora_end": round_to_nearest_5_minutes(datetime.strptime(current_exam.orafinal.strftime("%H:%M"), "%H:%M"))
                })

        # If no scheduled exams exist for the given date, return the full working hours
        if not scheduled_exams:
            return [{
                "ora_start": work_start.strftime("%H:%M"),
                "ora_end": work_end.strftime("%H:%M")
            }]

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
                    "ora_start": previous_end.strftime("%H:%M"),
                    "ora_end": start.strftime("%H:%M")
                })

            # Update the end of the previous exam
            previous_end = end

        # After the last exam, check if there's time left until the end of the working hours
        if previous_end < work_end:
            available_slots.append({
                "ora_start": previous_end.strftime("%H:%M"),
                "ora_end": work_end.strftime("%H:%M")
            })

        return available_slots

    except Exception as e:

        raise Exception(f"Error while getting sali: {str(e)}")

    finally:

        session.close()

def get_sali_dupa_nume_repo(numeSala):

    try:

        session = open_session()
        # Use ilike for case-insensitive partial matching and limit results to 10
        sali = session.query(Sali).filter(Sali.nume.ilike(f"%{numeSala}%")).limit(10).all()

        # Build the result list
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

    finally:

        session.close()

def get_orar_sali_repo(salaId, data):

    try:

        session = open_session()

        sali_cereri = session.query(SaliCereri).filter(SaliCereri.idsala == salaId).all()

        # Extract the list of exam request IDs
        exameneId = {cerere.idcerere for cerere in sali_cereri}

        # Query all exams for the specified date
        examene = (
            session.query(Examene)
            .filter(Examene.data == data, Examene.starea == Status.APPROVED.name.lower())
            .all()
        )

        examene_list = []

        for examen in examene:
            # Skip exams that match any ID in the cereri list
            if examen.id in exameneId:


                # Fetch subject (Materii) details
                materia = session.query(Materii).filter(Materii.id == examen.materieid).first()

                # Prepare subject details if found
                data_materia = {
                    "id": materia.id,
                    "nume": materia.nume,
                    "abreviere": materia.abreviere,
                    "tipevaluare": materia.tipevaluare,
                } if materia else None

                # Add exam details to the list
                examene_list.append({
                    "id": examen.id,
                    "data": examen.data.isoformat(),
                    "orastart": str(examen.orastart),
                    "orafinal": str(examen.orafinal),
                    "materie": data_materia,
                })

        return examene_list

    except Exception as e:

        raise Exception(f"Error while getting sali: {str(e)}")

    finally:

        session.close()



