from sqlalchemy import Column, String
from Domain.extensions import Base
class Sali(Base):
    __tablename__ = 'Sali'

    id = Column(String(50), primary_key=True)
    nume = Column(String(200), nullable=False)
    departament = Column(String(100), nullable=False)

    def __init__(self, Id, Nume, Departament):
        self.id = Id
        self.nume = Nume
        self.departament = Departament
