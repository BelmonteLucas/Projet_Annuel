"""
API Backend - HoneyPot Pro Max
==============================

Service API principal du gestionnaire de mots de passe sécurisé.
Implémente l'authentification MFA, le chiffrement des données et la gestion des mots de passe.

Fonctionnalités principales :
- Authentification utilisateur avec hashage bcrypt
- Authentification à double facteur (TOTP)
- Chiffrement des secrets MFA avec Fernet
- Gestion sécurisée des mots de passe utilisateurs
- API RESTful pour l'interface frontend

Auteur: Équipe ESGI 2024-2025
"""

print("INFO: main.py is running")

# =============================================================================
# IMPORTS ET DÉPENDANCES
# =============================================================================
from fastapi import FastAPI, HTTPException, Request              # Framework API moderne
from pydantic import BaseModel                                   # Validation des données
from sqlalchemy import create_engine                             # ORM pour PostgreSQL
from sqlalchemy.orm import sessionmaker                          # Sessions de base de données
from models import Base, User, Password                          # Modèles de données
import os                                                        # Variables d'environnement
import base64                                                    # Encodage des données
from passlib.context import CryptContext                        # Hashage sécurisé des mots de passe
from fastapi.middleware.cors import CORSMiddleware              # Gestion CORS pour le frontend
import pyotp                                                     # Génération/validation TOTP (MFA)
from typing import Optional                                      # Types optionnels
from cryptography.fernet import Fernet                          # Chiffrement symétrique des secrets MFA

# =============================================================================
# CONFIGURATION DU CHIFFREMENT MFA
# =============================================================================
# Gestion sécurisée de la clé de chiffrement pour les secrets MFA
# Priorité : Docker secrets > fichiers locaux > variables d'environnement

def get_mfa_encryption_key():
    """
    Récupère la clé de chiffrement MFA depuis différentes sources sécurisées.
    
    Ordre de priorité :
    1. Docker secret (/run/secrets/mfa_encryption_key)
    2. Fichier local pour développement
    3. Variable d'environnement (fallback)
    
    Returns:
        bytes: Clé de chiffrement Fernet valide
        
    Raises:
        Exception: Si aucune clé n'est trouvée
    """
    docker_secret_path = "/run/secrets/mfa_encryption_key"        # Production Docker
    local_secret_path = "/app/secrets/mfa_encryption_key.txt"     # Développement local

    if os.path.exists(docker_secret_path):
        print(f"Reading MFA encryption key from Docker secret: {docker_secret_path}")
        return open(docker_secret_path, "r").read().strip().encode() # Conversion en bytes pour Fernet
    elif os.path.exists(local_secret_path):
        print(f"Reading MFA encryption key from local file: {local_secret_path}")
        return open(local_secret_path, "r").read().strip().encode() # Conversion en bytes pour Fernet
    else:
        mfa_key_env = os.getenv("MFA_ENCRYPTION_KEY")
        if mfa_key_env:
            print("Reading MFA encryption key from environment variable MFA_ENCRYPTION_KEY")
            return mfa_key_env.encode()
            return mfa_key_env.encode()
        print(f"ERROR: MFA encryption key file not found at {docker_secret_path} or {local_secret_path}, and MFA_ENCRYPTION_KEY env var not set.")
        raise Exception("MFA_ENCRYPTION_KEY not found.")

# Initialisation du moteur de chiffrement MFA
try:
    MFA_KEY = get_mfa_encryption_key()                            # Récupération de la clé de chiffrement
    FERNET_INSTANCE = Fernet(MFA_KEY)                             # Instance Fernet pour chiffrement/déchiffrement
    print("MFA encryption engine initialized.")
except Exception as e:
    print(f"Failed to initialize MFA encryption: {e}")
    # SÉCURITÉ : Arrêt de l'application si le chiffrement MFA ne peut pas être initialisé
    raise

# =============================================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# =============================================================================
# Gestion sécurisée du mot de passe de base de données PostgreSQL

def get_db_password():
    """
    Récupère le mot de passe de la base de données depuis des sources sécurisées.
    
    Ordre de priorité :
    1. Docker secret (/run/secrets/db_password) - Production
    2. Fichier local pour développement
    
    Returns:
        str: Mot de passe de la base de données
        
    Raises:
        Exception: Si aucun mot de passe n'est trouvé
    """
    docker_secret_path = "/run/secrets/db_password"               # Chemin Docker secret (production)
    local_secret_path = "/app/secrets/db_password.txt"            # Fichier local (développement)

    if os.path.exists(docker_secret_path):
        print(f"Reading DB password from Docker secret: {docker_secret_path}")
        return open(docker_secret_path, "r").read().strip()
    elif os.path.exists(local_secret_path):
        print(f"Reading DB password from local file: {local_secret_path}")
        return open(local_secret_path, "r").read().strip()
    else:
        print(f"ERROR: DB password file not found at {docker_secret_path} or {local_secret_path}")
        raise Exception(f"DB password file not found. Searched in {docker_secret_path} and {local_secret_path}")

