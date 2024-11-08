from sqlalchemy import Column, Integer, String
from Domain.extensions import Base

class Secretar(Base):

    __tablename__ = 'Secretari'
    id = Column(String, primary_key=True)
    nume = Column(String)
    telefon = Column(String)

    def __init__(self, id, nume, telefon):
        self.id = id
        self.nume = nume
        self.telefon = telefon