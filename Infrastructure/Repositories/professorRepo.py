import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.Entities.asistent import Asistenti
from Domain.extensions import session
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.Entities.saliCereri import SaliCereri
from datetime import datetime

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



def accept_examen_by_profesor_repo(exam_data):

    try:

        examen = session.query(Examene).filter(Examene.id == exam_data['id']).first()
        idSalaCerere = str(uuid.uuid4())

        if examen is None:

            raise Exception("Examen not found")

        examen.asistentid = exam_data['asistentid']
        examen.orastart = exam_data['orastart']
        examen.orafinal = exam_data['orafinal']
        examen.starea = Status.APPROVED.name.lower()
        examen.actualizatde = examen.profesorid
        examen.actualizatla = datetime.utcnow()

        sala_cerere = SaliCereri(idSalaCerere,examen.id,exam_data["salaid"])
        session.add(sala_cerere)

        session.commit()

    except Exception as e:

        raise Exception(f"Error while accepting examen: {str(e)}")
