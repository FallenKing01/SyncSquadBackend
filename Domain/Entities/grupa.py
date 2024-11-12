from sqlalchemy import Column, String
from Domain.extensions import Base

class Grupe(Base):

    __tablename__ = 'Grupe'

    id = Column(String(50), primary_key=True)
    grupa = Column(String(20), nullable=False)

    def __init__(self, id, grupa):
        self.id = id
        self.grupa = grupa
