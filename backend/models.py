"""
Models SQLAlchemy - HoneyPot Pro Max
===================================

DÃ©finition des modÃ¨les de donnÃ©es pour l'application gestionnaire de mots de passe.
- User: Gestion des utilisateurs avec authentification MFA
- Password: Stockage sÃ©curisÃ© des mots de passe utilisateurs

Auteur: Ã‰quipe ESGI 2024-2025
"""
import os
import bcrypt
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Chargement de la clÃ© Fernet
with open("/app/secrets/db_encryption_key.txt", "rb") as f:
    fernet = Fernet(f.read())

Base = declarative_base()

class User(Base):
    """
    ModÃ¨le utilisateur avec support MFA
    ==================================
    
    Stocke les informations d'authentification des utilisateurs incluant :
    - Identifiants de connexion classiques (username/password)
    - Configuration MFA (secret chiffrÃ© + statut d'activation)
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)                    # Identifiant unique auto-incrÃ©mentÃ©
    username = Column(String, unique=True, index=True)                    # Nom d'utilisateur (unique et indexÃ©)
    password = Column(String)                                             # Mot de passe hashÃ© avec bcrypt
    mfa_secret = Column(String, nullable=True)                            # ClÃ© secrÃ¨te MFA chiffrÃ©e avec Fernet
    mfa_enabled = Column(Boolean, default=False)                          # Statut d'activation du MFA

class Password(Base):
    """
    ModÃ¨le Password chiffrÃ©
    ========================
    Stocke les mots de passe chiffrÃ©s Ã  l'aide de Fernet.
    """
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    site = Column(String)
    account = Column(String)
    _password = Column("password", String)  # champs rÃ©el en BDD

    __table_args__ = (
        UniqueConstraint('user', 'site', 'account', name='uq_user_site_account'),
    )

    @property
    def password(self):
        """
        Retourne le mot de passe dÃ©chiffrÃ©
        """
        decrypted = fernet.decrypt(self._password.encode())
        return decrypted.decode()

    @password.setter
    def password(self, plaintext):
        """
        Chiffre le mot de passe en Fernet avant de le stocker
        """
        encrypted = fernet.encrypt(plaintext.encode())
        self._password = encrypted.decode()
