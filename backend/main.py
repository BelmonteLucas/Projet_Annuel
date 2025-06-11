print("✅ main.py is running")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Password
import os
import base64
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware

# --- CORRECTED: Read DB password from Docker secret or fallback ---
def get_db_password():
    # Priorité au secret Docker
    docker_secret_path = "/run/secrets/db_password"
    # Fallback pour dev local (non Dockerisé) ou si le secret n'est pas monté
    local_secret_path = "/app/secrets/db_password.txt" # Assurez-vous que ce chemin est correct si vous l'utilisez en dev

    if os.path.exists(docker_secret_path):
        print(f"Reading DB password from Docker secret: {docker_secret_path}")
        return open(docker_secret_path, "r").read().strip()
    elif os.path.exists(local_secret_path):
        print(f"Reading DB password from local file: {local_secret_path}")
        return open(local_secret_path, "r").read().strip()
    else:
        # Essayer de lire à partir de la variable d'environnement comme dernier recours (moins sécurisé)
        # ou lever une exception si aucun mot de passe n'est trouvé.
        # Pour ce projet, nous allons lever une exception si aucun fichier n'est trouvé.
        print(f"ERROR: DB password file not found at {docker_secret_path} or {local_secret_path}")
        raise Exception(f"DB password file not found. Searched in {docker_secret_path} and {local_secret_path}")

DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

try:
    DB_PASSWORD = get_db_password()
except Exception as e:
    print(f"Failed to get DB_PASSWORD: {e}")
    # Gérer l'erreur de manière appropriée, par exemple, en quittant ou en utilisant une valeur par défaut si cela a du sens
    # Pour une application de production, il est préférable de ne pas démarrer si le mot de passe n'est pas disponible.
    raise  # Renvoyer l'exception pour arrêter le démarrage si le mot de passe n'est pas trouvé

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Connecting to database with URL: postgresql://{DB_USER}:********@{DB_HOST}:{DB_PORT}/{DB_NAME}")
# --- END CORRECTED ---

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"], # Ou l'URL de votre frontend
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
    # Gérer l'erreur, par exemple, si la base de données n'est pas accessible

class UserEntry(BaseModel):
    username: str
    password: str

class PasswordEntry(BaseModel):
    user: str # Devrait être l'identifiant de l'utilisateur, pas le currentUser encodé en base64
    site: str
    account: str # Nom du compte pour le site
    password: str # Mot de passe pour le site/compte

class DeleteEntry(BaseModel):
    user: str # Identifiant de l'utilisateur
    site: str
    account: str

class DeleteAllEntry(BaseModel):
    user: str # Identifiant de l'utilisateur

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/register")
def register_user(entry: UserEntry):
    db = Session()
    existing_user = db.query(User).filter_by(username=entry.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    
    hashed_password = get_password_hash(entry.password)
    user = User(username=entry.username, password=hashed_password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"message": "Utilisateur créé avec succès", "user_id": user.id}

# Note: La gestion du 'user' en base64 dans les routes suivantes est une faiblesse de sécurité.
# Idéalement, l'authentification devrait être gérée par des tokens (ex: JWT)
# et l'ID de l'utilisateur extrait du token.
# Pour l'instant, on garde le fonctionnement tel quel mais c'est un point d'amélioration.

def get_username_from_b64(user_b64: str) -> str:
    """Décode le nom d'utilisateur de base64. Lève une HTTPException en cas d'erreur."""
    try:
        # Le frontend envoie "username:password" encodé en b64. Nous n'avons besoin que du username ici.
        decoded_str = base64.b64decode(user_b64).decode("utf-8")
        username = decoded_str.split(":")[0] # Extrait le username avant le ':'
        return username
    except Exception:
        raise HTTPException(status_code=400, detail="Format d'utilisateur invalide (base64)")

@app.post("/add")
def add_password(entry: PasswordEntry):
    db = Session()
    # Le champ 'user' de PasswordEntry est supposé être la chaîne encodée en base64
    # provenant du localStorage 'currentUser'
    username_for_db = get_username_from_b64(entry.user)

    # Vérifie l'unicité (user, site, account)
    existing = db.query(Password).filter_by(user=username_for_db, site=entry.site, account=entry.account).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Ce compte existe déjà pour ce site.")

    pwd = Password(user=username_for_db, site=entry.site, account=entry.account, password=entry.password)
    db.add(pwd)
    db.commit()
    db.refresh(pwd)
    db.close()
    return {"message": "Mot de passe ajouté", "id": pwd.id}

@app.get("/list")
def get_passwords(user: str): # user est la chaîne encodée en base64
    db = Session()
    username_for_db = get_username_from_b64(user)
    
    entries = db.query(Password).filter_by(user=username_for_db).all()
    db.close()
    return {"passwords": [{"site": e.site, "account": e.account, "password": e.password} for e in entries]}

@app.post("/delete")
def delete_password(entry: DeleteEntry):
    db = Session()
    username_for_db = get_username_from_b64(entry.user)

    pwd = db.query(Password).filter_by(user=username_for_db, site=entry.site, account=entry.account).first()
    if pwd:
        db.delete(pwd)
        db.commit()
        db.close()
        return {"message": "Mot de passe supprimé"}
    db.close()
    raise HTTPException(status_code=404, detail="Mot de passe non trouvé")

@app.post("/delete_all")
def delete_all_passwords(entry: DeleteAllEntry):
    db = Session()
    username_for_db = get_username_from_b64(entry.user)

    deleted_count = db.query(Password).filter_by(user=username_for_db).delete()
    db.commit()
    db.close()
    return {"message": f"{deleted_count} mot(s) de passe supprimé(s)"}

# Ajout pour s'assurer que les sessions DB sont fermées
from fastapi import Request
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    try:
        request.state.db = Session()
        response = await call_next(request)
    finally:
        if hasattr(request.state, "db"):
            request.state.db.close()
    return response