# Gestionnaire de mots de passe – Projet Annuel ESGI

Bienvenue ! Ce dépôt propose une application web complète pour gérer vos mots de passe de façon sécurisée et simple à installer.

---

## 🚀 Présentation

Ce gestionnaire de mots de passe vous permet de :
- Créer un compte personnel sécurisé
- Ajouter, lister et supprimer vos mots de passe pour différents sites
- Accéder à une interface web moderne et intuitive

L’application repose sur :
- **Frontend** : Application web statique (HTML/CSS/JS)
- **Backend** : API FastAPI (Python)
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

### 3. Configuration du mot de passe de la base de données

Un fichier d’exemple est déjà présent :  
`/secrets/db_password.txt`

**Avant de lancer l’application, modifiez ce fichier et mettez-y un mot de passe fort de votre choix.**

1. Ouvrez `secrets/db_password.txt`
2. Remplacez le contenu par votre mot de passe (ex : `MonMotDePasseSecurise2024!`)
3. Ce fichier est ignoré par git après le clonage, vos modifications restent privées.
4. Utilisez ce mot de passe pour accéder à la base PostgreSQL via pgAdmin.

> ⚠️ Si vous changez ce mot de passe, supprimez les volumes Docker pour réinitialiser la base, puis relancez les conteneurs.

---

## ▶️ Lancer l’application

1. Ouvrez un terminal dans le dossier du projet.
2. Lancez :
   ```sh
   docker-compose up -d
   ```
3. Attendez que tous les services soient démarrés.

---

## 🌐 Accéder à l’application

