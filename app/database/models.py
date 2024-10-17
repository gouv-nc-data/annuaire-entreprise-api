from app.database.connection import Base

from sqlalchemy import Column, String, Integer


class Entreprise(Base):
    __tablename__ = "entreprise"

    id = Column(Integer, primary_key=True)
    rid = Column(String, unique=True)
    sigle = Column(String)
    enseigne = Column(String)
    forme_juridique = Column(String)
    adresse = Column(String)
    code_postal = Column(String)
    ville = Column(String)
