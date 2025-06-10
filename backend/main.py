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

# --- NEW: Read DB password from secrets file and build DATABASE_URL ---
def get_db_password():
    # Chemin absolu dans le conteneur Docker
    return open("/app/secrets/db_password.txt", "r").read().strip()

DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PASSWORD = get_db_password()
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# --- END NEW ---

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

Base.metadata.create_all(bind=engine)

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

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/register")
def register_user(entry: UserEntry):
    db = Session()
    existing_user = db.query(User).filter_by(username=entry.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    
    hashed_password = get_password_hash(entry.password)
    user = User(username=entry.username, password=hashed_password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Utilisateur créé avec succès", "user_id": user.id}

@app.post("/add")
def add_password(entry: PasswordEntry):
    db = Session()
    try:
        decoded_user = base64.b64decode(entry.user).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur invalide")

    # Vérifie l'unicité (user, site, account)
    existing = db.query(Password).filter_by(user=decoded_user, site=entry.site, account=entry.account).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ce compte existe déjà pour ce site.")

    pwd = Password(user=decoded_user, site=entry.site, account=entry.account, password=entry.password)
    db.add(pwd)
    db.commit()
    db.refresh(pwd)
    return {"message": "Mot de passe ajouté", "id": pwd.id}

@app.get("/list")
def get_passwords(user: str):
    try:
        decoded_user = base64.b64decode(user).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur invalide")

    db = Session()
    entries = db.query(Password).filter_by(user=decoded_user).all()
    return {"passwords": [{"site": e.site, "account": e.account, "password": e.password} for e in entries]}

@app.post("/delete")
def delete_password(entry: DeleteEntry):
    db = Session()
    try:
        decoded_user = base64.b64decode(entry.user).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur invalide")

    pwd = db.query(Password).filter_by(user=decoded_user, site=entry.site, account=entry.account).first()
    if pwd:
        db.delete(pwd)
        db.commit()
        return {"message": "Mot de passe supprimé"}
    raise HTTPException(status_code=404, detail="Mot de passe non trouvé")

@app.post("/delete_all")
def delete_all_passwords(entry: DeleteAllEntry):
    db = Session()
    try:
        decoded_user = base64.b64decode(entry.user).decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur invalide")

    deleted = db.query(Password).filter_by(user=decoded_user).delete()
    db.commit()
    return {"message": f"{deleted} mot(s) de passe supprimé(s)"}
