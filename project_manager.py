#!/usr/bin/env python3
"""
Gestionnaire du Projet - HoneyPot Security Suite
===============================================

Script utilitaire pour gérer facilement le projet.
Centralise toutes les opérations courantes.

Usage:
    python project_manager.py [command] [options]

Commandes disponibles:
    setup      - Configuration initiale de l'environnement
    start      - Démarrer tous les services
    stop       - Arrêter tous les services
    restart    - Redémarrer tous les services
    status     - Vérifier le statut des services
    validate   - Valider l'installation complète
    test       - Lancer les tests de sécurité
    logs       - Afficher les logs des services
    clean      - Nettoyer l'environnement
    help       - Afficher cette aide

Auteur: Équipe ESGI 2024-2025
"""

import argparse
import subprocess
import sys
import os
import time
from pathlib import Path

class ProjectManager:
    def __init__(self):
        self.project_root = Path.cwd()
        
    def print_banner(self):
        """Affiche le banner du gestionnaire"""
        print("""
🛡️  HoneyPot Security Suite - Project Manager
==============================================
🎓 Projet Annuel ESGI 2024-2025
⚙️  Gestionnaire centralisé du projet
        """)

    def setup_environment(self):
        """Configure l'environnement de développement"""
        print("🔧 Configuration de l'environnement de développement...")
        
        try:
            # Exécuter le script de setup
            result = subprocess.run([sys.executable, "setup_dev_environment.py"], check=True)
            print("✅ Configuration terminée avec succès !")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la configuration: {e}")
            return False
        except FileNotFoundError:
            print("❌ Script setup_dev_environment.py non trouvé")
            return False

    def start_services(self):
        """Démarre tous les services Docker"""
        print("🚀 Démarrage de tous les services...")
        
        try:
            # Démarrer avec build
            subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
            print("✅ Services démarrés avec succès !")
            
            print("\n⏰ Attente du démarrage complet (30 secondes)...")
            time.sleep(30)
            
            self.show_access_urls()
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du démarrage: {e}")
            return False

    def stop_services(self):
        """Arrête tous les services Docker"""
        print("🛑 Arrêt de tous les services...")
        
        try:
            subprocess.run(["docker", "compose", "down"], check=True)
            print("✅ Services arrêtés avec succès !")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'arrêt: {e}")
            return False

    def restart_services(self):
        """Redémarre tous les services"""
        print("🔄 Redémarrage des services...")
        
        if self.stop_services():
            time.sleep(5)
            return self.start_services()
        return False

    def check_status(self):
        """Vérifie le statut des services"""
        print("📊 Vérification du statut des services...")
        
        try:
            result = subprocess.run(["docker", "compose", "ps"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de la vérification: {e}")
            return False

    def validate_installation(self):
        """Lance la validation complète"""
        print("🔍 Validation de l'installation...")
        
        try:
            result = subprocess.run([sys.executable, "scripts/validate_installation.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Validation terminée avec des avertissements (code {e.returncode})")
            return False
        except FileNotFoundError:
            print("❌ Script de validation non trouvé")
            return False

    def run_security_tests(self, scenario="all"):
        """Lance les tests de sécurité"""
        print(f"🔴 Lancement des tests de sécurité (scénario: {scenario})...")
        
        try:
            cmd = [sys.executable, "scripts/security_tests.py", "--scenario", scenario]
            result = subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors des tests: {e}")
            return False
        except FileNotFoundError:
            print("❌ Script de tests non trouvé")
            return False

    def show_logs(self, service=None):
        """Affiche les logs des services"""
        if service:
            print(f"📜 Logs du service {service}...")
            cmd = ["docker", "compose", "logs", "-f", "--tail", "50", service]
        else:
            print("📜 Logs de tous les services...")
            cmd = ["docker", "compose", "logs", "-f", "--tail", "20"]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'affichage des logs: {e}")
        except KeyboardInterrupt:
            print("\n📜 Affichage des logs interrompu")

    def clean_environment(self):
        """Nettoie l'environnement Docker"""
        print("🧹 Nettoyage de l'environnement...")
        
        try:
            # Arrêter et supprimer les conteneurs, volumes, et réseaux
            subprocess.run(["docker", "compose", "down", "-v", "--remove-orphans"], check=True)
            
            # Nettoyer les images non utilisées
            subprocess.run(["docker", "system", "prune", "-f"], check=True)
            
            print("✅ Environnement nettoyé avec succès !")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors du nettoyage: {e}")
            return False

    def show_access_urls(self):
        """Affiche les URLs d'accès"""
        print("""
🌐 URLS D'ACCÈS:
===============
🎯 SecureVault HTTP  : http://localhost:9080
🔐 SecureVault HTTPS : https://localhost:9443
📊 Kibana           : http://localhost:5601
🗄️  pgAdmin          : http://localhost:5050
🔌 API Docs         : http://localhost:8000/docs
        """)

    def show_help(self):
        """Affiche l'aide complète"""
        print("""
📋 COMMANDES DISPONIBLES:
========================

🔧 setup      - Configuration initiale de l'environnement
   Crée les secrets, configure l'environnement

🚀 start      - Démarrer tous les services
   Lance Docker Compose avec build automatique

🛑 stop       - Arrêter tous les services
   Arrête proprement tous les conteneurs

🔄 restart    - Redémarrer tous les services
   Équivalent à stop + start

📊 status     - Vérifier le statut des services
   Affiche l'état de tous les conteneurs

🔍 validate   - Valider l'installation complète
   Vérifie tous les composants et génère un rapport

🔴 test       - Lancer les tests de sécurité
   Options: --scenario [brute_force|sql_injection|port_scan|mfa_bypass|all]

📜 logs       - Afficher les logs des services
   Options: --service [nom_du_service] pour un service spécifique

🧹 clean      - Nettoyer l'environnement
   Supprime conteneurs, volumes et images inutilisées

❓ help       - Afficher cette aide

📖 EXEMPLES D'UTILISATION:
=========================
python project_manager.py setup                    # Configuration initiale
python project_manager.py start                     # Démarrage complet
python project_manager.py test --scenario all       # Tests de sécurité
python project_manager.py logs --service backend    # Logs du backend
python project_manager.py validate                  # Validation complète
        """)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Gestionnaire du projet HoneyPot Security Suite")
    parser.add_argument("command", 
                       choices=["setup", "start", "stop", "restart", "status", "validate", "test", "logs", "clean", "help"],
                       help="Commande à exécuter")
    parser.add_argument("--scenario", 
                       choices=["brute_force", "sql_injection", "port_scan", "mfa_bypass", "all"],
                       default="all",
                       help="Scénario de test pour la commande 'test'")
    parser.add_argument("--service",
                       help="Service spécifique pour la commande 'logs'")
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    manager.print_banner()
    
    success = True
    
    if args.command == "setup":
        success = manager.setup_environment()
    elif args.command == "start":
        success = manager.start_services()
    elif args.command == "stop":
        success = manager.stop_services()
    elif args.command == "restart":
        success = manager.restart_services()
    elif args.command == "status":
        success = manager.check_status()
    elif args.command == "validate":
        success = manager.validate_installation()
    elif args.command == "test":
        success = manager.run_security_tests(args.scenario)
    elif args.command == "logs":
        manager.show_logs(args.service)
    elif args.command == "clean":
        success = manager.clean_environment()
    elif args.command == "help":
        manager.show_help()
    
    if not success and args.command != "help" and args.command != "logs":
        sys.exit(1)

if __name__ == "__main__":
    main()
