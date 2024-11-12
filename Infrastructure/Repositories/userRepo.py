import uuid
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Domain.Entities.secretar import Secretar
from Utils.passwordhash import hash_password
from Domain.extensions import session

def create_student_repo(user_data):

    user_id = str(uuid.uuid4())

    try:

        user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
        user_data['id'] = user_id

        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'student')
        student = Student(user_data['id'], user_data['nume'], user_data['telefon'],
                          user_data['facultatea'], user_data['specializarea'], user_data['idGrupa'], False)

        session.add(utilizator)
        session.add(student)

        session.commit()

        return {"message": "Student created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():

            return {
                "error": "Email already exists. Please use a different email."}, 409  # 409 Conflict HTTP status code

        print(f"Error while inserting user: {e}")
        raise Exception(f"Error while inserting user: {str(e)}")


def create_profesor_repo(user_data):

    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id

    try:

        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'profesor')
        session.add(utilizator)

        profesor = Profesor(user_data['id'], user_data['nume'], user_data['telefon'], user_data['departament'])
        session.add(profesor)

        session.commit()
        return {"message": "Profesor created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        print(f"Error while inserting professor: {e}")
        raise Exception(f"Error while inserting professor: {str(e)}")

def create_secretar_repo(user_data):

    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id

    try:

        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'secretar')
        session.add(utilizator)

        secretar = Secretar(user_data['id'], user_data['nume'], user_data['telefon'])
        session.add(secretar)

        session.commit()
        return {"message": "Secretar created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        print(f"Error while inserting secretary: {e}")
        raise Exception(f"Error while inserting secretary: {str(e)}")

def get_users_repo():
    """Retrieve a list of students from the database using the SQLAlchemy session."""
    try:

        students = session.query(Student).all()

        users_list = []
        for student in students:
            user_dict = {
                "id": student.id,
                "nume": student.nume,
                "telefon": student.telefon,
                "facultatea": student.facultatea,
                "specializarea": student.specializarea,
                "idgrupa": student.idgrupa,
                "sef": student.sef
            }
            users_list.append(user_dict)

        return users_list

    except Exception as e:
        print(f"Error while fetching users: {e}")
        raise Exception(f"Error while fetching users: {str(e)}")
