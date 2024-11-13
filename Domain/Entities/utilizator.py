from Domain.extensions import Base
from sqlalchemy import Column, Integer, String

class Utilizator(Base):

    __tablename__ = 'Utilizatori'

    id = Column(String, primary_key=True)
    email = Column(String)
    parola = Column(String)
    rol = Column(String)

    def __init__(self, id, email, parola, rol ):
        self.id = id
        self.email = email
        self.parola = parola
        self.rol = rol
