import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.Entities.asistenti import Asistenti
from Domain.extensions import session
def add_profesor_repo(profesor_data):

    profesor = Profesor(profesor_data['id'], profesor_data['nume'], profesor_data['telefon'], profesor_data['departament'])
    session.add(profesor)


def get_profesori_repo():

    try:

        profesori = session.query(Profesor).all()

        profesori_list = []

        for prof in profesori:

            profesori_list.append({
                "id": prof.id,
                "nume": prof.nume,
                "telefon": prof.telefon,
                "departament": prof.departament
            })

        return profesori_list

    except Exception as e:
        raise Exception(f"Error while getting profesori: {str(e)}")
