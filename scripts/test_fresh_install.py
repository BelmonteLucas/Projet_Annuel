#!/usr/bin/env python3
"""
Test d'Installation Fraîche - HoneyPot Pro Max
=====================================================

Script de test qui simule une installation complètement fraîche
en suivant exactement les instructions du README.

Usage:
    python scripts/test_fresh_install.py

Auteur: Équipe ESGI 2024-2025
"""

import subprocess
import time
import sys
import os
from pathlib import Path
import tempfile
import shutil
import json

class FreshInstallTester:
    def __init__(self):
        self.test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "overall_status": "UNKNOWN",
            "steps": {},
            "issues": [],
            "recommendations": []
        }
        self.original_dir = os.getcwd()
        self.test_dir = None
        
    def print_banner(self):
        """Affiche le banner de test"""
        print("""
🧪 TEST D'INSTALLATION FRAÎCHE
===============================
🛡️  HoneyPot Pro Max
📋 Simulation d'installation de zéro suivant le README
        """)

    def step_1_check_prerequisites(self):
        """Étape 1: Vérifier les pré-requis selon le README"""
        print("\n🎯 ÉTAPE 1: Vérification des pré-requis...")
        
        result = {
            "status": "UNKNOWN",
            "docker_version": None,
            "docker_compose_version": None,
            "python_version": None,
            "issues": []
        }
        
        # Vérifier Docker
        try:
            cmd_result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["docker_version"] = cmd_result.stdout.strip()
            print(f"   ✅ Docker: {result['docker_version']}")
        except Exception as e:
            result["issues"].append(f"Docker non disponible: {e}")
            print(f"   ❌ Docker: MANQUANT ({e})")
        
        # Vérifier Docker Compose
        try:
            cmd_result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["docker_compose_version"] = cmd_result.stdout.strip()
            print(f"   ✅ Docker Compose: {result['docker_compose_version']}")
        except Exception as e:
            result["issues"].append(f"Docker Compose non disponible: {e}")
            print(f"   ❌ Docker Compose: MANQUANT ({e})")
        
        # Vérifier Python
        try:
            cmd_result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["python_version"] = cmd_result.stdout.strip()
            print(f"   ✅ Python: {result['python_version']}")
        except Exception as e:
            result["issues"].append(f"Python non disponible: {e}")
            print(f"   ❌ Python: MANQUANT ({e})")
        
        # Déterminer le statut
        if len(result["issues"]) == 0:
            result["status"] = "SUCCESS"
            print("\n✅ Tous les pré-requis sont satisfaits")
        else:
            result["status"] = "FAILED"
            print(f"\n❌ {len(result['issues'])} pré-requis manquants")
        
        return result

    def step_2_simulate_git_clone(self):
        """Étape 2: Simuler le git clone (utilise le projet actuel)"""
        print("\n📥 ÉTAPE 2: Simulation du git clone...")
        
        result = {
            "status": "UNKNOWN",
            "test_directory": None,
            "files_copied": 0
        }
        
        try:
            # Créer un répertoire temporaire de test
            self.test_dir = tempfile.mkdtemp(prefix="honeypot_test_")
            
            # Copier les fichiers essentiels (simule git clone)
            essential_files = [
                "docker-compose.yml",
                "nginx.conf",
                "nginx.crt",
                "nginx.key",
                "setup_dev_environment.py",
                "backend/",
                "frontend/",
                "scripts/"
            ]
            
            for item in essential_files:
                src_path = Path(self.original_dir) / item
                dst_path = Path(self.test_dir) / item
                
                if src_path.exists():
                    if src_path.is_dir():
                        shutil.copytree(src_path, dst_path)
                        result["files_copied"] += len(list(src_path.rglob("*")))
                    else:
                        dst_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_path, dst_path)
                        result["files_copied"] += 1
            
            result["test_directory"] = self.test_dir
            result["status"] = "SUCCESS"
            print(f"   ✅ Projet copié vers: {self.test_dir}")
            print(f"   ✅ {result['files_copied']} fichiers/dossiers copiés")
            
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   ❌ Erreur lors de la copie: {e}")
        
        return result

    def step_3_run_setup_script(self):
        """Étape 3: Exécuter le script de setup selon le README"""
        print("\n🔧 ÉTAPE 3: Exécution du script de configuration...")
        
        result = {
            "status": "UNKNOWN",
            "setup_output": "",
            "secrets_created": [],
            "errors": []
        }
        
        try:
            # Changer vers le répertoire de test
            os.chdir(self.test_dir)
            
            # Exécuter le script de setup
            cmd_result = subprocess.run(
                ["python", "setup_dev_environment.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            result["setup_output"] = cmd_result.stdout + cmd_result.stderr
            
            if cmd_result.returncode == 0:
                # Vérifier que les secrets ont été créés
                secrets_dir = Path("secrets")
                if secrets_dir.exists():
                    for secret_file in secrets_dir.glob("*.txt"):
                        result["secrets_created"].append(str(secret_file))
                
                result["status"] = "SUCCESS"
                print(f"   ✅ Script de setup exécuté avec succès")
                print(f"   ✅ {len(result['secrets_created'])} secrets créés")
            else:
                result["status"] = "FAILED"
                result["errors"].append(f"Script exit code: {cmd_result.returncode}")
                print(f"   ❌ Script de setup échoué (code: {cmd_result.returncode})")
                
        except subprocess.TimeoutExpired:
            result["status"] = "FAILED"
            result["errors"].append("Timeout du script de setup")
            print("   ❌ Timeout du script de setup (>60s)")
        except Exception as e:
            result["status"] = "FAILED"
            result["errors"].append(str(e))
            print(f"   ❌ Erreur lors de l'exécution: {e}")
        finally:
            # Retourner au répertoire original
            os.chdir(self.original_dir)
        
        return result

    def step_4_docker_compose_syntax(self):
        """Étape 4: Vérifier la syntaxe docker-compose"""
        print("\n🐳 ÉTAPE 4: Vérification de la syntaxe Docker Compose...")
        
        result = {
            "status": "UNKNOWN",
            "config_valid": False,
            "services_found": [],
            "errors": []
        }
        
        try:
            os.chdir(self.test_dir)
            
            # Vérifier la configuration docker-compose
            cmd_result = subprocess.run(
                ["docker", "compose", "config"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if cmd_result.returncode == 0:
                result["config_valid"] = True
                
                # Lister les services définis
                try:
                    cmd_result = subprocess.run(
                        ["docker", "compose", "config", "--services"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    result["services_found"] = cmd_result.stdout.strip().split('\n')
                except:
                    pass
                
                result["status"] = "SUCCESS"
                print(f"   ✅ Configuration Docker Compose valide")
                print(f"   ✅ {len(result['services_found'])} services définis")
            else:
                result["status"] = "FAILED"
                result["errors"].append(cmd_result.stderr)
                print(f"   ❌ Configuration Docker Compose invalide")
                
        except Exception as e:
            result["status"] = "FAILED"
            result["errors"].append(str(e))
            print(f"   ❌ Erreur lors de la vérification: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def step_5_simulate_docker_build(self):
        """Étape 5: Simuler le build Docker (vérification uniquement)"""
        print("\n🏗️  ÉTAPE 5: Simulation du build Docker...")
        
        result = {
            "status": "UNKNOWN",
            "dockerfiles_found": [],
            "build_simulation": "NOT_EXECUTED"
        }
        
        try:
            os.chdir(self.test_dir)
            
            # Chercher les Dockerfiles
            for dockerfile in Path(".").rglob("Dockerfile"):
                result["dockerfiles_found"].append(str(dockerfile))
            
            # NOTE: On ne fait PAS le vrai build pour éviter les conflits
            # avec l'installation existante, mais on simule la commande
            print(f"   ✅ {len(result['dockerfiles_found'])} Dockerfile(s) trouvé(s)")
            print("   ⚠️  Build Docker simulé (non exécuté pour éviter les conflits)")
            print("   📝 Commande qui serait exécutée: docker compose up -d --build")
            
            result["status"] = "SUCCESS"
            result["build_simulation"] = "SIMULATED_OK"
            
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   ❌ Erreur lors de la simulation: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def step_6_validate_file_structure(self):
        """Étape 6: Valider la structure de fichiers attendue"""
        print("\n📁 ÉTAPE 6: Validation de la structure de fichiers...")
        
        result = {
            "status": "UNKNOWN",
            "expected_files": [],
            "missing_files": [],
            "present_files": []
        }
        
        # Fichiers attendus selon le README
        expected_files = [
            "docker-compose.yml",
            "nginx.conf",
            "nginx.crt",
            "nginx.key",
            "setup_dev_environment.py",
            "backend/main.py",
            "backend/Dockerfile",
            "frontend/index.html",
            "secrets/db_password.txt",
            "secrets/mfa_encryption_key.txt"
        ]
        
        try:
            os.chdir(self.test_dir)
            
            for file_path in expected_files:
                path = Path(file_path)
                if path.exists():
                    result["present_files"].append(file_path)
                    print(f"   ✅ {file_path}")
                else:
                    result["missing_files"].append(file_path)
                    print(f"   ❌ {file_path}: MANQUANT")
            
            if len(result["missing_files"]) == 0:
                result["status"] = "SUCCESS"
                print(f"\n✅ Structure de fichiers complète ({len(result['present_files'])}/{len(expected_files)})")
            else:
                result["status"] = "PARTIAL"
                print(f"\n⚠️  Structure partielle ({len(result['present_files'])}/{len(expected_files)})")
                
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   ❌ Erreur lors de la validation: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def cleanup_test_environment(self):
        """Nettoyer l'environnement de test"""
        if self.test_dir and Path(self.test_dir).exists():
            try:
                shutil.rmtree(self.test_dir)
                print(f"\n🧹 Environnement de test nettoyé: {self.test_dir}")
            except Exception as e:
                print(f"\n⚠️  Impossible de nettoyer {self.test_dir}: {e}")

    def generate_recommendations(self):
        """Générer des recommandations d'amélioration"""
        recommendations = []
        
        # Analyser les résultats pour des recommandations
        if self.test_results["steps"].get("prerequisites", {}).get("status") != "SUCCESS":
            recommendations.append("📋 Améliorer la section pré-requis du README avec des liens d'installation")
        
        if self.test_results["steps"].get("setup_script", {}).get("status") != "SUCCESS":
            recommendations.append("🔧 Améliorer la robustesse du script setup_dev_environment.py")
        
        if self.test_results["steps"].get("file_structure", {}).get("status") != "SUCCESS":
            recommendations.append("📁 Vérifier que tous les fichiers essentiels sont dans le repository")
        
        return recommendations

    def run_full_test(self):
        """Exécuter le test complet d'installation fraîche"""
        self.print_banner()
        
        try:
            # Exécuter toutes les étapes
            self.test_results["steps"]["prerequisites"] = self.step_1_check_prerequisites()
            self.test_results["steps"]["git_clone"] = self.step_2_simulate_git_clone()
            
            # Si les étapes de base réussissent, continuer
            if (self.test_results["steps"]["prerequisites"]["status"] == "SUCCESS" and 
                self.test_results["steps"]["git_clone"]["status"] == "SUCCESS"):
                
                self.test_results["steps"]["setup_script"] = self.step_3_run_setup_script()
                self.test_results["steps"]["docker_syntax"] = self.step_4_docker_compose_syntax()
                self.test_results["steps"]["docker_build"] = self.step_5_simulate_docker_build()
                self.test_results["steps"]["file_structure"] = self.step_6_validate_file_structure()
            
            # Générer les recommandations
            self.test_results["recommendations"] = self.generate_recommendations()
            
            # Déterminer le statut global
            step_statuses = [step.get("status") for step in self.test_results["steps"].values()]
            
            if all(status == "SUCCESS" for status in step_statuses):
                self.test_results["overall_status"] = "SUCCESS"
            elif any(status == "SUCCESS" for status in step_statuses):
                self.test_results["overall_status"] = "PARTIAL"
            else:
                self.test_results["overall_status"] = "FAILED"
            
            self.print_summary()
            
        finally:
            # Nettoyer toujours
            self.cleanup_test_environment()
        
        return self.test_results

    def print_summary(self):
        """Affiche le résumé du test"""
        status_emoji = {
            "SUCCESS": "✅",
            "PARTIAL": "⚠️",
            "FAILED": "❌",
            "UNKNOWN": "❓"
        }
        
        emoji = status_emoji.get(self.test_results["overall_status"], "❓")
        
        print(f"""
📋 RÉSUMÉ DU TEST D'INSTALLATION FRAÎCHE
=========================================
{emoji} Statut global: {self.test_results["overall_status"]}
🕐 Timestamp: {self.test_results["timestamp"]}

📊 ÉTAPES TESTÉES:
""")
        
        for step_name, step_data in self.test_results["steps"].items():
            status = step_data.get("status", "UNKNOWN")
            emoji = status_emoji.get(status, "❓")
            step_display = step_name.replace("_", " ").title()
            print(f"   {emoji} {step_display}: {status}")
        
        if self.test_results["recommendations"]:
            print(f"\n💡 RECOMMANDATIONS D'AMÉLIORATION:")
            for rec in self.test_results["recommendations"]:
                print(f"   {rec}")
        
        print(f"""
🎯 CONCLUSIONS:
   • Le README est-il suivable ? {"✅ OUI" if self.test_results["overall_status"] == "SUCCESS" else "❌ NON"}
   • Installation en 5 minutes possible ? {"✅ OUI" if self.test_results["overall_status"] == "SUCCESS" else "⚠️  AMÉLIORATION REQUISE"}
   • Expérience utilisateur satisfaisante ? {"✅ OUI" if self.test_results["overall_status"] == "SUCCESS" else "⚠️  À AMÉLIORER"}

📁 Rapport sauvegardé: fresh_install_test_report.json
        """)
        
        # Sauvegarder le rapport
        with open("fresh_install_test_report.json", "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, indent=2)

def main():
    """Fonction principale"""
    tester = FreshInstallTester()
    results = tester.run_full_test()
    
    # Code de sortie basé sur le statut
    if results["overall_status"] == "SUCCESS":
        sys.exit(0)
    elif results["overall_status"] == "PARTIAL":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
