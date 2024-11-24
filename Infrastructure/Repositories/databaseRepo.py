from Domain.extensions import open_session
from Utils.constants import SALI_URL,PROFESORI_URL
import requests
import uuid
from Domain.Entities.sala import Sali
from Domain.Entities.profesor import Profesor


def insert_database_sali_from_api_repo():

    response = requests.get(SALI_URL)
    data_list = response.json()

    try:

        session = open_session()

        for record in data_list:

            if record.get('name') is None or record.get('shortName') == '':

                continue

            record["departament"] = None
            sali_entry = Sali(
                str(uuid.uuid4()),
                record['name'],
                record['departament'],
                record['shortName'],
                record['buildingName']
            )

            session.add(sali_entry)

        session.commit()

    except Exception as e:

        session.rollback()

    finally:

        session.close()

def insert_profesori_from_api_repo():

    response = requests.get(PROFESORI_URL)
    data_list = response.json()

    try:

        session = open_session()
        count = 0

        for record in data_list:

            if (
                record.get('facultyName') == "Facultatea de Inginerie Electrică şi Ştiinţa Calculatoarelor"
                and count < 50
            ):

                last_name = record.get('lastName', '').strip()
                first_name = record.get('firstName', '').strip()

                if not last_name or not first_name:

                    continue

                full_name = f"{last_name} {first_name}"

                profesor_entry = Profesor(
                    str(uuid.uuid4()),
                    full_name,
                    None,
                    None
                )

                session.add(profesor_entry)

                count += 1

        session.commit()

    except Exception as e:

        session.rollback()

    finally:

        session.close()