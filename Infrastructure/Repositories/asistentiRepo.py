import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.Entities.asistent import Asistenti
from Domain.extensions import open_session
from Domain.Entities.examen import Examene


def create_asistent_repo(titularId , asistentId):

    try:

        session = open_session()

        id = str(uuid.uuid4())

        titularExist = session.query(Profesor).filter(Profesor.id == titularId).first()

        if(titularExist is None):

            return {"error": "The professor does not exist"}, 204

        asistentExist = session.query(Profesor).filter(Profesor.id == asistentId).first()

        if(asistentExist is None):

            return {"error": "The assistant does not exist"}, 204

        asistent = Asistenti(id, titularId ,asistentId)
        session.add(asistent)
        session.commit()

        return {"message": "Assistant created successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while inserting assistant: {str(e)}")

    finally:

        session.close()

def get_asistenti_of_profesor_repo(profesorId):

    session = open_session()

    try:

        assistants = session.query(Asistenti).filter(Asistenti.idprof == profesorId).all()

        assistants_list = []

        if not assistants:

            return assistants_list, 204

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

    finally:

        session.close()


def delete_asistent_repo(asistent_id, profesor_id):

    try:

        session = open_session()

        asistent = session.query(Asistenti).filter(
            Asistenti.idasistent == asistent_id,
            Asistenti.idprof == profesor_id
        ).first()

        examene = session.query(Examene).filter(Examene.asistentid == asistent_id).all()

        if examene is not None:

            return {"message":"Asistentul are examene asignate si nu poate fi sters"}


        if asistent is None:

            raise Exception(f"Asistent with id '{asistent_id}' and profesor id '{profesor_id}' not found.")

        session.delete(asistent)
        session.commit()

        return {"message": f"Asistent with id '{asistent_id}' deleted successfully!"}

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while deleting asistent: {str(e)}")

    finally:

        session.close()


def get_asistenti_repo(profesorId):

    try:

        session = open_session()

        current_assistants = session.query(Asistenti).filter(Asistenti.idprof==profesorId).all()
        all_asistents = session.query(Profesor).all()

        result = []

        for asistent in all_asistents:

            if asistent.id != profesorId and asistent.id not in [assistant.idasistent for assistant in current_assistants]:

                result.append({
                    "id": asistent.id,
                    "nume": asistent.nume,
                    "telefon": asistent.telefon,
                    "departament": asistent.departament
                })

        return result,200

    except Exception as e:

        return {"error": str(e)}, 500

    finally:

        session.close()

