import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.Entities.asistenti import Asistenti
from Domain.extensions import session

def create_subject_repo(subject_data):

    subject_id = str(uuid.uuid4())

    try:

        profesor = session.query(Profesor).filter(Profesor.id == subject_data['profesorid']).first()

        if profesor is None:

            return {"error": "The professor does not exist"}, 404

        subject_data['id'] = subject_id


        subject = Materii(subject_data['id'], subject_data['nume'], subject_data['abreviere'],
                          subject_data['tipevaluare'], subject_data['numarcredite'], subject_data['profesorid'])

        session.add(subject)

        session.commit()

        return {"message": "Subject created successfully"}, 201

    except Exception as e:

        session.rollback()

        print(f"Error while inserting subject: {e}")
        raise Exception(f"Error while inserting subject: {str(e)}")


def get_subjects_of_profesor_repo(profesorId):
    try:
        # Fetch the list of subjects for the professor
        subjects = session.query(Materii).filter(Materii.profesorid == profesorId).all()

        if not subjects:
            return {"error": "No subjects found"}, 404

        # Create a list to hold dictionaries for each subject
        subjects_list = []

        for subject in subjects:
            # Create a dictionary for each subject
            subject_dict = {
                "subjectId": subject.id,
                "nume": subject.nume,
                "abreviere" : subject.abreviere,
                "tipEvaluare" : subject.tipevaluare,
                "numarCredite" : subject.numarcredite,
            }

            subjects_list.append(subject_dict)

        return subjects_list

    except Exception as e:

        raise Exception(f"Error while getting subjects of professor: {str(e)}")

def create_asistent_repo(titularId , asistentId):

    id = str(uuid.uuid4())

    titularExist = session.query(Profesor).filter(Profesor.id == titularId).first()

    if(titularExist is None):

        return {"error": "The professor does not exist"}, 404

    asistentExist = session.query(Profesor).filter(Profesor.id == asistentId).first()

    if(asistentExist is None):

        return {"error": "The assistant does not exist"}, 404


    try:

        asistent = Asistenti(id, titularId ,asistentId)

        session.add(asistent)

        session.commit()

        return {"message": "Assistant created successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while inserting assistant: {str(e)}")

def get_asistenti_of_profesor_repo(profesorId):
    try:
        # Fetch the list of assistants for the professor
        assistants = session.query(Asistenti).filter(Asistenti.idprof == profesorId).all()

        assistants_list = []

        if not assistants:
            return assistants_list, 404

        for assistant in assistants:

            current_assistant = session.query(Profesor).filter(Profesor.id == assistant.idasistent).first()

            assistants_list.append({
                "id" : current_assistant.id,
                "nume": current_assistant.nume,
                "telefon": current_assistant.telefon,
                "departament": current_assistant.departament
            })

        return assistants_list

    except Exception as e:
        raise Exception(f"Error while getting assistants of professor: {str(e)}")


