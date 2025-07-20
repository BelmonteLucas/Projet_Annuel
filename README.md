# Gestionnaire de mots de passe – Projet Annuel ESGI

Bienvenue ! Ce dépôt propose une application web complète pour gérer vos mots de passe de façon sécurisée et simple à installer, incluant désormais l'authentification à deux facteurs (MFA).

---

## 🚀 Présentation

Ce gestionnaire de mots de passe vous permet de :
- Créer un compte personnel sécurisé.
- Activer l'authentification à deux facteurs (MFA/2FA) avec une application d'authentification (TOTP).
- Ajouter, lister et supprimer vos mots de passe pour différents sites.
- Accéder à une interface web moderne et intuitive.

L’application repose sur :
- **Frontend** : Application web statique (HTML/CSS/JS)
- **Backend** : API FastAPI (Python) avec support MFA (`pyotp`, `cryptography`).
- **Base de données** : PostgreSQL
- **Administration** : pgAdmin

Le tout fonctionne grâce à **Docker** pour une installation rapide, sans configuration complexe.

---

## 🛠️ Installation rapide

### 1. Cloner le dépôt

```sh
git clone https://github.com/BelmonteLucas/Projet_Annuel.git
cd Projet_Annuel
```

### 2. Prérequis

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3](https://www.python.org/) (pour le script de configuration de l'environnement de développement et pour le backend).
  - Les dépendances Python du backend (`fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `python-dotenv`, `passlib[bcrypt]`, `pyotp`, `qrcode[pil]`, `cryptography`) seront installées dans l'image Docker. Pour le script de configuration, `cryptography` pourrait être nécessaire localement.

### 3. Configuration de l'environnement de développement local

Après avoir cloné le dépôt :

**a. Installez les dépendances de développement (nécessaires pour le script de configuration) :**
Ouvrez un terminal à la racine du projet et exécutez :
```sh
pip install -r requirements-dev.txt
# ou python3 -m pip install -r requirements-dev.txt
```
Cela installera `cryptography` et d'autres outils de développement si nous en ajoutons.

**b. Lancez le script de configuration principal :**
```sh
python setup_dev_environment.py 
# ou python3 setup_dev_environment.py
```
Ce script va :
- Créer un répertoire `secrets/` s'il n'existe pas.
- Générer un fichier `secrets/mfa_encryption_key.txt` avec une clé de chiffrement unique pour votre instance locale (ce fichier est ignoré par Git). Cette clé est **essentielle** pour le fonctionnement du MFA.
- Vous rappeler de créer `secrets/db_password.txt` si ce n'est pas déjà fait.

### 4. Configuration du mot de passe de la base de données

Le mot de passe de la base de données est **centralisé et sécurisé** dans le fichier :
`secrets/db_password.txt`

- **Écrivez le mot de passe souhaité sur la première ligne du fichier** (pas de commentaire sur la première ligne).
- Ce mot de passe sera utilisé automatiquement par :
  - **PostgreSQL** (service `db`)
  - **Le backend** (service `backend`)
  - **pgAdmin** (service `pgadmin`, accès sans saisie manuelle du mot de passe)

**Exemple (`secrets/db_password.txt`):**
```
monSuperMotDePasse2024!
```

### 5. Clé de chiffrement MFA (pour information)

La clé `secrets/mfa_encryption_key.txt` (générée par `setup_dev_environment.py` pour le développement local) est utilisée pour chiffrer les secrets MFA des utilisateurs en base de données.
- **Ne commitez jamais ce fichier.** Il est déjà dans `.gitignore`.
- Pour un déploiement en **production**, cette clé doit être générée une seule fois, stockée de manière extrêmement sécurisée et fournie au backend via des secrets Docker ou des variables d'environnement (comme configuré dans `docker-compose.yml` et lu par `main.py`).

Pour changer le mot de passe de la base de données ou la clé MFA (ce qui invaliderait les secrets MFA existants) :
1. Modifiez le fichier correspondant dans `secrets/`.
2. Supprimez les volumes Docker pour réinitialiser la base et potentiellement les données utilisateur :
   ```sh
   docker-compose down -v
   ```
3. Relancez l’application (cela reconstruira les images si nécessaire) :
   ```sh
   docker-compose up -d --build
   ```

> **Astuce :**
> pgAdmin est déjà préconfiguré pour se connecter à la base sans avoir à saisir le mot de passe, grâce à la génération dynamique du fichier `.pgpass`.

---

## ▶️ Lancer l’application

1. Assurez-vous d'avoir configuré `secrets/db_password.txt` et que `secrets/mfa_encryption_key.txt` a été généré (via `python setup_dev_environment.py`).
2. Ouvrez un terminal dans le dossier du projet.
3. Lancez :
   ```sh
   docker-compose up -d --build
   ```
   L'option `--build` est recommandée la première fois ou après des modifications dans `Dockerfile` ou `requirements.txt`.
4. Attendez que tous les services soient démarrés.

---

## 🌐 Accéder à l’application

- **Interface web (frontend via Nginx/HTTPS)** :  
  [https://localhost/](https://localhost/)  
  - Le frontend est désormais servi par **Nginx** en HTTPS.
  - Le point d’entrée est `frontend/index.html`.
  - Les fichiers statiques utilisés sont :
    - `frontend/index.html`
    - `frontend/app.js`
    - `frontend/style.css`
    - (et autres ressources éventuelles dans `frontend/`)

- **API (FastAPI)** :  
  [http://localhost:8000](http://localhost:8000)  
  - Documentation Swagger : [http://localhost:8000/docs](http://localhost:8000/docs)

- **pgAdmin (gestion base de données)** :  
  [http://localhost:5050](http://localhost:5050)  
  - Email : `admin@admin.com`
  - Mot de passe : `admin`
  - Pour se connecter au serveur PostgreSQL :  
    - Host : `db`
    - Port : `5432`
    - Username : `postgres`
    - Password : (votre mot de passe défini dans `secrets/db_password.txt`)

---

## 📁 Structure du frontend

- `frontend/index.html` : page principale du gestionnaire de mots de passe.
- `frontend/app.js` : logique JavaScript pour l’interface et les appels API.
- `frontend/style.css` : styles CSS personnalisés.
- Les fichiers sont servis par Nginx (voir configuration dans `nginx.conf`, `nginx.crt`, `nginx.key`).

---

## ✨ Fonctionnalités MFA

- **Activation du MFA :** Depuis l'interface utilisateur (une fois connectée), un utilisateur peut choisir d'activer le MFA. Un QR code sera affiché pour être scanné par une application d'authentification (Google Authenticator, Authy, etc.). Une vérification par code OTP est requise pour finaliser l'activation.
- **Connexion avec MFA :** Si le MFA est activé, après avoir entré son nom d'utilisateur et son mot de passe, l'utilisateur devra fournir un code OTP de son application d'authentification pour se connecter.
- **Sécurité :** Le secret MFA de chaque utilisateur est stocké chiffré en base de données à l'aide de la clé `MFA_ENCRYPTION_KEY`.

---

## 🧪 Tester l’application

- Vérifiez que tous les conteneurs sont "Up" :
   ```sh
   docker ps
   ```
- Ouvrez l’interface web, créez un compte.
- Essayez d'activer le MFA, déconnectez-vous, puis reconnectez-vous en utilisant le code OTP.
- Ajoutez et supprimez des mots de passe.

---

## 🧑‍💻 Pour les développeurs

Après avoir cloné le dépôt :
1. Exécutez `python setup_dev_environment.py` pour initialiser les fichiers secrets locaux nécessaires.
2. Assurez-vous que les dépendances Python (listées dans `backend/requirements.txt`) sont disponibles pour votre interpréteur local si vous souhaitez exécuter le backend en dehors de Docker ou si vous avez besoin de `cryptography` pour le script de setup.
3. Utilisez `docker-compose up -d --build` pour lancer l'environnement.

---

## Besoin d’aide ?

- Consultez la documentation du projet pour plus de détails.
- Pour toute question ou problème, ouvrez une issue sur GitHub.

---