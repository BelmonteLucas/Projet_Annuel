# 🛡️ HoneyPot Pro Max – Laboratoire de Cybersécurité ESGI

**Un gestionnaire de mots de passe sécurisé testé en conditions réelles d'attaque**

Ce projet ESGI démontre la création d'**HoneyPot Pro Max** (gestionnaire de mots de passe avec MFA) et son **test dans un environnement hostile** avec monitoring temps réel des tentatives d'intrusion.

---

## 🚀 Installation Rapide (5 minutes)

```bash
# 1. Cloner le projet
git clone https://github.com/BelmonteLucas/Projet_Annuel.git
cd Projet_Annuel

# 2. Configuration automatique
python setup_dev_environment.py

# 3. Lancement complet
docker compose up -d --build

# 4. Vérification
python scripts/validate_installation.py
```

**🌐 Accès aux services :**
- **HoneyPot Pro Max** : [http://localhost:9080](http://localhost:9080) (HTTP) / [https://localhost:9443](https://localhost:9443) (HTTPS)
- **Kibana (Monitoring)** : [http://localhost:5601](http://localhost:5601)
- **pgAdmin (Base de données)** : [http://localhost:5050](http://localhost:5050) (`admin@admin.com` / `admin`)
- **API Documentation** : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🎯 Vision du Projet

### **Le Défi**
Créer une application sécurisée ET la tester face à de vraies menaces pour valider sa robustesse.

### **Notre Approche**
1. **🔐 HoneyPot Pro Max** : Gestionnaire de mots de passe avec MFA
2. **🛡️ Infrastructure de détection** : Snort IDS, Wazuh HIDS, ELK Stack
3. **⚔️ Tests d'intrusion** : Scénarios d'attaque en conditions réelles

### **Technologies Clés**
- **Frontend** : HTML5/CSS3/JS (design glassmorphism)
- **Backend** : FastAPI + PostgreSQL
- **Sécurité** : MFA/TOTP, chiffrement Fernet, HTTPS
- **Monitoring** : Snort, Wazuh, Elasticsearch, Logstash, Kibana
- **Infrastructure** : Docker Compose, NGINX

---

## 🏗️ Architecture

```
🌍 INTERNET
     ↓
┌─────────────────────────────────────────┐
│            🔒 DMZ ZONE                  │
│                                         │
│ 🌐 Frontend ←→ 🛡️ NGINX ←→ 🚀 Backend   │
│   (9080/9443)    (Proxy)    (FastAPI)  │
│                                         │
│         🗄️ PostgreSQL + pgAdmin         │
└─────────────────────────────────────────┘
     ↓
┌─────────────────────────────────────────┐
│        🔍 MONITORING & SECURITY         │
│                                         │
│ 📡 Snort  →  🛡️ Wazuh  →  📊 ELK        │
│  (IDS)       (HIDS)      (Analytics)   │
└─────────────────────────────────────────┘
```

**✅ Fonctionnalités de sécurité :**
- Authentification MFA obligatoire (TOTP)
- Chiffrement bout en bout (Fernet + HTTPS)
- Détection d'intrusion temps réel
- Monitoring avancé avec alertes
- Tests automatisés de vulnérabilités

---

## 🧪 Tests de Sécurité

### **Scénarios de Test Disponibles**

#### **🎯 Tests de Base**
```bash
# Utilisation normale (baseline)
# → Créer compte, activer MFA, gérer mots de passe

# Test HTTPS vs HTTP
# → Comparer la sécurité des communications
```

#### **⚔️ Tests Offensifs**
```bash
# Force brute automatisée
python scripts/security_tests.py --scenario brute_force

# Injection SQL
python scripts/security_tests.py --scenario sql_injection

# Scan de ports
nmap -sS localhost -p 1-10000
```

#### **🔍 Analyse des Résultats**
- **Kibana** : Visualisation temps réel des attaques
- **Logs Snort** : Détection réseau
- **Logs Wazuh** : Surveillance système
- **Métriques** : Temps de détection, faux positifs/négatifs

---

## 📊 Monitoring

### **Dashboard Principal (Kibana)**
🔗 [http://localhost:5601](http://localhost:5601)

**Dashboards recommandés :**
- Security Overview
- Network Traffic Analysis
- Authentication Attempts
- System Integrity Monitoring

### **Commandes de Surveillance**
```bash
# État des services
docker ps --format "table {{.Names}}\t{{.Status}}"

# Logs en temps réel
docker compose logs -f snort_service wazuh_service

# Métriques système
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

---

## 🔧 Développement

### **Structure du Projet**
```
Projet_Annuel/
├── frontend/                   # Interface HoneyPot Pro Max
├── backend/                    # API FastAPI
├── scripts/                    # Outils de validation/test
├── secrets/                    # Fichiers sensibles (gitignore)
├── elk/                        # Configuration ELK Stack
├── snort/                      # Configuration Snort IDS
├── wazuh/                      # Configuration Wazuh HIDS
└── docker-compose.yml          # Orchestration complète
```

### **Workflow de Développement**
```bash
# Modification et test
docker compose down
docker compose up -d --build

# Validation complète
python scripts/validate_installation.py

# Tests de sécurité
python scripts/security_tests.py --scenario all
```

---

## 🆘 Dépannage

### **Problèmes Courants**

| ❌ Problème | 💡 Solution |
|-------------|-------------|
| **Port occupé** | `docker compose down` |
| **Service unhealthy** | `docker compose logs [service]` |
| **MFA ne fonctionne pas** | Vérifier `/api/` proxy |
| **Kibana inaccessible** | Attendre 2-3 min démarrage |

### **Windows Spécifique**
- ✅ **Popup Docker File Sharing** → Cliquer "Allow"
- ✅ **Erreur Snort EOF** → Corrigé automatiquement
- ✅ **network_mode: host** → Utilise bridge networking

### **Validation Complète**
```bash
# Test de connectivité
curl http://localhost:9080/
curl http://localhost:5601/
curl http://localhost:8000/docs

# Redémarrage d'urgence
docker compose down -v --remove-orphans
docker system prune -a
python setup_dev_environment.py
docker compose up -d --build
```

---

## 👥 Équipe ESGI 2024-2025

**🎯 Jakub WERLINSKI** - *Chef de projet*  
Architecture globale, coordination équipe

**🔐 Lucas BELMONTE** - *Développeur sécurité*  
HoneyPot Pro Max, système MFA, chiffrement

**🏗️ Evan RATSIMANOHATRA** - *Architecte infrastructure*  
Docker, ELK Stack, monitoring

### **Objectifs Pédagogiques Atteints**
- ✅ Développement sécurisé (MFA, chiffrement)
- ✅ Détection d'intrusion (IDS/HIDS)
- ✅ Analyse forensique (ELK Stack)
- ✅ DevSecOps (intégration sécurité)
- ✅ Tests d'intrusion (Red/Blue Team)

---

## 📚 Ressources

### **Documentation Complète**
- **README détaillé** : `README.md` (version complète)
- **API Swagger** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Scripts de test** : `scripts/` directory

### **Support**
- **GitHub Issues** : [Signaler un problème](https://github.com/BelmonteLucas/Projet_Annuel/issues)
- **Dépôt GitHub** : [Projet_Annuel](https://github.com/BelmonteLucas/Projet_Annuel)

---

*🛡️ "La meilleure défense, c'est de comprendre l'attaque" - Ce projet illustre cette philosophie en créant un laboratoire d'apprentissage cybersécurité complet.*