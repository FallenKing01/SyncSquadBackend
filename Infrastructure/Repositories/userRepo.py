from Domain.dbInit import dbInit
import uuid

def create_user_repo(user_data):

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

def get_users_repo():
    cnxn, cursor = dbInit()

    if cnxn and cursor:
        try:
            cursor.execute("SELECT id, nume, prenume, password FROM Users")
            user_data = cursor.fetchall()

            # List to hold user dictionaries
            users_list = []

            # Convert each tuple to a dictionary with appropriate keys
            for row in user_data:
                user_dict = {
                    "id": str(row[0]),        # Convert UUID to string
                    "nume": row[1],
                    "prenume": row[2],
                    "password": row[3]         # You might want to hash passwords or avoid returning them
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