# Configuration des paramètres de connexion PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")                       # Utilisateur PostgreSQL (défaut: postgres)
DB_HOST = os.getenv("DB_HOST", "db")                             # Hôte PostgreSQL (service Docker: db)
DB_PORT = os.getenv("DB_PORT", "5432")                           # Port PostgreSQL (défaut: 5432)
DB_NAME = os.getenv("DB_NAME", "postgres")

try:
    DB_PASSWORD = get_db_password()
except Exception as e:
    print(f"Failed to get DB_PASSWORD: {e}")
    raise

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Connecting to database with URL: postgresql://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9080", "https://localhost:9443", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified.")
except Exception as e:
    print(f"Error creating database tables: {e}")

class UserEntry(BaseModel): 
    username: str
    password: str

class PasswordEntry(BaseModel):
    user: str 
    site: str
    account: str 
    password: str 

class DeleteEntry(BaseModel):
    user: str 
    site: str
    account: str

class DeleteAllEntry(BaseModel):
    user: str

class MfaSetupRequest(BaseModel):
    user: str

class MfaVerifyRequest(BaseModel):
    user: str 
    otp_code: str

class LoginResponse(BaseModel):
    message: str
    mfa_required: bool
    username: Optional[str] = None
    user_b64_token: Optional[str] = None

class MfaLoginOtpRequest(BaseModel):
    username: str
    otp_code: str

class MfaStatusRequest(BaseModel):
    username: str
    password: str

class MfaDisableRequest(BaseModel):
    user: str
    otp_code: str

