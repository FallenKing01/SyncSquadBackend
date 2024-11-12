import uuid
from Domain.Entities.grupa import Grupe
from Domain.Entities.student import Student
from Domain.extensions import session
from sqlalchemy.exc import IntegrityError




def create_grupa_repo(grupa_data):

    grupa_id = str(uuid.uuid4())

    try:

        grupa_data['id'] = grupa_id

        grupa = Grupe(grupa_data['id'],grupa_data['grupa'])

        session.add(grupa)
        session.commit()

        return {"message": "Group created successfully"}, 201

    except IntegrityError as e:

        session.rollback()
        if "unique key" in str(e).lower():
            return {"message": "A group with this name already exists."}, 409


    except Exception as e:

        session.rollback()
        print(f"Error while inserting group: {e}")
        return {"message": f"An error occurred while creating the group: {e}"}, 500

def get_students_of_group_repo(grupaId):
    try:

        students = session.query(Student).filter(Student.idgrupa == grupaId).all()

        students_list = []

        if not students:

            return students_list, 404



        for student in students:

            student_dict = {
                "id": student.id,
                "nume": student.nume,
                "telefon" : student.telefon,
                "facultatea" : student.facultatea,
                "specializarea" : student.specializarea,
                "isSef" : student.sef
            }

            students_list.append(student_dict)

        return students_list

    except Exception as e:
        print(f"Error while fetching students: {e}")
        return {"message": f"An error occurred while fetching students: {e}"}, 500
