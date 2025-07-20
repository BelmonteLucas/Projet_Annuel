# 🛡️ HoneyPot Security Suite – Projet Annuel ESGI

Bienvenue ! Ce projet propose une **infrastructure de sécurité complète** incluant un gestionnaire de mots de passe sécurisé avec authentification à deux facteurs (MFA), couplé à un **système de monitoring et détection d'intrusion** professionnel.

---

## 🚀 Vue d'ensemble du projet

### 🎯 **Objectifs pédagogiques**
Ce projet ESGI démontre la mise en œuvre d'une architecture de sécurité moderne comprenant :
- **Développement sécurisé** : Application web avec MFA et chiffrement
- **Détection d'intrusion** : Monitoring réseau et système en temps réel  
- **Analyse forensique** : Centralisation et visualisation des logs
- **Infrastructure as Code** : Déploiement automatisé avec Docker

### 🏗️ **Architecture technique**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FRONTEND      │    │    BACKEND      │    │   DATABASE      │
│   (NGINX/SSL)   │◄──►│   (FastAPI)     │◄──►│  (PostgreSQL)   │
│   Port 80/443   │    │   Port 8000     │    │   Port 5432     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
    ┌─────────────────────────────┼─────────────────────────────┐
    │              STACK DE SÉCURITÉ                            │
    ├─────────────────┬─────────────────┬─────────────────────┤
    │   SNORT IDS     │   WAZUH HIDS    │    ELK STACK        │
    │ (Réseau/Port)   │ (Fichiers/Sys)  │ (Logs/Analytics)    │
    │   Port 1514     │   Port 1515     │ Elasticsearch:9200  │
    │                 │   Port 55000    │ Logstash:5044       │
    │                 │                 │ Kibana:5601         │
    └─────────────────┴─────────────────┴─────────────────────┘
```

### 🛡️ **Composants de sécurité**

#### **Application principale**
- **Frontend** : Interface web sécurisée (HTTPS, certificats SSL)
- **Backend** : API FastAPI avec authentification MFA/2FA
- **Base de données** : PostgreSQL avec chiffrement des secrets
- **Administration** : pgAdmin pour la gestion base de données

#### **Système de détection d'intrusion (IDS/HIDS)**
- **Snort IDS** : Détection d'intrusion réseau en temps réel
- **Wazuh HIDS** : Surveillance d'intégrité des fichiers système
- **Règles personnalisées** : Détection d'attaques SSH, web, scan de ports

#### **Stack d'analyse et monitoring**
- **Elasticsearch** : Moteur de recherche et indexation des logs
- **Logstash** : Pipeline de traitement et enrichissement des logs
- **Kibana** : Interface de visualisation et dashboard de sécurité

### ✨ **Fonctionnalités**

#### **Gestionnaire de mots de passe**
- Créer un compte personnel sécurisé
- Activer l'authentification à deux facteurs (MFA/2FA) avec TOTP
- Ajouter, lister et supprimer vos mots de passe pour différents sites
- Interface web moderne et intuitive

#### **Monitoring de sécurité**
- Détection en temps réel des tentatives d'intrusion
- Surveillance de l'intégrité des fichiers critiques
- Alertes automatiques sur activités suspectes
- Tableaux de bord de sécurité avec métriques
- Analyse forensique des incidents

---

## 🛠️ Installation et configuration

### 1. Prérequis

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python 3](https://www.python.org/) (pour le script de configuration)
- [Git](https://git-scm.com/) pour cloner le dépôt

### 2. Cloner le projet

```bash
git clone https://github.com/BelmonteLucas/Projet_Annuel.git
cd Projet_Annuel
```

### 3. Configuration de l'environnement

#### a. Installer les dépendances de développement

```bash
pip install -r requirements-dev.txt
```

#### b. Lancer le script de configuration

```bash
python setup_dev_environment.py
```

Ce script va :
- Créer le répertoire `secrets/` si nécessaire
- Générer une clé de chiffrement MFA unique (`secrets/mfa_encryption_key.txt`)
- Configurer l'environnement de développement local

#### c. Configurer le mot de passe de la base de données

Créez le fichier `secrets/db_password.txt` avec votre mot de passe :

```bash
echo "votre_mot_de_passe_securise" > secrets/db_password.txt
```

### 4. Déploiement avec Docker

```bash
# Construction et lancement de toute l'infrastructure
docker compose up -d --build

