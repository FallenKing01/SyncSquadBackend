from sqlalchemy import Column, String, DateTime, Date
from Domain.extensions import Base
class Examene(Base):
    __tablename__ = 'Examene'

    id = Column(String(50), primary_key=True)
    profesorid = Column(String(50), nullable=False)
    sefid = Column(String(50), nullable=False)
    materieid = Column(String(50), nullable=True)
    asistentid = Column(String(50), nullable=True)
    orastart = Column(DateTime, nullable=True)
    orafinal = Column(DateTime, nullable=True)
    data = Column(Date, nullable=True)
    starea = Column(String(50), nullable=True)
    actualizatde = Column(String(50), nullable=True)
    actualizatla = Column(Date, nullable=False)

    def __init__(self, Id, ProfesorId, SefId, MaterieId=None, AsistentId=None,
                 OraStart=None, OraFinal=None, Data=None, Starea=None,
                 ActualizatDe=None, ActualizatLa=None):

        self.id = Id
        self.profesorid = ProfesorId
        self.sefid = SefId
        self.materieid = MaterieId
        self.asistentid = AsistentId
        self.orastart = OraStart
        self.orafinal = OraFinal
        self.data = Data
        self.starea = Starea
        self.actualizatde = ActualizatDe
        self.actualizatla = ActualizatLa
