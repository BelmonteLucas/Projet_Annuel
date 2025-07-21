# =============================================================================
# DOCKERFILE BACKEND - HoneyPot Pro Max
# =============================================================================
# Image Docker pour l'API backend Python/FastAPI
# Optimisée pour la sécurité et les performances en production
# =============================================================================

# Image de base Python slim pour réduire la surface d'attaque et la taille
FROM python:3.11-slim  
# Image officielle Python 3.11 avec packages système minimaux

# =============================================================================
# CONFIGURATION DE L'ENVIRONNEMENT PYTHON
# =============================================================================
ENV PYTHONDONTWRITEBYTECODE=1 
# Empêche Python d'écrire des fichiers .pyc (améliore sécurité et performance)

ENV PYTHONUNBUFFERED=1    
# Force les flux stdout/stderr à être non bufferisés (logs temps réel dans Docker)

# =============================================================================
# CONFIGURATION DU RÉPERTOIRE DE TRAVAIL
# =============================================================================
WORKDIR /app
# Répertoire de travail pour tous les fichiers de l'application

# =============================================================================
# INSTALLATION DES DÉPENDANCES PYTHON
# =============================================================================
# Copie séparée de requirements.txt pour optimiser le cache Docker
# (les dépendances changent moins souvent que le code)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Installation sans cache pour réduire la taille de l'image

# =============================================================================
# COPIE DU CODE SOURCE
# =============================================================================
# Copie de tout le code source de l'application
# Note : .dockerignore doit exclure .git, venv, __pycache__, etc.
COPY . /app

# =============================================================================
# CONFIGURATION DES SCRIPTS ET PERMISSIONS
# =============================================================================
# Script d'attente pour la base de données (évite les erreurs de connexion)
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh
# Rend le script exécutable pour attendre que PostgreSQL soit prêt

# =============================================================================
# EXPOSITION DU PORT
# =============================================================================
EXPOSE 8000
# Port sur lequel l'API FastAPI sera accessible

# =============================================================================
# COMMANDE DE DÉMARRAGE
# =============================================================================
# Démarre l'application avec attente de la base de données
# Utilise Uvicorn comme serveur ASGI pour FastAPI
CMD ["/app/wait-for-it.sh", "db:5432", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]