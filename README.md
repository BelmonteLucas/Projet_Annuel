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

> Pour toute question technique ou problème de démarrage, consultez la documentation du projet ou contactez les mainteneurs.