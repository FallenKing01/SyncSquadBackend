import uuid

from Domain.extensions import session
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Utils.enums.role import Role
from Domain.Entities.grupa import Grupe
from Domain.Entities.examen import Examene
def get_grupe_from_repo():

    try:

        grupe = session.query(Grupe).all()

        grupe_list = []

        for grupa in grupe:
            grupe_list.append({
                "id": grupa.id,
                "nume": grupa.grupa,
            })

        return grupe_list, 200

    except Exception as e:

        raise Exception(f"Error while fetching grupe: {str(e)}")


def get_grupa_dupa_nume(nume):

    try:

        grupe = (
            session.query(Grupe)
            .filter(Grupe.grupa.ilike(f"%{nume}%"))
            .limit(10)
            .all()
        )

        grupe_list = []

        for grupa in grupe:
            grupe_list.append({
                "id": grupa.id,
                "nume": grupa.grupa,
            })

        return grupe_list, 200

    except Exception as e:

        raise Exception(f"Error while fetching grupa: {str(e)}")

def create_grupa_repo(data):

    try:

        grupa = Grupe(str(uuid.uuid4()), data['nume'])
        session.add(grupa)
        session.commit()

        return {"message": "Grupa created successfully"}, 201

    except Exception as e:

        session.rollback()

        raise Exception(f"Error while creating grupa: {str(e)}")
