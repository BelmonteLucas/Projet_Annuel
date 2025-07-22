# 🚀 Installation Rapide - HoneyPot Pro Max

**Déploiement de votre laboratoire de cybersécurité en 5 minutes**

## ⚡ Installation Express

```bash
# 1. Cloner le projet
git clone https://github.com/BelmonteLucas/Projet_Annuel.git
cd Projet_Annuel

# 2. Configuration automatique
python setup_dev_environment.py

# 3. Lancement complet
docker compose up -d --build

# 4. Vérification (optionnel)
python scripts/validate_installation.py
```

## 🌐 Accès aux Services

| Service | URL | Identifiants |
|---------|-----|--------------|
| **HoneyPot Pro Max** | [http://localhost:9080](http://localhost:9080) | Créer un compte |
| **HoneyPot SSL** | [https://localhost:9443](https://localhost:9443) | Créer un compte |
| **Kibana Monitoring** | [http://localhost:5601](http://localhost:5601) | Accès direct |
| **pgAdmin Database** | [http://localhost:5050](http://localhost:5050) | `admin@admin.com` / `admin` |
| **API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) | Accès direct |

## ✅ Test de Fonctionnement

```bash
# Vérifier tous les services
curl http://localhost:9080/
curl http://localhost:5601/
curl http://localhost:8000/docs

# État des conteneurs
docker ps
```

## 🆘 En cas de Problème

```bash
# Redémarrage complet
docker compose down
docker compose up -d --build

# Logs d'un service
docker compose logs [nom_service]

# Nettoyage complet (si nécessaire)
docker compose down -v --remove-orphans
docker system prune -a
```

## 📋 Pré-requis

- **Docker** : version 20.x.x ou plus récent
- **Docker Compose** : version 2.x.x ou plus récent  
- **Python** : 3.8+ (pour les scripts de configuration)
- **Espace disque** : ~2GB pour les images Docker

---

**🔗 Documentation complète** : [README.md](README.md)  
**🛠️ Version optimisée** : [README-OPTIMIZED.md](README-OPTIMIZED.md)
