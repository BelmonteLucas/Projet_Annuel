from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Utilise un mot de passe crypté ici dans une vraie application

# Si tu veux qu’il soit créé à chaque fois que tu lances le projet
# Base.metadata.create_all(bind=engine)
class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)  # Associe un mot de passe à un utilisateur
    site = Column(String)  # Le nom du site pour lequel on garde un mot de passe
    account = Column(String)  # Identifiant du compte pour le site
    password = Column(String)  # Le mot de passe à stocker

    __table_args__ = (
        UniqueConstraint('user', 'site', 'account', name='uq_user_site_account'),
    )
