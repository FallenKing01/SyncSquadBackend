from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class SaliCereri(Base):

    __tablename__ = 'SaliCereri'

    id = Column(String, primary_key=True)
    idcerere = Column(String, nullable=False)
    idsala = Column(String, nullable=False)

    def __init__(self, id, idcerere, idsala):

        self.id = id
        self.idcerere = idcerere
        self.idsala = idsala