# Projet_Annuel

## Lancer le projet avec Docker

1. Ouvrez un terminal.
2. Placez-vous dans le dossier contenant `docker-compose.yml` :

   ```sh
   cd "c:\chemin_vers_le_dossier\Projet_Annuel\Projet_Annuel"
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
> └─ Projet_Annuel/
>     └─ ...
> ```
> placez-vous dans `Projet_Annuel` pour lancer la commande.  
> Si le fichier est dans `Projet_Annuel\Projet_Annuel`, placez-vous dans ce dossier.

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


## Pour faire les commits
1. Changer de branche ex. :
git checkout -b le-nom-de-notre-branche

2. Faites vos modifications

3. Faites un commit avec un message explicite ex. :
git add le-nom-de-l'element
git commit -m "Mise à jour du README.md"

4. Faites un push pour envoyer vos modifications sur le serveur distant :
git push -u origin le-nom-de-la-branche

- Créez une Pull Request pour que les autres puissent voir vos modifications et les valider
- Une fois que la Pull Request a été validée, vous pouvez supprimer la branche d


- Pour supprimer la branche, vous pouvez utiliser la commande suivante : `git branch

- Pour eviter que le git nous modifie wait-for-it.sh , nous allons utiliser la commande suivante : "git config --global core.autocrlf input" def