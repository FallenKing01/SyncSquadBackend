import uuid
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Utils.passwordhash import hash_password
from Domain.extensions import open_session
from Infrastructure.Repositories.professorRepo import add_profesor_repo
from Infrastructure.Repositories.secretariatRepo import add_secretar_repo
from Infrastructure.Repositories.studentRepo import add_student_repo
from Utils.enums.role import Role
from Domain.Entities.profesor import Profesor
from Domain.Entities.secretar import Secretar

def add_utilizator_repo(user_data,session):

        user = Utilizator(user_data['id'], user_data['email'], user_data['parola'], user_data['rol'])
        session.add(user)

def create_student_repo(user_data):

    user_id = str(uuid.uuid4())

    try:

        session = open_session()

        user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
        user_data['id'] = user_id
        user_data['rol'] = Role.STUDENT.name.lower()

        add_utilizator_repo(user_data,session)
        add_student_repo(user_data,session)

        session.commit()

        return {"message": "Student created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():

            return {"error": "Email already exists. Please use a different email."}, 409

        raise Exception(f"Error while inserting user: {str(e)}")

    finally:

        session.close()


def create_profesor_repo(user_data):

    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id
    user_data['rol'] = Role.PROFESOR.name.lower()

    try:

        session = open_session()

        add_utilizator_repo(user_data,session)
        add_profesor_repo(user_data,session)

        session.commit()

        return {"message": "Profesor created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        raise Exception(f"Error while inserting professor: {str(e)}")

    finally:

        session.close()

def create_secretar_repo(user_data):

    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id
    user_data['rol'] = Role.SECRETAR.name.lower()

    try:

        session = open_session()

        add_utilizator_repo(user_data,session)
        add_secretar_repo(user_data,session)

        session.commit()

        return {"message": "Secretar created successfully"}, 201

    except Exception as e:

        session.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        print(f"Error while inserting secretary: {e}")
        raise Exception(f"Error while inserting secretary: {str(e)}")

    finally:

        session.close()


def get_info_user_repo(id):

    try:

        session = open_session()

        userData = session.query(Utilizator).filter(Utilizator.id == id).first()

        if userData is None:

            raise Exception("User not found", 204)

        if userData.rol == Role.STUDENT.name.lower() or userData.rol == Role.SEF.name.lower():

            studentData = session.query(Student).filter(Student.id == id).first()

            return {
                "id": studentData.id,
                "nume": studentData.nume,
                "telefon": studentData.telefon,
                "facultatea": studentData.facultatea,
                "specializarea": studentData.specializarea,
                "idgrupa": studentData.idgrupa,
                "sef": studentData.sef
            }

        if userData.rol == Role.PROFESOR.name.lower():

                profesorData = session.query(Profesor).filter(Profesor.id == id).first()

                return {
                    "nume": profesorData.nume,
                    "telefon": profesorData.telefon,
                    "departament": profesorData.departament
                }

        if userData.rol == Role.SECRETAR.name.lower():

            secretarData = session.query(Secretar).filter(Secretar.id == id).first()

            return {
                "nume": secretarData.nume,
                "telefon": secretarData.telefon,
            }

    except Exception as e:

        raise Exception(f"Error while fetching user: {str(e)}")

    finally:

        session.close()




def get_users_repo():
    """Retrieve a list of students from the database using the SQLAlchemy session."""
    try:

        session = open_session()

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

        raise Exception(f"Error while fetching users: {str(e)}")

    finally:

        session.close()

def get_user_by_id_repo(id):

    try:

        session = open_session()

        user = session.query(Utilizator).filter(Utilizator.id == id).first()

        if user is None:

            raise Exception("User not found", 204)

        return user

    except Exception as e:

        raise Exception(f"Error while fetching user: {str(e)}")

    finally:

        session.close()