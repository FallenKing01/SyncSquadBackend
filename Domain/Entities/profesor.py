from sqlalchemy import Column, Integer, String
from Domain.extensions import Base

class Profesor(Base):

    __tablename__ = 'Profesori'

    id = Column(String, primary_key=True)
    nume = Column(String)
    telefon = Column(String)
    departament = Column(String)

    def __init__(self, id, nume, telefon, departament):
        self.id = id
        self.nume = nume
        self.telefon = telefon
        self.departament = departament