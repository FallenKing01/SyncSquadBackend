from sqlalchemy import Column, String
from Domain.extensions import Base


class Asistenti(Base):

    __tablename__ = 'Asistenti'

    id = Column(String(50), primary_key=True)
    idprof = Column(String(50), nullable=False)
    idasistent = Column(String(50), nullable=False)

    def __init__(self, Id, IdProf, IdAsistent):
        self.id = Id
        self.idprof = IdProf
        self.idasistent = IdAsistent

