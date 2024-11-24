from Domain.extensions import open_session
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from Domain.Entities.utilizator import Utilizator
from Utils.passwordhash import hash_password,verify_password

def login_user(accountData):

    try:

        session = open_session()

        username = accountData.get("username")
        password = accountData.get("parola")

        user = session.query(Utilizator).filter(Utilizator.email == username).first()

        if user is None:

            raise ValueError("User not found", 204)

        checkedPass = hash_password(password).decode('utf-8')

        print(user.parola)
        print(checkedPass)

        if not verify_password(password, user.parola):

            raise ValueError("Wrong password", 204)

        userData = {
            "id": user.id,
            "email": user.email,  # Commented out as per your code
            "rol": user.rol
        }

        expires = timedelta(days=30)

        return {
            "Authentication successful": create_access_token(
                identity=userData,
                additional_claims=userData,
                expires_delta=expires
            )
        }, 201

    except ValueError as e:

        message, status_code = e.args if len(e.args) == 2 else ("An error occurred", 400)
        return {"error": message}, status_code

    except Exception as e:

        return {"error": f"Error while logging in user: {str(e)}"}, 500

    finally:

        session.close()