from sqlalchemy import Column, Integer, String
from Domain.extensions import Base

class Student(Base):

    __tablename__ = 'Studenti'

    id = Column(String, primary_key=True)
    nume = Column(String)
    telefon = Column(String)
    facultatea = Column(String)
    specializarea = Column(String)
    idgrupa = Column(String)
    sef = Column(Integer)

    def __init__(self, id, nume, telefon, facultatea, specializarea, idgrupa , sef ):
        self.id = id
        self.nume = nume
        self.telefon = telefon
        self.facultatea = facultatea
        self.specializarea = specializarea
        self.idgrupa = idgrupa
        self.sef = sef