- **Interface web** :  
  [http://localhost:5500/Gestionnaire_mdp.html](http://localhost:5500/Gestionnaire_mdp.html)

- **API (FastAPI)** :  
  [http://localhost:8000](http://localhost:8000)

- **pgAdmin (gestion base de données)** :  
  [http://localhost:5050](http://localhost:5050)  
  - Email : `admin@admin.com`
  - Mot de passe : `admin`
  - Pour se connecter au serveur PostgreSQL :  
    - Host : `db`
    - Port : `5432`
    - Username : `postgres`
    - Password : (votre mot de passe défini dans `db_password.txt`)

---

## 🧪 Tester l’application

- Vérifiez que tous les conteneurs sont "Up" :
   ```sh
   docker ps
   ```
- Ouvrez l’interface web, créez un compte, ajoutez et supprimez des mots de passe.

---

## Besoin d’aide ?

- Consultez la documentation du projet pour plus de détails.
- Pour toute question ou problème, ouvrez une issue sur GitHub.

---

# Projet_Annuel

## Installation et mise en place de l'application

### 1. Télécharger le projet

- Cliquez sur le bouton **"Code"** de la page GitHub du projet, puis **Download ZIP**.
- Décompressez l'archive ZIP sur votre ordinateur.
- Ou bien, clonez le dépôt avec :
  ```sh
  git clone https://github.com/BelmonteLucas/Projet_Annuel.git
  ```

### 2. Prérequis

- [Docker](https://www.docker.com/products/docker-desktop) et [Docker Compose](https://docs.docker.com/compose/) installés sur votre machine.

### 3. Lancer le projet avec Docker

1. Ouvrez un terminal.
2. Placez-vous dans le dossier contenant `docker-compose.yml` :

   ```sh
   cd "c:\chemin_vers_le_dossier\Projet_Annuel"
   ```

3. Lancez la commande :

   ```sh
   docker-compose up -d
   ```

> ℹ️ **Remarque :**  
> Si votre structure est :
> ```
> Projet_Annuel/
> ├─ docker-compose.yml
> └─ ...
> ```
> placez-vous dans `Projet_Annuel` pour lancer la commande.

## Accéder à l'application

Une fois les conteneurs démarrés :

- **Frontend (interface web)** :  
  [http://localhost:5500/Gestionnaire_mdp.html](http://localhost:5500/Gestionnaire_mdp.html)

- **Backend (API FastAPI)** :  
  [http://localhost:8000](http://localhost:8000)

- **pgAdmin (gestion base de données)** :  
  [http://localhost:5050](http://localhost:5050)  
  (identifiants dans le `docker-compose.yml`)

## Connexion à pgAdmin

- Lors de la première connexion à [http://localhost:5050](http://localhost:5050), utilisez :
  - **Email** : `admin@admin.com`
  - **Mot de passe** : `admin`

- Pour accéder à la base de données PostgreSQL depuis pgAdmin :
  - Cliquez sur le serveur déjà présent ou ajoutez-en un avec :
    - **Host** : `db`
    - **Port** : `5432`
    - **Username** : `postgres`
    - **Password** : `example`
  - Si un mot de passe est demandé lors de la connexion au serveur, saisissez simplement `example`.

## Tester l'application

1. Vérifiez que tous les conteneurs sont démarrés :
   ```sh
   docker ps
   ```
   Vous devez voir les conteneurs `postgres`, `backend`, `frontend`, et `pgadmin` en statut "Up".

2. Testez l'accès à chaque service :
   - Frontend : ouvrez [http://localhost:5500/Gestionnaire_mdp.html](http://localhost:5500/Gestionnaire_mdp.html)
   - Backend/API : ouvrez [http://localhost:8000](http://localhost:8000) (vous devez voir un message JSON)
   - pgAdmin : ouvrez [http://localhost:5050](http://localhost:5050) et connectez-vous avec les identifiants du `docker-compose.yml`

3. Dans l'interface web :
   - Créez un compte, connectez-vous, ajoutez un mot de passe, vérifiez que la liste s'affiche et que la suppression fonctionne.
   - Vous pouvez gérer plusieurs comptes pour un même site (identifiant + site + mot de passe).
   - Les mots de passe doivent être complexes (voir l'interface pour les critères).
   - Les boutons et champs sont alignés pour une meilleure lisibilité.
   - Vous pouvez supprimer tous les mots de passe d'un coup.

## Pour faire les commits

1. Créez une nouvelle branche :
   ```sh
   git checkout -b le-nom-de-notre-branche
   ```

2. Faites vos modifications.

3. Ajoutez et validez vos modifications :
   ```sh
   git add .
   git commit -m "Votre message de commit"
   ```

4. Poussez vos modifications sur le serveur distant :
   ```sh
   git push origin le-nom-de-notre-branche
   ```

5. Créez une Pull Request pour que les autres puissent voir vos modifications et les valider.

6. Une fois la Pull Request validée, vous pouvez supprimer la branche distante si besoin :
   ```sh
   git push origin --delete le-nom-de-notre-branche
   ```

- Pour éviter que git modifie les fins de ligne de `wait-for-it.sh` :
   ```sh
   git config --global core.autocrlf input
   ```

---

## Sécurité et configuration du mot de passe de la base de données

Pour garantir la sécurité et permettre à chacun d’utiliser l’application sans exposer de mot de passe dans le code ou le dépôt :

1. **Après avoir téléchargé le projet, créez le dossier `secrets` à la racine du projet (au même niveau que `docker-compose.yml`).**
2. **Dans ce dossier, créez un fichier `db_password.txt` contenant le mot de passe souhaité pour la base de données PostgreSQL.**
   - Exemple :
     ```
     exemplemotdepasse
     ```
3. **Ce dossier est déjà ignoré par git (`/secrets/` dans `.gitignore`), donc votre mot de passe ne sera jamais versionné.**
4. **Le backend lira automatiquement ce mot de passe pour se connecter à la base de données.**
5. **Lors de la connexion à PostgreSQL via pgAdmin, utilisez ce même mot de passe.**

> ⚠️ Si vous changez le mot de passe dans `db_password.txt`, supprimez les volumes Docker pour réinitialiser le mot de passe de la base de données, puis relancez les conteneurs.

---

> Pour toute question technique ou problème de démarrage, consultez la documentation du projet ou contactez les mainteneurs.