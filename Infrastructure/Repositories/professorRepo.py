import uuid
from Domain.Entities.materie import Materii
from Domain.Entities.profesor import Profesor
from Domain.extensions import open_session
from Domain.Entities.examen import Examene
from Utils.enums.statusExam import Status
from Domain.Entities.saliCereri import SaliCereri
from datetime import datetime,timedelta
from Domain.Entities.sala import Sali
import requests

def add_profesor_repo(profesor_data,session):

    profesor = Profesor(profesor_data['id'], profesor_data['nume'], profesor_data['telefon'], profesor_data['departament'])
    session.add(profesor)


def get_profesori_repo():

    try:

        session = open_session()

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

    finally:

        session.close()



def accept_examen_by_profesor_repo(exam_data):

    try:

        session = open_session()

        examen = session.query(Examene).filter(Examene.id == exam_data['id']).first()
        idSalaCerere = str(uuid.uuid4())

        if examen is None:

            raise Exception("Examen not found")

        examen.asistentid = exam_data['asistentid']
        examen.orastart = exam_data['orastart']
        examen.orafinal = (datetime.strptime(exam_data['orafinal'], "%H:%M") ).strftime("%H:%M")
        examen.starea = Status.APPROVED.name.lower()
        examen.actualizatde = examen.profesorid
        examen.actualizatla = datetime.utcnow()

        sala_cerere = SaliCereri(idSalaCerere,examen.id,exam_data["salaid"])
        session.add(sala_cerere)

        session.commit()

    except Exception as e:

        raise Exception(f"Error while accepting examen: {str(e)}")

    finally:

        session.close()




def get_profesori_from_api(idgrupa):
    """
    Fetches the list of professor IDs from the API based on group ID.

    Args:
        idgrupa (str/int): The group ID to fetch professor data for.

    Returns:
        list: A list of unique professor IDs.
    """
    # Define API URL
    ORAR_GRUPA_URL = f"https://orar.usv.ro/orar/vizualizare/data/orarSPG.php?ID={idgrupa}&mod=grupa&json"
    session = open_session()

    try:

        response = requests.get(ORAR_GRUPA_URL)

        data_list = response.json()
        id_profesori = []
        data_list = data_list[0]
        for i in range(len(data_list)):

            if data_list[i]["typeLongName"] in ["curs", "proiect"]:

                id_prof_curent = data_list[i]["teacherID"]

                if id_prof_curent not in id_profesori:
                    id_profesori.append(id_prof_curent)


        data_profesor = []

        for id in id_profesori:

            prof_data = session.query(Profesor).filter(Profesor.id == id).first()
            if prof_data is not None:
                data_profesor.append({
                    "id": prof_data.id,
                    "nume": prof_data.nume,
                    "telefon": prof_data.telefon,
                    "departament": prof_data.departament
                })

        return data_profesor

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []


def get_orar_of_prof_repo(prof_id,data):

    try:

        session = open_session()

        examene = session.query(Examene).filter(Examene.profesorid == prof_id,Examene.starea==Status.APPROVED.name.lower(),Examene.data==data).all()

        examene_list = []

        for examen in examene:

            date_materie = session.query(Materii).filter(Materii.id == examen.materieid).first()
            date_materie = {
                "id": date_materie.id,
                "nume": date_materie.nume,
                "abreviere": date_materie.abreviere
            }

            idsala = session.query(SaliCereri).filter(SaliCereri.idcerere == examen.id).first().idsala

            date_sala = session.query(Sali).filter(Sali.id == idsala).first()
            date_sala = {
                "id": date_sala.id,
                "nume": date_sala.nume,
                "departament": date_sala.departament,
                "abreviere": date_sala.abreviere,
                "cladire": date_sala.cladire
            }

            examene_list.append({
                "id": examen.id,
                "materie": date_materie,
                "profesorid": examen.profesorid,
                "asistentid": examen.asistentid,
                "orastart": str(examen.orastart),
                "orafinal": str(examen.orafinal),
                "salaid": date_sala
            })

        return examene_list

    except Exception as e:

        raise Exception(f"Error while getting orar of profesor: {str(e)}")

    finally:

        session.close()