def get_username_from_b64(user_b64: str) -> str:
    try:
        decoded_str = base64.b64decode(user_b64).decode("utf-8")
        username = decoded_str.split(":")[0]
        return username
    except Exception:
        raise HTTPException(status_code=400, detail="Format d'utilisateur invalide (base64)")

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/register")
def register_user(entry: UserEntry):
    db = Session()
    try:
        existing_user = db.query(User).filter_by(username=entry.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
        
        hashed_password = get_password_hash(entry.password)
        user = User(username=entry.username, password=hashed_password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "Utilisateur créé avec succès", "user_id": user.id}
    finally:
        db.close()

@app.post("/login", response_model=LoginResponse)
def login_user(entry: UserEntry):
    db = Session()
    try:
        user_from_db = db.query(User).filter_by(username=entry.username).first()

        if not user_from_db:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if not verify_password(entry.password, user_from_db.password):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

        if user_from_db.mfa_enabled:
            return LoginResponse(
                message="MFA OTP requis", 
                mfa_required=True, 
                username=user_from_db.username
            )
        else:
            user_b64_token_str = f"{entry.username}:{entry.password}"
            user_b64_token = base64.b64encode(user_b64_token_str.encode("utf-8")).decode("utf-8")
            return LoginResponse(
                message="Connexion réussie", 
                mfa_required=False, 
                username=user_from_db.username,
                user_b64_token=user_b64_token
            )
    finally:
        db.close()

@app.post("/login/otp")
def login_otp_verify(request_data: MfaLoginOtpRequest):
    db = Session()
    try:
        user = db.query(User).filter_by(username=request_data.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if not user.mfa_enabled or not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA non activé ou non configuré pour cet utilisateur.")
        
        try:
            decrypted_mfa_secret = FERNET_INSTANCE.decrypt(user.mfa_secret.encode()).decode()
        except Exception: # Inclut InvalidToken de Fernet
            # Potentiellement logguer l'erreur ici pour investiguer
            raise HTTPException(status_code=500, detail="Erreur lors du déchiffrement du secret MFA.")

        totp = pyotp.TOTP(decrypted_mfa_secret)
        if totp.verify(request_data.otp_code):
            return {"message": "Vérification OTP réussie. Connexion autorisée."}
        else:
            raise HTTPException(status_code=401, detail="Code OTP invalide.")
    finally:
        db.close()

@app.post("/add")
def add_password(entry: PasswordEntry):
    db = Session()
    try:
        username_for_db = get_username_from_b64(entry.user)
        existing = db.query(Password).filter_by(user=username_for_db, site=entry.site, account=entry.account).first()
        if existing:
            raise HTTPException(status_code=400, detail="Ce compte existe déjà pour ce site.")

        pwd = Password(user=username_for_db, site=entry.site, account=entry.account, password=entry.password)
        db.add(pwd)
        db.commit()
        db.refresh(pwd)
        return {"message": "Mot de passe ajouté", "id": pwd.id}
    finally:
        db.close()

@app.get("/list")
def get_passwords(user: str):
    db = Session()
    try:
        username_for_db = get_username_from_b64(user)
        entries = db.query(Password).filter_by(user=username_for_db).all()
        return {"passwords": [{"site": e.site, "account": e.account, "password": e.password} for e in entries]}
    finally:
        db.close()
    
@app.post("/delete")
def delete_password(entry: DeleteEntry):
    db = Session()
    try:
        username_for_db = get_username_from_b64(entry.user)
        pwd = db.query(Password).filter_by(user=username_for_db, site=entry.site, account=entry.account).first()
        if pwd:
            db.delete(pwd)
            db.commit()
            return {"message": "Mot de passe supprimé"}
        raise HTTPException(status_code=404, detail="Mot de passe non trouvé")
    finally:
        db.close()

@app.post("/delete_all")
def delete_all_passwords(entry: DeleteAllEntry):
    db = Session()
    try:
        username_for_db = get_username_from_b64(entry.user)
        deleted_count = db.query(Password).filter_by(user=username_for_db).delete()
        db.commit()
        return {"message": f"{deleted_count} mot(s) de passe supprimé(s)"}
    finally:
        db.close()

@app.post("/mfa/setup")
def mfa_setup(request_data: MfaSetupRequest):
    db = Session()
    try:
        username = get_username_from_b64(request_data.user)
        user = db.query(User).filter_by(username=username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if user.mfa_enabled:
            raise HTTPException(status_code=400, detail="Le MFA est déjà activé pour cet utilisateur.")

        plain_mfa_secret = pyotp.random_base32()
        encrypted_mfa_secret = FERNET_INSTANCE.encrypt(plain_mfa_secret.encode()).decode() # Chiffrer et stocker en string

        user.mfa_secret = encrypted_mfa_secret # Stocker le secret chiffré
        db.commit()
        db.refresh(user)

        # L'URI de provisioning utilise le secret en clair, NON chiffré
        totp = pyotp.TOTP(plain_mfa_secret) 
        provisioning_uri = totp.provisioning_uri(
            name=user.username, 
            issuer_name="ProjetAnnuelESGI" 
        )
        return {"provisioning_uri": provisioning_uri, "message": "Scannez le QR code avec votre application MFA et vérifiez."}
    finally:
        db.close()

@app.post("/mfa/verify")
def mfa_verify(request_data: MfaVerifyRequest):
    db = Session()
    try:
        username = get_username_from_b64(request_data.user)
        user = db.query(User).filter_by(username=username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if not user.mfa_secret: # Le secret stocké est chiffré
            raise HTTPException(status_code=400, detail="MFA non initialisé pour cet utilisateur. Veuillez d'abord utiliser /mfa/setup.")

        try:
            decrypted_mfa_secret = FERNET_INSTANCE.decrypt(user.mfa_secret.encode()).decode()
        except Exception: # Inclut InvalidToken de Fernet
             # Potentiellement logguer l'erreur ici pour investiguer
            raise HTTPException(status_code=500, detail="Erreur lors du déchiffrement du secret MFA pour la vérification.")

        totp = pyotp.TOTP(decrypted_mfa_secret)
        if totp.verify(request_data.otp_code):
            if not user.mfa_enabled:
                user.mfa_enabled = True
                db.commit()
                db.refresh(user)
            return {"message": "Code OTP valide. MFA activé avec succès."}
        else:
            raise HTTPException(status_code=400, detail="Code OTP invalide.")
    finally:
        db.close()

@app.post("/mfa/status")
def mfa_status(request_data: MfaStatusRequest):
    db = Session()
    try:
        user = db.query(User).filter_by(username=request_data.username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        # Vérifier le mot de passe
        if not verify_password(request_data.password, user.password):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

        return {
            "mfa_enabled": user.mfa_enabled if user.mfa_enabled else False,
            "setup_date": user.created_at.isoformat() if user.mfa_enabled and hasattr(user, 'created_at') else None
        }
    finally:
        db.close()

@app.post("/mfa/disable")
def mfa_disable(request_data: MfaDisableRequest):
    db = Session()
    try:
        username = get_username_from_b64(request_data.user)
        user = db.query(User).filter_by(username=username).first()

        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        if not user.mfa_enabled or not user.mfa_secret:
            raise HTTPException(status_code=400, detail="MFA non activé pour cet utilisateur.")

        try:
            decrypted_mfa_secret = FERNET_INSTANCE.decrypt(user.mfa_secret.encode()).decode()
        except Exception:
            raise HTTPException(status_code=500, detail="Erreur lors du déchiffrement du secret MFA.")

        totp = pyotp.TOTP(decrypted_mfa_secret)
        if totp.verify(request_data.otp_code):
            user.mfa_enabled = False
            user.mfa_secret = None
            db.commit()
            db.refresh(user)
            return {"success": True, "message": "MFA désactivé avec succès."}
        else:
            raise HTTPException(status_code=400, detail="Code OTP invalide.")
    finally:
        db.close()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    # Si vous décidez de gérer les sessions via middleware, vous initialiseriez et fermeriez la session ici.
    # Pour l'instant, les routes gèrent explicitement leurs sessions.
    # Ce middleware peut être utilisé pour d'autres logiques transversales si besoin.
    # Pour éviter des conflits avec la gestion manuelle dans les routes, on le laisse simple.
    # request.state.db = Session() # Exemple si on voulait injecter
    try:
        response = await call_next(request)
    finally:
        # if hasattr(request.state, "db"): # Exemple si on voulait fermer la session injectée
        #    request.state.db.close()
        pass # Laisser les routes gérer leur session
    return response