from Domain.dbInit import dbInit
import uuid
from Domain.Entities.student import Student
from Domain.Entities.utilizator import Utilizator
from Domain.Entities.profesor import Profesor
from Domain.Entities.secretar import Secretar
from Utils.passwordhash import hash_password
from Utils.sqlcommands import add_row
def create_student_repo(user_data):

    user_id = str(uuid.uuid4())
    cnxn, cursor = dbInit()

    if cnxn and cursor:

        try:

                user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
                user_data['id'] = user_id

                utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'] , 'student')
                student = Student(user_data['id'], user_data['nume'], user_data['telefon'], user_data['facultatea'], user_data['specializarea'], user_data['idGrupa'],False)

                add_row(cursor, "Utilizatori", utilizator)
                add_row(cursor, "Studenti", student)

                return {"message": "Student created successfully"}, 201


        except Exception as e:

            print(f"Error while inserting user: {e}")  # Better error logging
            raise Exception(f"Error while inserting user: {str(e)}")

        finally:
            cursor.close()
            cnxn.close()

    else:

        raise Exception("Error: Database connection not established.")

def create_profesor_repo(user_data):

    user_id = str(uuid.uuid4())
    cnxn, cursor = dbInit()

    if cnxn and cursor:

        try:

                user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
                user_data['id'] = user_id

                utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'] , 'profesor')
                add_row(cursor, "Utilizatori", utilizator)

                profesor = Profesor(user_data['id'], user_data['nume'], user_data['telefon'], user_data['departament'])
                add_row(cursor, "Profesori", profesor)

                return {"message": "Profesor created successfully"}, 201



        except Exception as e:

            print(f"Error while inserting user: {e}")

            return {"error": str(e)}, 400

        finally:

            cursor.close()
            cnxn.close()

    else:

        raise Exception("Error: Database connection not established.")

def create_secretar_repo(user_data):

    user_id = str(uuid.uuid4())
    cnxn, cursor = dbInit()

    if cnxn and cursor:

        try:

                user_data['parola'] = hash_password(user_data['parola']).decode('utf-8')
                user_data['id'] = user_id

                utilizator = Utilizator(user_data['id'], user_data['email'], user_data['parola'] , 'secretar')
                add_row(cursor, "Utilizatori", utilizator)

                secretar = Secretar(user_data['id'], user_data['nume'], user_data['telefon'])
                add_row(cursor, "Secretari", secretar)

                return {"message": "Secretar created successfully"}, 201



        except Exception as e:

            print(f"Error while inserting user: {e}")

            return {"error": str(e)}, 400

        finally:

            cursor.close()
            cnxn.close()

    else:

        raise Exception("Error: Database connection not established.")


def get_users_repo():
    cnxn, cursor = dbInit()

    if cnxn and cursor:
        try:
            cursor.execute("SELECT * FROM Studenti")
            user_data = cursor.fetchall()

            # List to hold user dictionaries
            users_list = []

            # Convert each tuple to a dictionary with appropriate keys
            for row in user_data:
                user_dict = {
                    "id": str(row[0]),
                    "nume": row[1],
                    "telefon": row[2],
                    "facultatea": row[3],
                    "specializarea": row[4],
                    "id_grupa": row[5],
                    "sef": row[6]
                }
                users_list.append(user_dict)

            return users_list

        except Exception as e:
            raise Exception(f"Error while fetching users: {str(e)}")

        finally:
            cursor.close()
            cnxn.close()

    else:
        raise Exception("Error: Database connection not established.")
