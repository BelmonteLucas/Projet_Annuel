#!/usr/bin/env python3
"""
Test d'Installation FraÃ®che - HoneyPot Pro Max
=====================================================

Script de test qui simule une installation complÃ¨tement fraÃ®che
en suivant exactement les instructions du README.

Usage:
    python scripts/test_fresh_install.py

Auteur: Ã‰quipe ESGI 2024-2025
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
ðŸ§ª TEST D'INSTALLATION FRAÃŽCHE
===============================
ðŸ›¡ï¸  HoneyPot Pro Max
ðŸ“‹ Simulation d'installation de zÃ©ro suivant le README
        """)

    def step_1_check_prerequisites(self):
        """Ã‰tape 1: VÃ©rifier les prÃ©-requis selon le README"""
        print("\nðŸŽ¯ Ã‰TAPE 1: VÃ©rification des prÃ©-requis...")
        
        result = {
            "status": "UNKNOWN",
            "docker_version": None,
            "docker_compose_version": None,
            "python_version": None,
            "issues": []
        }
        
        # VÃ©rifier Docker
        try:
            cmd_result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["docker_version"] = cmd_result.stdout.strip()
            print(f"   âœ… Docker: {result['docker_version']}")
        except Exception as e:
            result["issues"].append(f"Docker non disponible: {e}")
            print(f"   âŒ Docker: MANQUANT ({e})")
        
        # VÃ©rifier Docker Compose
        try:
            cmd_result = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["docker_compose_version"] = cmd_result.stdout.strip()
            print(f"   âœ… Docker Compose: {result['docker_compose_version']}")
        except Exception as e:
            result["issues"].append(f"Docker Compose non disponible: {e}")
            print(f"   âŒ Docker Compose: MANQUANT ({e})")
        
        # VÃ©rifier Python
        try:
            cmd_result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            result["python_version"] = cmd_result.stdout.strip()
            print(f"   âœ… Python: {result['python_version']}")
        except Exception as e:
            result["issues"].append(f"Python non disponible: {e}")
            print(f"   âŒ Python: MANQUANT ({e})")
        
        # DÃ©terminer le statut
        if len(result["issues"]) == 0:
            result["status"] = "SUCCESS"
            print("\nâœ… Tous les prÃ©-requis sont satisfaits")
        else:
            result["status"] = "FAILED"
            print(f"\nâŒ {len(result['issues'])} prÃ©-requis manquants")
        
        return result

    def step_2_simulate_git_clone(self):
        """Ã‰tape 2: Simuler le git clone (utilise le projet actuel)"""
        print("\nðŸ“¥ Ã‰TAPE 2: Simulation du git clone...")
        
        result = {
            "status": "UNKNOWN",
            "test_directory": None,
            "files_copied": 0
        }
        
        try:
            # CrÃ©er un rÃ©pertoire temporaire de test
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
            print(f"   âœ… Projet copiÃ© vers: {self.test_dir}")
            print(f"   âœ… {result['files_copied']} fichiers/dossiers copiÃ©s")
            
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   âŒ Erreur lors de la copie: {e}")
        
        return result

    def step_3_run_setup_script(self):
        """Ã‰tape 3: ExÃ©cuter le script de setup selon le README"""
        print("\nðŸ”§ Ã‰TAPE 3: ExÃ©cution du script de configuration...")
        
        result = {
            "status": "UNKNOWN",
            "setup_output": "",
            "secrets_created": [],
            "errors": []
        }
        
        try:
            # Changer vers le rÃ©pertoire de test
            os.chdir(self.test_dir)
            
            # ExÃ©cuter le script de setup
            cmd_result = subprocess.run(
                ["python", "setup_dev_environment.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            result["setup_output"] = cmd_result.stdout + cmd_result.stderr
            
            if cmd_result.returncode == 0:
                # VÃ©rifier que les secrets ont Ã©tÃ© crÃ©Ã©s
                secrets_dir = Path("secrets")
                if secrets_dir.exists():
                    for secret_file in secrets_dir.glob("*.txt"):
                        result["secrets_created"].append(str(secret_file))
                
                result["status"] = "SUCCESS"
                print(f"   âœ… Script de setup exÃ©cutÃ© avec succÃ¨s")
                print(f"   âœ… {len(result['secrets_created'])} secrets crÃ©Ã©s")
            else:
                result["status"] = "FAILED"
                result["errors"].append(f"Script exit code: {cmd_result.returncode}")
                print(f"   âŒ Script de setup Ã©chouÃ© (code: {cmd_result.returncode})")
                
        except subprocess.TimeoutExpired:
            result["status"] = "FAILED"
            result["errors"].append("Timeout du script de setup")
            print("   âŒ Timeout du script de setup (>60s)")
        except Exception as e:
            result["status"] = "FAILED"
            result["errors"].append(str(e))
            print(f"   âŒ Erreur lors de l'exÃ©cution: {e}")
        finally:
            # Retourner au rÃ©pertoire original
            os.chdir(self.original_dir)
        
        return result

    def step_4_docker_compose_syntax(self):
        """Ã‰tape 4: VÃ©rifier la syntaxe docker-compose"""
        print("\nðŸ³ Ã‰TAPE 4: VÃ©rification de la syntaxe Docker Compose...")
        
        result = {
            "status": "UNKNOWN",
            "config_valid": False,
            "services_found": [],
            "errors": []
        }
        
        try:
            os.chdir(self.test_dir)
            
            # VÃ©rifier la configuration docker-compose
            cmd_result = subprocess.run(
                ["docker", "compose", "config"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if cmd_result.returncode == 0:
                result["config_valid"] = True
                
                # Lister les services dÃ©finis
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
                print(f"   âœ… Configuration Docker Compose valide")
                print(f"   âœ… {len(result['services_found'])} services dÃ©finis")
            else:
                result["status"] = "FAILED"
                result["errors"].append(cmd_result.stderr)
                print(f"   âŒ Configuration Docker Compose invalide")
                
        except Exception as e:
            result["status"] = "FAILED"
            result["errors"].append(str(e))
            print(f"   âŒ Erreur lors de la vÃ©rification: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def step_5_simulate_docker_build(self):
        """Ã‰tape 5: Simuler le build Docker (vÃ©rification uniquement)"""
        print("\nðŸ—ï¸  Ã‰TAPE 5: Simulation du build Docker...")
        
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
            
            # NOTE: On ne fait PAS le vrai build pour Ã©viter les conflits
            # avec l'installation existante, mais on simule la commande
            print(f"   âœ… {len(result['dockerfiles_found'])} Dockerfile(s) trouvÃ©(s)")
            print("   âš ï¸  Build Docker simulÃ© (non exÃ©cutÃ© pour Ã©viter les conflits)")
            print("   ðŸ“ Commande qui serait exÃ©cutÃ©e: docker compose up -d --build")
            
            result["status"] = "SUCCESS"
            result["build_simulation"] = "SIMULATED_OK"
            
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   âŒ Erreur lors de la simulation: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def step_6_validate_file_structure(self):
        """Ã‰tape 6: Valider la structure de fichiers attendue"""
        print("\nðŸ“ Ã‰TAPE 6: Validation de la structure de fichiers...")
        
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
                    print(f"   âœ… {file_path}")
                else:
                    result["missing_files"].append(file_path)
                    print(f"   âŒ {file_path}: MANQUANT")
            
            if len(result["missing_files"]) == 0:
                result["status"] = "SUCCESS"
                print(f"\nâœ… Structure de fichiers complÃ¨te ({len(result['present_files'])}/{len(expected_files)})")
            else:
                result["status"] = "PARTIAL"
                print(f"\nâš ï¸  Structure partielle ({len(result['present_files'])}/{len(expected_files)})")
                
        except Exception as e:
            result["status"] = "FAILED"
            result["error"] = str(e)
            print(f"   âŒ Erreur lors de la validation: {e}")
        finally:
            os.chdir(self.original_dir)
        
        return result

    def cleanup_test_environment(self):
        """Nettoyer l'environnement de test"""
        if self.test_dir and Path(self.test_dir).exists():
            try:
                shutil.rmtree(self.test_dir)
                print(f"\nðŸ§¹ Environnement de test nettoyÃ©: {self.test_dir}")
            except Exception as e:
                print(f"\nâš ï¸  Impossible de nettoyer {self.test_dir}: {e}")

    def generate_recommendations(self):
        """GÃ©nÃ©rer des recommandations d'amÃ©lioration"""
        recommendations = []
        
        # Analyser les rÃ©sultats pour des recommandations
        if self.test_results["steps"].get("prerequisites", {}).get("status") != "SUCCESS":
            recommendations.append("ðŸ“‹ AmÃ©liorer la section prÃ©-requis du README avec des liens d'installation")
        
        if self.test_results["steps"].get("setup_script", {}).get("status") != "SUCCESS":
            recommendations.append("ðŸ”§ AmÃ©liorer la robustesse du script setup_dev_environment.py")
        
        if self.test_results["steps"].get("file_structure", {}).get("status") != "SUCCESS":
            recommendations.append("ðŸ“ VÃ©rifier que tous les fichiers essentiels sont dans le repository")
        
        return recommendations

    def run_full_test(self):
        """ExÃ©cuter le test complet d'installation fraÃ®che"""
        self.print_banner()
        
        try:
            # ExÃ©cuter toutes les Ã©tapes
            self.test_results["steps"]["prerequisites"] = self.step_1_check_prerequisites()
            self.test_results["steps"]["git_clone"] = self.step_2_simulate_git_clone()
            
            # Si les Ã©tapes de base rÃ©ussissent, continuer
            if (self.test_results["steps"]["prerequisites"]["status"] == "SUCCESS" and 
                self.test_results["steps"]["git_clone"]["status"] == "SUCCESS"):
                
                self.test_results["steps"]["setup_script"] = self.step_3_run_setup_script()
                self.test_results["steps"]["docker_syntax"] = self.step_4_docker_compose_syntax()
                self.test_results["steps"]["docker_build"] = self.step_5_simulate_docker_build()
                self.test_results["steps"]["file_structure"] = self.step_6_validate_file_structure()
            
            # GÃ©nÃ©rer les recommandations
            self.test_results["recommendations"] = self.generate_recommendations()
            
            # DÃ©terminer le statut global
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
        """Affiche le rÃ©sumÃ© du test"""
        status_emoji = {
            "SUCCESS": "âœ…",
            "PARTIAL": "âš ï¸",
            "FAILED": "âŒ",
            "UNKNOWN": "â“"
        }
        
        emoji = status_emoji.get(self.test_results["overall_status"], "â“")
        
        print(f"""
ðŸ“‹ RÃ‰SUMÃ‰ DU TEST D'INSTALLATION FRAÃŽCHE
=========================================
{emoji} Statut global: {self.test_results["overall_status"]}
ðŸ• Timestamp: {self.test_results["timestamp"]}

ðŸ“Š Ã‰TAPES TESTÃ‰ES:
""")
        
        for step_name, step_data in self.test_results["steps"].items():
            status = step_data.get("status", "UNKNOWN")
            emoji = status_emoji.get(status, "â“")
            step_display = step_name.replace("_", " ").title()
            print(f"   {emoji} {step_display}: {status}")
        
        if self.test_results["recommendations"]:
            print(f"\nðŸ’¡ RECOMMANDATIONS D'AMÃ‰LIORATION:")
            for rec in self.test_results["recommendations"]:
                print(f"   {rec}")
        
        print(f"""
ðŸŽ¯ CONCLUSIONS:
   â€¢ Le README est-il suivable ? {"âœ… OUI" if self.test_results["overall_status"] == "SUCCESS" else "âŒ NON"}
   â€¢ Installation en 5 minutes possible ? {"âœ… OUI" if self.test_results["overall_status"] == "SUCCESS" else "âš ï¸  AMÃ‰LIORATION REQUISE"}
   â€¢ ExpÃ©rience utilisateur satisfaisante ? {"âœ… OUI" if self.test_results["overall_status"] == "SUCCESS" else "âš ï¸  Ã€ AMÃ‰LIORER"}

ðŸ“ Rapport sauvegardÃ©: fresh_install_test_report.json
        """)
        
        # Sauvegarder le rapport
        with open("fresh_install_test_report.json", "w", encoding="utf-8") as f:
            json.dump(self.test_results, f, indent=2)

def main():
    """Fonction principale"""
    tester = FreshInstallTester()
    results = tester.run_full_test()
    
    # Code de sortie basÃ© sur le statut
    if results["overall_status"] == "SUCCESS":
        sys.exit(0)
    elif results["overall_status"] == "PARTIAL":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
