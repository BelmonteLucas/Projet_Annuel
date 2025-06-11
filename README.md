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

Le mot de passe de la base de données est **centralisé et sécurisé** dans le fichier :  
`secrets/db_password.txt`

- **Écrivez le mot de passe souhaité sur la première ligne du fichier** (pas de commentaire sur la première ligne).
- Ce mot de passe sera utilisé automatiquement par :
  - **PostgreSQL** (service `db`)
  - **Le backend** (service `backend`)
  - **pgAdmin** (service `pgadmin`, accès sans saisie manuelle du mot de passe)

**Exemple :**
```
monSuperMotDePasse2024!
# Ceci est un commentaire (optionnel, ignoré)
```

Pour changer le mot de passe :
1. Modifiez la première ligne de `secrets/db_password.txt`.
2. Supprimez les volumes pour réinitialiser la base :
   ```sh
   docker-compose down -v
   ```
3. Relancez l’application :
   ```sh
   docker-compose up -d
   ```

> **Astuce :**  
> pgAdmin est déjà préconfiguré pour se connecter à la base sans avoir à saisir le mot de passe, grâce à la génération dynamique du fichier `.pgpass`.

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
