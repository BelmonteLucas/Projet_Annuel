# 🛡️ HoneyPot Pro Max – Laboratoire de Cybersécurité ESGI

> **Projet Annuel 2024-2025** | Un gestionnaire de mots de passe avec MFA testé dans un environnement hostile

[![Version](https://img.shields.io/badge/Version-2025.1-brightgreen)](https://github.com/BelmonteLucas/Projet_Annuel)
[![Docker](https://img.shields.io/badge/Docker-Compose%20Ready-blue)](https://docker.com)
[![Security](https://img.shields.io/badge/Security-MFA%20%2B%20IDS-red)](https://en.wikipedia.org/wiki/Multi-factor_authentication)
[![License](https://img.shields.io/badge/License-Educational-yellow)](LICENSE)

## 🎯 Vision du Projet

**Notre défi** : Créer une application sécurisée, puis l'attaquer pour valider sa robustesse !

Ce projet simule un **laboratoire de cybersécurité professionnel** où nous développons **HoneyPot Pro Max** (gestionnaire de mots de passe avec authentification à deux facteurs) et le testons face à des attaques réelles dans un environnement contrôlé avec monitoring complet.

### ✨ Ce qui rend ce projet unique
- 🏗️ **Architecture complète** : Application + Infrastructure de sécurité + Monitoring
- 🔐 **Sécurité réelle** : MFA/2FA, chiffrement AES-256, protection anti-replay
- 📊 **Monitoring professionnel** : Stack ELK + Snort IDS + Wazuh HIDS
- ⚔️ **Tests d'intrusion** : Scripts automatisés de pentesting
- 📋 **Documentation exhaustive** : Guide complet pour reproduire et comprendre

---

## 📚 Table des Matières

1. [🏗️ Architecture du Laboratoire](#architecture)
2. [🔐 HoneyPot Pro Max - Application Cible](#application)
3. [🛡️ Système de Détection](#detection)
4. [⚙️ Installation & Déploiement](#installation)
5. [📊 Monitoring & Analyse](#monitoring)
6. [🌐 Accès aux Services](#acces)
7. [⚔️ Tests de Sécurité](#tests)
8. [🔧 Scripts & Outils](#scripts)
9. [🆘 Dépannage](#depannage)
10. [👥 Équipe & Contributions](#equipe)

---

<a id="architecture"></a>

## 🏗️ Architecture du Laboratoire

### 💡 Concept : Zone Démilitarisée (DMZ) Sécurisée

Notre laboratoire simule un **environnement de production réaliste** avec une architecture en couches pour tester la sécurité en profondeur :

```
🌍 COUCHE D'EXPOSITION
┌─────────────────────────────────────────────────────────────────────┐
│  🌐 Frontend (NGINX)     🔐 HTTPS/SSL     📡 Points d'entrée       │
│  Ports: 9080 (HTTP) / 9443 (HTTPS)       Surface d'attaque visible  │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
🚀 COUCHE APPLICATIVE
┌─────────────────────────────────────────────────────────────────────┐
│  ⚡ Backend FastAPI      🔑 Authentication MFA    📊 API REST      │
│  Port: 8000              Gestion sessions        Validation données │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
🗄️ COUCHE DONNÉES
┌─────────────────────────────────────────────────────────────────────┐
│  💾 PostgreSQL          🔒 Chiffrement AES      🛠️ pgAdmin         │
│  Secrets MFA chiffrés   Isolation réseau        Interface admin     │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
🔍 COUCHE SURVEILLANCE
┌─────────────────────────────────────────────────────────────────────┐
│  📡 Snort IDS    🛡️ Wazuh HIDS    📊 ELK Stack    🚨 Alertes      │
│  Trafic réseau   Intégrité sys.   Visualisation   Temps réel        │
└─────────────────────────────────────────────────────────────────────┘
```

### 🎯 Pourquoi cette architecture ?

| 🏷️ Couche | 🎯 Objectif | 🔧 Technologies | ⚔️ Tests possibles |
|-----------|-------------|-----------------|-------------------|
| **Exposition** | Surface d'attaque réaliste | NGINX, SSL/TLS | Man-in-the-middle, SSL/TLS attacks |
| **Application** | Robustesse du code | FastAPI, MFA, Sessions | Injection SQL, XSS, Force brute |
| **Données** | Protection des secrets | PostgreSQL, Fernet AES-256 | Exfiltration, Privilege escalation |
| **Surveillance** | Détection & analyse | Snort, Wazuh, ELK | Forensique, Pattern analysis |

---

<a id="application"></a>

## 🔐 HoneyPot Pro Max - Application Cible

### 🎨 Interface Moderne & Sécurisée

**HoneyPot Pro Max** est notre gestionnaire de mots de passe avec interface glassmorphism moderne, mais sa beauté cache une sécurité de niveau professionnel :

- 🎨 **Design** : Interface glassmorphism avec police Inter
- 🔐 **Authentification** : MFA/2FA obligatoire (TOTP RFC 6238)
- 🗄️ **Gestion** : CRUD complet des mots de passe avec génération sécurisée
- 🛡️ **Sécurité** : Chiffrement bout-en-bout, anti-replay, sessions sécurisées

### 🔒 Système MFA/2FA Avancé

#### Architecture de sécurité MFA
```
📱 Authenticator App          🖥️ Backend FastAPI           🗄️ PostgreSQL
        │                            │                            │
        │ 1. QR Code scanné          │                            │
        │◄───────────────────────────│                            │
        │                            │                            │
        │ 2. Code TOTP (ex: 123456)  │ 3. Validation + Chiffrement│
        │───────────────────────────►│ Fernet (AES-256)           │
        │                            │───────────────────────────►│
        │ 4. Accès autorisé          │ 5. Secret jamais en clair  │
        │◄───────────────────────────│                            │
```

#### 🛡️ Mesures de sécurité implémentées

| 🔒 Protection | 💡 Implémentation | ✅ Test de résistance |
|---------------|-------------------|----------------------|
| **Replay attacks** | Codes TOTP à usage unique | ✅ Impossible de réutiliser un code |
| **Brute force** | Limitation de tentatives + délais | ✅ Protection contre automation |
| **Timing attacks** | Comparaisons à temps constant | ✅ Pas de fuite d'information |
| **Database compromise** | Secrets Fernet AES-256 | ✅ Inutile même avec accès DB |
| **Social engineering** | Aucun fallback SMS/email | ✅ MFA obligatoire, pas de bypass |

### 📊 Endpoints API Disponibles

| 🌐 Endpoint | 📋 Description | 🔐 Sécurité |
|-------------|---------------|-------------|
| `POST /register` | Création de compte | Validation email + password |
| `POST /login` | Connexion standard | Rate limiting |
| `POST /login/otp` | Connexion avec MFA | Code TOTP requis |
| `POST /mfa/setup` | Configuration MFA | Auth préalable |
| `POST /mfa/verify` | Activation MFA | Code TOTP validation |
| `GET /passwords` | Liste des mots de passe | Auth + MFA |
| `POST /passwords` | Ajout mot de passe | Validation + chiffrement |

> 📖 **Documentation complète** : [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger interactif)

---

<a id="detection"></a>

## 🛡️ Système de Détection

### 🚨 Stack de Monitoring Professionnel

Notre laboratoire utilise les mêmes outils que les entreprises pour détecter et analyser les cyberattaques :

#### 📡 Snort IDS - Sentinel du Réseau
```
🔍 Snort - Intrusion Detection System
├── 🎯 Mission : Surveiller TOUT le trafic réseau
├── 📍 Position : Entre Internet et notre application  
├── 🚨 Détecte : Scans ports, injections SQL, XSS, DDoS
└── ⚡ Réaction : Alertes temps réel vers ELK Stack
```

#### 🛡️ Wazuh HIDS - Gardien du Système
```
🔒 Wazuh - Host-based Intrusion Detection
├── 🎯 Mission : Surveiller l'intégrité interne
├── 📍 Position : À l'intérieur des conteneurs
├── 🚨 Détecte : Modifications fichiers, escalade privilèges
└── ⚡ Réaction : Logs forensiques + corrélation d'événements
```

#### 📊 ELK Stack - Cerveau Analytique
```
🧠 Elasticsearch + Logstash + Kibana
├── 🔍 Elasticsearch : Indexation ultra-rapide des logs
├── ⚙️ Logstash : Pipeline d'enrichissement des données
└── 📈 Kibana : Visualisation et dashboards temps réel
```

### 🎯 Types d'Attaques Détectées

| 🔴 Niveau Critique | 🟡 Niveau Attention | 🔵 Niveau Information |
|-------------------|-------------------|---------------------|
| Injection SQL réussie | Scan de ports répétés | Trafic HTTP normal |
| Escalade de privilèges | Tentatives brute force | Authentification réussie |
| Modification fichiers système | Anomalies de trafic | Requêtes API légitimes |
| Exfiltration de données | Géolocalisation suspecte | Logs de débogage |

---

<a id="installation"></a>

## ⚙️ Installation & Déploiement

### 🚀 Installation en Une Commande

Notre script d'installation automatique configure **tout l'environnement** en moins de 5 minutes :

```bash
# 1. Cloner le projet
git clone https://github.com/BelmonteLucas/Projet_Annuel.git
cd Projet_Annuel

# 2. Configuration automatique (génère secrets, certificats, validation)
python setup_dev_environment.py

# 3. Lancement complet
docker compose up -d --build
```

> 💡 **Astuce** : Utilisez `python setup_dev_environment.py --help` pour voir toutes les options

### 🎯 Pré-requis Système

| 🛠️ Outil | 📋 Version | ✅ Vérification |
|-----------|------------|-----------------|
| **Docker** | 20.x+ | `docker --version` |
| **Docker Compose** | 2.x+ | `docker compose version` |
| **Python** | 3.8+ | `python --version` |
| **Git** | 2.x+ | `git --version` |

### 🔐 Ce que fait le Script d'Installation

1. **🗂️ Création structure** : Répertoires `secrets/` avec permissions correctes
2. **🔑 Génération secrets** : 
   - Clé MFA Fernet AES-256 (256 bits d'entropie)
   - Mot de passe PostgreSQL sécurisé (32 caractères, 4 types de caractères)
3. **🔒 Certificats SSL** : Auto-signés pour développement (ou migration existants)
4. **🧪 Validation** : Tests de compatibilité Docker + vérification des services
5. **📝 Configuration** : Fichiers `.env`, `.gitattributes`, `.editorconfig`

### ⏱️ Temps d'Installation

- **🥇 Première fois** : 5-8 minutes (téléchargement images Docker)
- **🔄 Relancement** : 30 secondes (images en cache)
- **🛠️ Après modification** : 1-2 minutes (rebuild services modifiés)

### ✅ Validation Automatique

```bash
# Vérifier tous les services
docker compose ps

# Validation complète avec rapport détaillé
python scripts/validate_installation.py

# Test de l'installation depuis zéro (simulation)
python scripts/test_fresh_install.py
```

**Services attendus :**
- ✅ `frontend_service` (NGINX) - Ports 9080/9443
- ✅ `backend_service` (FastAPI) - Port 8000  
- ✅ `database_service` (PostgreSQL) - Port 5432
- ✅ `kibana_service` (Monitoring) - Port 5601
- ✅ `elasticsearch_service` - Port 9200
- ✅ `snort_service` + `wazuh_service` (IDS/HIDS)

---

<a id="monitoring"></a>

## 📊 Monitoring & Analyse

### 🎯 Centre de Commandement Kibana

**Accès principal** : [http://localhost:5601](http://localhost:5601)

#### 📋 Dashboards Recommandés à Créer

```
📊 Security Overview
├── Vue d'ensemble des menaces actives
├── Métriques temps réel (attaques/minute)
└── Top 10 des IPs suspectes

📈 Network Analysis  
├── Analyse du trafic Snort en temps réel
├── Détection des scans de ports
└── Patterns d'attaque réseau

🔐 Authentication Monitor
├── Tentatives de connexion (succès/échec)
├── Activité MFA (codes générés/validés)
└── Sessions actives et géolocalisation

🛡️ System Integrity
├── Surveillance Wazuh des fichiers
├── Modifications système suspectes
└── Processus et services anormaux
```

### 🔍 Commandes de Monitoring en Direct

```bash
# 📡 Surveillance réseau (Snort)
docker logs snort_service --tail 50 | grep -i "ALERT"

# 🛡️ Surveillance système (Wazuh)  
docker logs wazuh_service --tail 30 | grep -i "rule"

# 📊 État général des services
docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"

# 💾 Utilisation des ressources
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 🔍 Recherche dans Elasticsearch
curl -s "http://localhost:9200/_search?q=alert&size=10" | jq '.hits.hits[]._source'
```

### 📈 Métriques Clés à Surveiller

| 🎯 Métrique | 🔍 Où la voir | ⚠️ Seuil d'alerte |
|-------------|---------------|-------------------|
| **Tentatives de connexion** | Kibana > Auth Dashboard | > 10/minute |
| **Codes MFA invalides** | Logs backend FastAPI | > 5 consécutifs |
| **Scans de ports** | Snort alerts | Détection immédiate |
| **Erreurs 4xx/5xx** | NGINX logs | > 50/minute |
| **Modifications fichiers** | Wazuh integrity | Toute modification |
| **CPU/RAM services** | Docker stats | > 80% sustained |

---

<a id="acces"></a>

## 🌐 Accès aux Services

### 🎯 Applications Principales (Vos Cibles de Test)

| 🌐 Service | 🔗 URL d'Accès | 📋 Description | ⚔️ Tests Recommandés |
|------------|----------------|---------------|---------------------|
| **HoneyPot HTTP** | [http://localhost:9080](http://localhost:9080) | Interface non chiffrée | Man-in-the-middle, packet sniffing |
| **HoneyPot HTTPS** | [https://localhost:9443](https://localhost:9443) | Interface sécurisée SSL | SSL/TLS attacks, certificate bypass |
| **API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger interactif | API fuzzing, endpoint discovery |
| **API Backend Direct** | [http://localhost:8000](http://localhost:8000) | FastAPI sans proxy | Bypass testing, direct injection |

### 🔧 Interfaces de Monitoring (Vos Outils d'Analyse)

| 🛠️ Service | 🔗 URL d'Accès | 🔑 Identifiants | 💡 Utilité |
|------------|----------------|-----------------|-------------|
| **Kibana** | [http://localhost:5601](http://localhost:5601) | *(Accès direct)* | Visualiser attaques temps réel |
| **pgAdmin** | [http://localhost:5050](http://localhost:5050) | `admin@admin.com` / `admin` | Analyser impact sur base données |

### ⚙️ Services Internes (Monitoring)

| 🔒 Service | 🔌 Port | 🎯 Fonction | 📊 Accès |
|------------|---------|-------------|----------|
| **Elasticsearch** | 9200 | Stockage des logs | API REST interne |
| **PostgreSQL** | 5432 | Base de données | Via pgAdmin uniquement |
| **Logstash** | 5044 | Pipeline de logs | Service interne |
| **Snort IDS** | 1514/udp | Détection réseau | Logs vers ELK |
| **Wazuh HIDS** | 1515, 55000 | Détection système | Logs vers ELK |

### ⚡ Test Rapide de Connectivité

```bash
# Vérification que tous les services répondent
curl -I http://localhost:9080/          # ✅ Frontend HTTP
curl -I -k https://localhost:9443/      # ✅ Frontend HTTPS  
curl -I http://localhost:8000/docs      # ✅ API Documentation
curl -I http://localhost:5601/          # ✅ Kibana Dashboard
curl -I http://localhost:5050/          # ✅ pgAdmin Interface

# Si toutes ces commandes retournent du HTML (200 OK), tout est opérationnel !
```

---

<a id="tests"></a>

## ⚔️ Tests de Sécurité

### 🎯 Scénarios de Test par Niveau

#### 🟢 Niveau 1 : Tests Fonctionnels (Baseline)

**Objectif** : Établir le comportement normal pour détecter les anomalies

```bash
# Test A : Utilisation normale
# 1. Ouvrir http://localhost:9080
# 2. Créer un compte utilisateur
# 3. Configurer MFA avec Google Authenticator
# 4. Ajouter 5-10 mots de passe
# 5. Observer les logs "normaux" dans Kibana
```

#### 🟡 Niveau 2 : Tests Offensifs

**Test B : Attaque Force Brute**
```bash
# Test automatisé avec notre script
python scripts/security_tests.py --scenario brute_force

# Test manuel avec curl
for i in {1..20}; do
  curl -X POST http://localhost:9080/api/login \
    -d "username=admin&password=wrong$i" \
    -H "Content-Type: application/x-www-form-urlencoded"
  sleep 1
done
```

**Test C : Injection SQL**
```bash
# Test avec payloads courants
python scripts/security_tests.py --scenario sql_injection

# Test manuel
curl -X POST http://localhost:9080/api/login \
  -d "username=admin' OR '1'='1--&password=test" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

**Test D : Scan de Ports**
```bash
# Avec nmap (si installé)
nmap -sS -O localhost -p 1-10000

# Scan basique avec netcat
for port in 22 80 443 3306 5432 8000 9080; do
  echo "Testing port $port"
  nc -zv localhost $port 2>&1 | grep succeeded
done
```

#### 🔴 Niveau 3 : Tests Avancés

**Test E : Contournement MFA**
```bash
# 1. S'authentifier normalement (username + password)
# 2. Intercepter la session avant validation MFA  
# 3. Essayer d'accéder directement aux endpoints protégés
# 4. Tenter des codes MFA invalides ou expirés
# 5. Analyser les logs de sécurité générés
```

**Test F : Évasion de Conteneur**
```bash
# Accéder à un conteneur
docker exec -it backend_service /bin/bash

# Tentatives d'évasion (surveillées par Wazuh)
# 1. Lister fichiers hôte : ls /host/ 2>/dev/null
# 2. Scanner réseau : ping database_service
# 3. Escalade privilèges : sudo su - 2>/dev/null
```

### 📊 Analyse des Résultats

#### ✅ Critères de Succès par Test

| 🎯 Type d'Attaque | 🎯 Résultat Attendu | 📍 Où Vérifier |
|-------------------|---------------------|-----------------|
| **Force brute** | Alerte dans les 10 tentatives | Snort + Kibana Dashboard |
| **Injection SQL** | Requête bloquée + log d'alerte | Backend logs + Wazuh |
| **Scan de ports** | Détection immédiate du scan | Snort IDS alerts |  
| **Contournement MFA** | Accès refusé sans code valide | Application logs |
| **Évasion conteneur** | Tentatives loggées par Wazuh | Wazuh HIDS alerts |

---

<a id="scripts"></a>

## 🔧 Scripts & Outils

### 🛠️ Scripts Disponibles

Notre projet inclut des scripts professionnels pour automatiser les tests et la maintenance :

#### 🔒 `scripts/security_tests.py` - Tests de Sécurité Automatisés

```bash
# Tests complets de sécurité
python scripts/security_tests.py --scenario all

# Tests spécifiques
python scripts/security_tests.py --scenario brute_force    # Force brute
python scripts/security_tests.py --scenario sql_injection # Injection SQL  
python scripts/security_tests.py --scenario port_scan     # Scan de ports
python scripts/security_tests.py --scenario xss           # Cross-site scripting

# Rapport détaillé JSON généré automatiquement
cat security_test_report.json | jq '.summary'
```

**Fonctionnalités** :
- ✅ Tests automatisés avec payloads réalistes
- ✅ Intégration avec le monitoring Kibana
- ✅ Rapports JSON pour analyse
- ✅ Simulation d'attaques multithread

#### ✅ `scripts/validate_installation.py` - Validation Complète

```bash
# Validation de tous les services
python scripts/validate_installation.py

# Validation avec rapport détaillé
python scripts/validate_installation.py --detailed --output validation_report.json
```

**Vérifications** :
- ✅ Statut des 9 services Docker
- ✅ Connectivité réseau entre services
- ✅ Accès aux interfaces web (HTTP codes)
- ✅ Santé de la base de données PostgreSQL
- ✅ Fonctionnement ELK Stack
- ✅ Configuration SSL/TLS

#### 🆕 `scripts/test_fresh_install.py` - Test Installation Fraîche

```bash
# Simulation installation from scratch
python scripts/test_fresh_install.py

# Test avec environnement Docker propre  
python scripts/test_fresh_install.py --clean-docker
```

**Simule** :
- ✅ Installation sur machine vierge
- ✅ Respect exact des étapes du README
- ✅ Temps d'installation mesurés
- ✅ Validation finale automatique

#### 🔧 `scripts/fix_line_endings.py` - Correction Encodage

```bash
# Correction automatique des fins de ligne LF/CRLF
python scripts/fix_line_endings.py

# Avec rapport détaillé
python scripts/fix_line_endings.py --verbose
```

#### 🔌 `scripts/check_port_conflicts.py` - Détection Conflits Ports

```bash
# Vérification complète des conflits de ports
python scripts/check_port_conflicts.py

# Vérification avec rapport JSON détaillé
python scripts/check_port_conflicts.py --report port_analysis.json

# Vérification silencieuse (pour intégration CI/CD)
python scripts/check_port_conflicts.py --no-report
```

**Fonctionnalités** :
- ✅ Détection automatique des ports occupés (TCP/UDP)
- ✅ Identification des processus en conflit
- ✅ Solutions adaptées par niveau de criticité
- ✅ Support Windows (ports réservés système)
- ✅ Suggestions de ports alternatifs
- ✅ Patches Docker Compose automatiques

### 🚀 Script Principal : `setup_dev_environment.py`

**Architecture modulaire v2.0** - Responsabilités séparées pour une maintenance optimale :

```bash         
# Installation complète (recommandée)
python setup_dev_environment.py

# Installation rapide (sans confirmations)
python setup_dev_environment.py --quick

# Options avancées
python setup_dev_environment.py --skip-docker    # Skip vérifications Docker
python setup_dev_environment.py --skip-encoding  # Skip conversion UTF-8
python setup_dev_environment.py --skip-ports     # Skip vérification ports

# Aide complète
python setup_dev_environment.py --help
```

#### 🏗️ Architecture Modulaire

| 📦 Module | 🎯 Responsabilité | 📋 Fonctions |
|-----------|------------------|--------------|
| **`setup/system_checker.py`** | Vérifications système | Python, Docker, permissions |
| **`setup/secrets_manager.py`** | Génération sécurisée | MFA keys, DB password, SSL certs |
| **`setup/project_configurator.py`** | Configuration projet | UTF-8, Git attributes, EditorConfig |
| **`setup/colors.py`** | Utilitaires affichage | Couleurs ANSI, formatage |
| **`scripts/check_port_conflicts.py`** | Vérification ports | Conflits TCP/UDP, solutions |

**Actions automatiques** :
1. � **Vérification système** : Python 3.8+, Docker, compatibilité OS
2. 🔌 **Détection conflits ports** : TCP/UDP, processus, solutions adaptées
3. 🔐 **Génération secrets** : MFA Fernet AES-256, DB password, SSL auto-signés
4. 🎨 **Standardisation** : UTF-8, `.gitattributes`, `.editorconfig`
5. ✅ **Validation complète** : Tests de cohérence et santé système
6. 📊 **Rapport détaillé** : Résumé avec statut de chaque étape

---

<a id="depannage"></a>

## 🆘 Dépannage

### 🚨 Guide de Résolution des Problèmes

| ❌ Problème Courant | 💡 Solution Rapide | 🔧 Solution Avancée |
|---------------------|-------------------|---------------------|
| **Port déjà utilisé** | `docker compose down` | Modifier ports dans `docker-compose.yml` |
| **Services non healthy** | `docker compose logs [service]` | Redémarrer individuellement |
| **MFA impossible** | Vérifier proxy `/api/` | `curl http://localhost:9080/api/docs` |
| **Kibana inaccessible** | Attendre 2-3 min (démarrage) | `docker logs kibana_service` |
| **Erreurs UTF-8** | `python scripts/fix_line_endings.py` | Reconfigurer Git |

### 🔌 Gestion des Conflits de Ports

**Erreur type** : `bind: An attempt was made to access a socket in a way forbidden by its access permissions`

#### 🎯 Ports utilisés par le projet

| 🔌 Port | 🛠️ Service | 🔧 Modifiable |
|---------|------------|--------------|
| **9080** | Frontend HTTP | ✅ Oui - Variable `FRONTEND_HTTP_PORT` |
| **9443** | Frontend HTTPS | ✅ Oui - Variable `FRONTEND_HTTPS_PORT` |
| **8000** | Backend API | ✅ Oui - Variable `BACKEND_PORT` |
| **5432** | PostgreSQL | ✅ Oui - Variable `POSTGRES_PORT` |
| **5601** | Kibana | ✅ Oui - Variable `KIBANA_PORT` |
| **5050** | pgAdmin | ✅ Oui - Variable `PGADMIN_PORT` |
| **9200** | Elasticsearch | ✅ Oui - Variable `ELASTICSEARCH_PORT` |
| **5044** | Logstash | ✅ Oui - Variable `LOGSTASH_PORT` |
| **1514** | Snort (UDP) | ⚠️ Critique - IDS |
| **1515** | Wazuh agents | ⚠️ Critique - HIDS |
| **55000** | Wazuh API | ⚠️ Critique - HIDS |

#### 🛠️ Solutions par type de conflit

**🟢 Conflit Simple (ports web)** :
```bash
# Vérifier quel processus utilise le port
netstat -ano | findstr :9080
# Ou sur Linux/Mac
lsof -i :9080

# Solution : Modifier le port dans docker-compose.yml
# Exemple : changer 9080 en 9081
```

**🟡 Conflit Critique (Wazuh port 55000)** :
```bash
# 1. Identifier le processus
netstat -ano | findstr :55000

# 2. Options de résolution :
# Option A : Arrêter le service conflictuel (si possible)
# Option B : Modifier le port Wazuh (attention : impact sur configuration)

# 3. Modification dans docker-compose.yml
# Remplacer "55000:55000" par "55001:55000"
# Puis mettre à jour la configuration Wazuh
```

**🔴 Conflit Windows (permissions système)** :
```powershell
# Vérifier les ports réservés par Windows
netsh int ipv4 show excludedportrange protocol=tcp

# Solution : Utiliser des ports hors de la plage réservée
# Généralement au-dessus de 50000 ou en dessous de 1024
```

**🐳 Cas Particulier : Docker déjà lancé** :
```bash
# Si vos services sont déjà actifs (comme montré ci-dessus)
docker compose ps  # Vérifier l'état

# Si les services tournent normalement, les "conflits" sont attendus
# Seuls les conflits avec d'AUTRES processus nécessitent une action
```

> 💡 **Note importante** : Si `docker compose ps` montre vos services en cours d'exécution, les conflits détectés avec `com.docker.backend.exe` sont **normaux et attendus**.

#### 🔥 Exemple Concret : Erreur Port 55000

**Erreur rencontrée** :
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:55000 -> 127.0.0.1:0: listen tcp 0.0.0.0:55000: bind: An attempt was made to access a socket in a way forbidden by its access permissions.
```

**Diagnostic automatique** :
```bash
# 1. Lancer la détection automatique
python scripts/check_port_conflicts.py

# 2. Identifier le processus responsable
# Le script vous montrera : "Port 55000 utilisé par: Processus XYZ (PID: 1234)"

# 3. Solutions proposées automatiquement
# - Arrêter le processus conflictuel
# - Modifier le mapping de port : "55001:55000"
# - Configuration alternative dans Wazuh
```

**Solution rapide** :
```bash
# Modifier docker-compose.yml pour Wazuh
# Ligne 150 : Remplacer "55000:55000" par "55001:55000"

# Puis relancer
docker compose up -d --build
```

> ✅ **Résultat** : Wazuh sera accessible sur http://localhost:55001 au lieu de 55000

| ❌ Problème | ✅ Solution | 📝 Explication |
|-------------|-------------|----------------|
| **Snort EOF error** | Autoriser Docker File Sharing | Normal sur Windows Docker Desktop |
| **Network host non supporté** | ✅ **Automatiquement corrigé** | Utilise maintenant bridge networking |
| **Popup File Sharing** | **Cliquer "Allow"** | Obligatoire pour volumes Docker |

### 🔍 Diagnostics Avancés

```bash
# État complet du système
docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Tests de connectivité
curl -I http://localhost:9080/          # Frontend HTTP
curl -I -k https://localhost:9443/      # Frontend HTTPS
curl -I http://localhost:5601/          # Kibana
curl -I http://localhost:5050/          # pgAdmin

# Vérification base de données
docker exec database_service pg_isready -U postgres
```

### 🆘 Réinitialisation Complète

```bash
# Nettoyage complet (en cas de problème majeur)
docker compose down -v --remove-orphans
docker system prune -a
rm -rf secrets/

# Réinstallation from scratch
python setup_dev_environment.py
docker compose up -d --build
```

---

<a id="equipe"></a>

## 👥 Équipe & Contributions

### 🎓 Projet Annuel ESGI 2024-2025

**Formation** : Expert en Sécurité Informatique | **Niveau** : M2

#### 👨‍💻 Équipe de Développement

| 👤 Membre | 🎯 Rôle | 💡 Spécialités | 🚀 Contributions |
|-----------|---------|----------------|------------------|
| **🎯 Jakub WERLINSKI** | Chef de projet | Architecture système, Management | Conception globale, coordination |
| **🔐 Lucas BELMONTE** | Développeur sécurité | FastAPI, Cryptographie, Frontend | HoneyPot Pro Max, MFA/2FA complet |
| **🏗️ Evan RATSIMANOHATRA** | Architecte DevOps | Docker, Infrastructure, ELK | Monitoring, orchestration services |

#### 🎯 Objectifs Pédagogiques Atteints

Notre formation nous a permis de maîtriser :

- **🔒 Développement sécurisé** : Application avec MFA, chiffrement AES-256, validation
- **🔍 Détection d'intrusion** : IDS/HIDS professionnels, monitoring temps réel
- **📊 Analyse forensique** : ELK Stack, investigation d'incidents, corrélation
- **🏗️ DevSecOps** : Intégration sécurité dans CI/CD, infrastructure as code
- **⚔️ Red/Blue Team** : Pentesting automatisé et défense active

#### 🌟 Innovations & Apprentissages

**Ce qui rend notre projet unique :**

- ✅ **Approche "Learn by Breaking"** : Comprendre la sécurité en attaquant sa propre création
- ✅ **Stack professionnelle** : Même outils qu'en entreprise (Fortune 500)
- ✅ **Documentation exhaustive** : README testé et validé à 100%
- ✅ **Tests automatisés** : Scripts de pentesting et validation
- ✅ **Architecture réaliste** : DMZ, séparation des couches, monitoring complet

#### 🚀 Perspectives d'Évolution

Ce laboratoire ouvre la voie à :

- **🤖 Machine Learning** : Détection d'anomalies comportementales par IA
- **🌐 Threat Intelligence** : Intégration feeds de menaces externes
- **⚡ SOAR (Security Orchestration)** : Réponse automatique aux incidents
- **☁️ Cloud Security** : Déploiement AWS/Azure avec sécurité native
- **📱 Mobile Security** : Extension aux applications mobiles

---

## 🎬 Guide de Démonstration

### 🎯 Scénario de Présentation (15 minutes)

#### **Phase 1 : Architecture & Installation (3-4 minutes)**

```bash
# 1. Montrer la structure du projet
tree -L 2

# 2. Validation automatique  
python scripts/validate_installation.py

# 3. État des services
docker compose ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"
```

**Points à mentionner :**
- Architecture microservices en couches
- 9 services interconnectés 
- Installation automatisée en 5 minutes

#### **Phase 2 : Application & Sécurité (5-6 minutes)**

```bash
# 1. Interface utilisateur (navigateur)
# - Ouvrir http://localhost:9080
# - Créer compte utilisateur
# - Configurer MFA avec QR Code
# - Ajouter mots de passe avec générateur

# 2. Tests de sécurité en live
python scripts/security_tests.py --scenario brute_force

# 3. Monitoring temps réel
# - Ouvrir http://localhost:5601 (Kibana)
# - Montrer les alertes générées
```

**Points à mentionner :**
- Interface moderne avec sécurité de niveau professionnel
- MFA obligatoire (RFC 6238)
- Détection automatique des attaques

#### **Phase 3 : Monitoring & Analyse (4-5 minutes)**

```bash
# 1. Logs temps réel
docker logs snort_service --tail 20 | grep -i "ALERT"
docker logs wazuh_service --tail 10 | grep -i "rule"

# 2. API Documentation
# - Ouvrir http://localhost:8000/docs
# - Montrer Swagger interactif

# 3. Base de données
# - Ouvrir http://localhost:5050 (pgAdmin)
# - Montrer données chiffrées
```

**Points à mentionner :**
- Stack ELK pour analyse forensique
- APIs documentées (Swagger)
- Secrets jamais en clair (AES-256)

#### **Phase 4 : Questions & Synthèse (2-3 minutes)**

**Messages clés :**
- ✅ **Sécurité par conception** : MFA + chiffrement + monitoring
- ✅ **Tests automatisés** : Résistance prouvée aux attaques courantes  
- ✅ **Approche professionnelle** : Outils industriels + documentation complète
- ✅ **Apprentissage concret** : Red Team + Blue Team en pratique

### 💡 Points d'Impact Maximum

1. **🔥 Démonstration live** : Tests de sécurité avec logs temps réel
2. **📊 Interface Kibana** : Visualisation des attaques détectées
3. **🔐 Processus MFA** : De la configuration au chiffrement
4. **🛠️ Scripts automatisés** : Professionnalisme et reproductibilité

### 🎯 FAQ Préparées

**Q: Pourquoi HoneyPot Pro Max et pas une app existante ?**
R: Pour contrôler chaque aspect sécuritaire et créer des vulnérabilités testables

**Q: L'architecture est-elle réaliste ?**  
R: Oui, cette stack (ELK + IDS/HIDS) est standard en entreprise

**Q: Les tests sont-ils complets ?**
R: Nous couvrons OWASP Top 10 + tests spécifiques MFA + forensique

**Q: Déploiement en production possible ?**
R: Architecture prête, il faut adapter les secrets et certificats officiels

---

## 📖 Documentation Technique

### 🔗 Technologies & Standards

| 🏷️ Catégorie | 🛠️ Technologies | 📋 Standards |
|---------------|------------------|--------------|
| **Frontend** | HTML5, CSS3, JavaScript ES6 | Glassmorphism, Responsive |
| **Backend** | FastAPI, SQLAlchemy, Uvicorn | REST API, OpenAPI 3.0 |
| **Sécurité** | pyOTP, Cryptography, Passlib | RFC 6238 (TOTP), AES-256 |
| **Base données** | PostgreSQL 13, pgAdmin | ACID, Transactions |
| **Monitoring** | Snort 2.x, Wazuh 4.7, ELK 7.17 | SIEM, IDS/HIDS |
| **Infrastructure** | Docker, NGINX, SSL/TLS | Microservices, Proxy |

### 📊 Métriques du Projet

- **📁 Structure** : 85+ fichiers organisés en modules
- **🔐 Sécurité** : 15+ mesures implémentées (MFA, chiffrement, validation)
- **🧪 Tests** : 4 scripts automatisés + validation complète
- **📋 Documentation** : README 900+ lignes, 100% testé
- **⚙️ Services** : 9 conteneurs orchestrés avec Docker Compose
- **🌐 APIs** : 8 endpoints documentés avec Swagger

### 🎯 Conformité & Standards

- ✅ **OWASP Top 10** : Protection contre les vulnérabilités critiques
- ✅ **RFC 6238** : TOTP correctement implémenté
- ✅ **NIST** : Bonnes pratiques cryptographiques (AES-256)
- ✅ **ISO 27001** : Logging et monitoring de sécurité
- ✅ **GDPR** : Protection des données personnelles

---

## 🚀 Conclusion

**HoneyPot Pro Max** démontre qu'il est possible de créer une application à la fois **moderne**, **fonctionnelle** et **sécurisée** tout en gardant une approche pédagogique.

### 🎯 Objectifs Atteints

- ✅ **Application complète** : Gestionnaire de mots de passe avec MFA professionnel
- ✅ **Sécurité robuste** : Résistance prouvée aux attaques courantes  
- ✅ **Monitoring complet** : Détection et analyse temps réel des intrusions
- ✅ **Automatisation** : Déploiement et tests en une commande
- ✅ **Documentation** : Guide exhaustif et testé à 100%

### 💡 Apprentissages Clés

1. **La sécurité se conçoit, ne se rajoute pas** : Architecture sécurisée dès le départ
2. **Monitoring = Visibilité** : Impossible de défendre ce qu'on ne voit pas
3. **Tests automatisés indispensables** : Validation continue de la sécurité
4. **Documentation vivante** : README comme single source of truth

### 🌟 Impact Pédagogique

Ce projet nous a permis de **vivre concrètement** le cycle complet de la cybersécurité :
- 🔨 **Conception** sécurisée d'une application
- 🛡️ **Implémentation** des mesures de protection  
- ⚔️ **Tests** offensifs et validation de la robustesse
- 📊 **Analyse** forensique et amélioration continue

> 💬 *"La meilleure défense, c'est de comprendre l'attaque"* - Cette philosophie guide chaque aspect de notre laboratoire de cybersécurité.

---

### 📧 Contacts & Ressources

- **🔗 Repository GitHub** : [Projet_Annuel](https://github.com/BelmonteLucas/Projet_Annuel)
- **📚 Documentation** : Ce README (maintenu à jour)
- **🐛 Issues** : GitHub Issues pour bug reports et suggestions
- **💬 Discussions** : GitHub Discussions pour questions techniques

**🎓 ESGI - Expert en Sécurité Informatique | Promotion 2024-2025**

---

*Projet réalisé dans le cadre de la formation Expert en Sécurité Informatique à l'ESGI Paris. Tous les codes sources et configurations sont disponibles sous licence éducative.*