from flask_restx import Api
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager

jwt = JWTManager()

authorizations = {
    "jsonWebToken": {"type": "apiKey", "in": "header", "name": "Authorization"}
}

url_object = URL.create(
    drivername="mssql+pyodbc",
    username="student@syncsquad",
    password="Suceava2024",
    host="syncsquad.database.windows.net",
    port=1433,
    database="ipsync",
    query={
        "driver": "ODBC Driver 17 for SQL Server",  # specify the ODBC driver here
        "Encrypt": "yes",
        "TrustServerCertificate": "no",
        "Connection Timeout": "30"
    }
)



Base = declarative_base()
engine = create_engine(url_object)
salt = bcrypt.gensalt()
api = Api()

def open_session():

    Sesion = sessionmaker(bind=engine)
    session = Sesion()

    return session