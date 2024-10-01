from Domain.dbInit import dbInit
import uuid

def createUserRepo(user_data):

    user_id = str(uuid.uuid4())

    cnxn, cursor = dbInit()

    if cnxn and cursor:
        try:

            cursor.execute(
                f"INSERT INTO Users (id, nume, prenume, password) VALUES ('{user_id}', '{user_data['nume']}', '{user_data['prenume']}', '{user_data['password']}')"
            )
            cnxn.commit()
            user_data["id"] = user_id

            return user_data

        except Exception as e:

            raise Exception(f"Error while inserting user: {str(e)}")

        finally:
            cursor.close()
            cnxn.close()

    else:

        raise Exception("Error: Database connection not established.")