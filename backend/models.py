"""
Models SQLAlchemy - HoneyPot Pro Max
===================================

Définition des modèles de données pour l'application gestionnaire de mots de passe.
- User: Gestion des utilisateurs avec authentification MFA
- Password: Stockage sécurisé des mots de passe utilisateurs

Auteur: Équipe ESGI 2024-2025
"""

from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """
    Modèle utilisateur avec support MFA
    ==================================
    
    Stocke les informations d'authentification des utilisateurs incluant :
    - Identifiants de connexion classiques (username/password)
    - Configuration MFA (secret chiffré + statut d'activation)
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)                    # Identifiant unique auto-incrémenté
    username = Column(String, unique=True, index=True)                    # Nom d'utilisateur (unique et indexé)
    password = Column(String)                                             # Mot de passe hashé avec bcrypt
    mfa_secret = Column(String, nullable=True)                            # Clé secrète MFA chiffrée avec Fernet
    mfa_enabled = Column(Boolean, default=False)                          # Statut d'activation du MFA

class Password(Base):
    """
    Modèle de stockage des mots de passe
    ===================================
    
    Stocke les mots de passe chiffrés des utilisateurs pour différents services.
    Contrainte d'unicité sur (user, site, account) pour éviter les doublons.
    """
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, index=True)                    # Identifiant unique auto-incrémenté
    user = Column(String, index=True)                                     # Propriétaire du mot de passe (indexé)
    site = Column(String)                                                 # Nom du service/site web
    account = Column(String)                                              # Identifiant du compte sur le site
    password = Column(String)                                             # Mot de passe chiffré

    # Contrainte d'unicité pour éviter les doublons
    __table_args__ = (
        UniqueConstraint('user', 'site', 'account', name='uq_user_site_account'),
    )
