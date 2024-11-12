from Domain.extensions import Base
from sqlalchemy import Column, Integer, String

class Materii(Base):
    __tablename__ = 'Materii'

    # Define columns based on the table structure
    id = Column(String, primary_key=True)
    nume = Column(String)
    abreviere = Column(String)
    tipevaluare = Column(String)
    numarcredite = Column(Integer)
    profesorid = Column(String)

    def __init__(self, Id, Nume, Abreviere, TipEvaluare, NumarCredite, ProfesorTitular):
        self.id = Id
        self.nume = Nume
        self.abreviere = Abreviere
        self.tipevaluare = TipEvaluare
        self.numarcredite = NumarCredite
        self.profesorid = ProfesorTitular
