import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.Entities.asistent import Asistenti
from Domain.extensions import session



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


