import uuid
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Domain.Entities.secretar import Secretar
from Utils.passwordhash import hash_password
from Domain.extensions import sesion

def create_student_repo(user_data):

    user_id = str(uuid.uuid4())

    try:
        # Hash the password and set the user ID
        user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
        user_data['id'] = user_id

        # Create instances of Utilizator and Student
        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'student')
        student = Student(user_data['id'], user_data['nume'], user_data['telefon'],
                          user_data['facultatea'], user_data['specializarea'], user_data['idGrupa'], False)

        # Add instances to the session
        sesion.add(utilizator)
        sesion.add(student)

        # Commit the transaction
        sesion.commit()

        return {"message": "Student created successfully"}, 201

    except Exception as e:
        # Rollback the session in case of any exception
        sesion.rollback()

        if "email" in str(e).lower() and "unique" in str(e).lower():

            return {
                "error": "Email already exists. Please use a different email."}, 409  # 409 Conflict HTTP status code

        print(f"Error while inserting user: {e}")
        raise Exception(f"Error while inserting user: {str(e)}")


def create_profesor_repo(user_data):
    """Create a professor entry in the database using the SQLAlchemy session."""
    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id

    try:
        # Create and add the user entry with 'profesor' role
        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'profesor')
        sesion.add(utilizator)

        # Create and add the professor-specific entry
        profesor = Profesor(user_data['id'], user_data['nume'], user_data['telefon'], user_data['departament'])
        sesion.add(profesor)

        # Commit the transaction
        sesion.commit()
        return {"message": "Profesor created successfully"}, 201

    except Exception as e:
        # Rollback in case of any exception
        sesion.rollback()

        # Check for unique email constraint violation
        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        # Log and re-raise generic exception
        print(f"Error while inserting professor: {e}")
        raise Exception(f"Error while inserting professor: {str(e)}")

def create_secretar_repo(user_data):
    """Create a secretary entry in the database using the SQLAlchemy session."""
    user_id = str(uuid.uuid4())
    user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
    user_data['id'] = user_id

    try:
        # Create and add the user entry with 'secretar' role
        utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'], 'secretar')
        sesion.add(utilizator)

        # Create and add the secretary-specific entry
        secretar = Secretar(user_data['id'], user_data['nume'], user_data['telefon'])
        sesion.add(secretar)

        # Commit the transaction
        sesion.commit()
        return {"message": "Secretar created successfully"}, 201

    except Exception as e:
        # Rollback in case of any exception
        sesion.rollback()

        # Check for unique email constraint violation
        if "email" in str(e).lower() and "unique" in str(e).lower():
            return {"error": "Email already exists. Please use a different email."}, 409

        # Log and re-raise generic exception
        print(f"Error while inserting secretary: {e}")
        raise Exception(f"Error while inserting secretary: {str(e)}")

def get_users_repo():
    """Retrieve a list of students from the database using the SQLAlchemy session."""
    try:
        # Query all students
        students = sesion.query(Student).all()

        # Convert each Student instance to a dictionary
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