# Vérifier que tous les services sont opérationnels
docker compose ps
```

L'option `--build` est recommandée la première fois ou après des modifications.

---

## 🌐 Accès aux services

### **🖥️ Applications principales**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | [https://localhost/](https://localhost/) | Interface utilisateur principale (HTTPS) |
| **API Backend** | [http://localhost:8000](http://localhost:8000) | API FastAPI avec documentation |
| **Swagger Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentation interactive de l'API |

### **🔧 Administration**

| Service | URL | Identifiants | Description |
|---------|-----|--------------|-------------|
| **pgAdmin** | [http://localhost:5050](http://localhost:5050) | `admin@admin.com` / `admin` | Interface d'administration PostgreSQL |
| **Kibana** | [http://localhost:5601](http://localhost:5601) | Accès direct | Tableaux de bord de sécurité |

### **🛡️ Monitoring de sécurité**

| Service | Port | Description |
|---------|------|-------------|
| **Snort IDS** | `1514/udp` | Collecte des logs syslog |
| **Wazuh API** | `55000` | API de gestion Wazuh |
| **Elasticsearch** | `9200` | Moteur de recherche des logs |

---

## 📊 Surveillance et monitoring

### **🔍 Commandes utiles pour vérifier l'état**

```bash
# Afficher le statut de tous les services avec format tableau
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Alternative : format personnalisé avec services
docker compose ps --format "table {{.Service}}\t{{.Name}}\t{{.Status}}"

# Affichage compact avec statut uniquement
docker ps --format "table {{.Names}}\t{{.Status}}" --filter "label=com.docker.compose.project=projet_annuel"

# Affichage détaillé avec ports et santé
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Size}}"

# Vérifier les logs de Snort IDS
docker logs snort_ids --tail 20

# Consulter les alertes de sécurité en temps réel
docker exec snort_ids tail -f /var/log/snort/alert

# Vérifier l'état de Wazuh
docker logs wazuh_manager --tail 10

# État de santé d'Elasticsearch
curl -s http://localhost:9200/_cluster/health | jq

# Surveillance en temps réel des logs
docker compose logs -f --tail=10
```

#### **📊 Commandes de monitoring avancé**

```bash
# Statistiques d'utilisation des ressources
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# Vérifier les healthchecks
docker inspect --format='{{.State.Health.Status}}' elasticsearch
docker inspect --format='{{.State.Health.Status}}' postgres_db_service

# Logs filtrés par niveau d'erreur
docker compose logs | grep -i error

# État des volumes Docker
docker volume ls | grep projet_annuel
docker system df
```

### **📈 Métriques de sécurité**

- **Snort IDS** : Capture et analyse le trafic réseau en temps réel
- **Wazuh HIDS** : Surveille l'intégrité des fichiers backend
- **ELK Stack** : Centralise tous les logs pour analyse et visualisation
- **Healthchecks** : Garantissent la disponibilité des services critiques

---

## 🔒 Sécurité et bonnes pratiques

### **🔐 Gestion des secrets**

- **Mots de passe** : Stockés dans `secrets/db_password.txt` (gitignore)
- **Clés MFA** : Chiffrées avec `secrets/mfa_encryption_key.txt`
- **Certificats SSL** : `nginx.crt` et `nginx.key` pour HTTPS
- **Isolation réseau** : Réseau Docker interne isolé

### **🛡️ Fonctionnalités MFA**

1. **Activation du MFA** : Interface utilisateur avec QR code
2. **Authentification TOTP** : Compatible Google Authenticator, Authy
3. **Stockage sécurisé** : Secrets MFA chiffrés en base
4. **Vérification obligatoire** : Code OTP requis pour la connexion

### **⚠️ Alertes de sécurité configurées**

- Tentatives de brute force SSH
- Scans de ports suspects  
- Accès non autorisés aux fichiers sensibles
- Trafic réseau anormal
- Connexions à la base de données

---

## 🧪 Tests et validation

### **✅ Vérifier l'installation**

```bash
# Tous les conteneurs doivent être "Up"
docker ps

# Tester l'accès à l'interface web
curl -k https://localhost/

# Vérifier l'API
curl http://localhost:8000/

