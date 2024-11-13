import uuid
from Domain.extensions import session
from Domain.Entities.sala import Sali

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


