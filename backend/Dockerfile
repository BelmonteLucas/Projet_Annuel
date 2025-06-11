FROM python:3.11-slim  
# Utilisation dune image slim pour réduire la taille

ENV PYTHONDONTWRITEBYTECODE 1 
# Empêche Python d'écrire des fichiers .pyc
ENV PYTHONUNBUFFERED 1    
# Force les flux stdout/stderr à être non bufferisés (utile pour les logs Docker)

WORKDIR /app

# Copier uniquement requirements.txt pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
# Assurez-vous que .dockerignore est configuré pour exclure les fichiers non nécessaires (ex: .git, venv, etc.)
COPY . /app

# Le fichier wait-for-it.sh doit être dans le contexte de build (dossier backend)
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# La ligne "COPY ../secrets /app/secrets" a été supprimée car les secrets sont gérés par Docker Compose

# Exposer le port sur lequel l'application s'exécute
EXPOSE 8000

# Commande pour démarrer l'application
# Utilise wait-for-it.sh pour attendre que la base de données soit prête
CMD ["/app/wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]