# Tester Elasticsearch
curl http://localhost:9200/_cluster/health
```

### **🎯 Scénarios de test**

1. **Créer un compte utilisateur** sur l'interface web
2. **Activer le MFA** et scanner le QR code
3. **Se déconnecter et reconnecter** avec le code OTP
4. **Ajouter/supprimer des mots de passe**
5. **Générer du trafic** pour tester Snort
6. **Consulter les tableaux de bord** Kibana

---

## 🧑‍💻 Développement

### **🔧 Structure du projet**

```
Projet_Annuel/
├── docker-compose.yml          # Orchestration complète
├── nginx.conf                  # Configuration NGINX/SSL
├── setup_dev_environment.py    # Script d'initialisation
├── backend/                    # API FastAPI
│   ├── main.py                # Point d'entrée de l'API
│   ├── models.py              # Modèles de données
│   └── requirements.txt       # Dépendances Python
├── frontend/                   # Interface web
│   ├── index.html             # Page principale
│   ├── app.js                 # Logique JavaScript
│   └── style.css              # Styles CSS
├── snort/                      # Configuration Snort IDS
│   ├── Dockerfile             # Image Snort personnalisée
│   ├── snort.conf             # Configuration Snort
│   ├── entrypoint.sh          # Script de démarrage
│   └── rules/                 # Règles de détection
├── elk/                        # Configuration ELK Stack
│   ├── elasticsearch/         # Config Elasticsearch
│   ├── logstash/              # Pipelines Logstash
│   └── kibana/                # Dashboards Kibana
└── secrets/                    # Fichiers sensibles (gitignore)
    ├── db_password.txt        # Mot de passe PostgreSQL
    └── mfa_encryption_key.txt # Clé de chiffrement MFA
```

### **🔄 Workflow de développement**

```bash
# Développement local
python setup_dev_environment.py

# Relancer après modifications
docker compose down
docker compose up -d --build

# Logs en temps réel
docker compose logs -f [service_name]

# Accès aux conteneurs
docker exec -it [container_name] /bin/bash
```

---

## 📚 Documentation technique

### **🔗 Technologies utilisées**

- **Frontend** : HTML5, CSS3, JavaScript ES6
- **Backend** : FastAPI, SQLAlchemy, Uvicorn
- **Base de données** : PostgreSQL 13
- **Sécurité** : pyOTP, cryptography, passlib
- **Infrastructure** : Docker, Docker Compose, NGINX
- **Monitoring** : Snort 2.x, Wazuh 4.7.5, ELK Stack 7.17.9

### **🌐 APIs et endpoints**

Consultez la documentation Swagger à l'adresse : [http://localhost:8000/docs](http://localhost:8000/docs)

### **🔧 Configuration avancée**

Pour une configuration en production, consultez :
- Les fichiers de configuration dans `elk/`
- Les règles Snort dans `snort/rules/`
- La configuration Wazuh pour la surveillance des fichiers

---

## 🆘 Support et dépannage

### **❌ Problèmes courants**

| Problème | Solution |
|----------|----------|
| Port déjà utilisé | `docker compose down` puis changer les ports |
| Permissions refusées | Vérifier les fichiers dans `secrets/` |
| Services non healthy | `docker compose logs [service]` |
| Erreur SSL/TLS | Régénérer les certificats NGINX |

### **🔍 Debugging**

```bash
# Logs détaillés d'un service
docker compose logs --details [service_name]

# État des conteneurs
docker stats

# Inspection des réseaux
docker network ls
docker network inspect [network_name]

# Volumes Docker
docker volume ls
docker volume inspect [volume_name]
```

### **🆘 Support**

- **Issues GitHub** : [https://github.com/BelmonteLucas/Projet_Annuel/issues](https://github.com/BelmonteLucas/Projet_Annuel/issues)
- **Documentation** : Ce README et les commentaires dans le code
- **Logs** : Consultez toujours les logs Docker en cas de problème

---

## 📄 Licence et contributions

Ce projet est développé dans le cadre d'un **projet annuel ESGI** à des fins pédagogiques.

- **Auteur** : Lucas Belmonte
- **Formation** : ESGI - Expert en Sécurité Informatique
- **Année** : 2024-2025

Les contributions sont les bienvenues via des Pull Requests sur GitHub.

---

*🛡️ Sécurité avant tout - Ce projet démontre l'implémentation d'une infrastructure de sécurité complète avec détection d'intrusion et monitoring en temps réel.*
