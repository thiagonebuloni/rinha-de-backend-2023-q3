from sqlalchemy import ARRAY, Column, Date, String, Uuid
from .database import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Uuid, primary_key=True, nullable=False)
    apelido = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    nascimento = Column(Date, nullable=False)
    stack = Column(ARRAY(String), nullable=False)
