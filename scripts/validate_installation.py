#!/usr/bin/env python3
"""
Validation de l'Installation - HoneyPot Pro Max
======================================================

Script de validation automatique de l'installation complÃ¨te.
VÃ©rifie tous les composants mentionnÃ©s dans le README.

Usage:
    python scripts/validate_installation.py

Auteur: Ã‰quipe ESGI 2024-2025
"""

import requests
import subprocess
import time
import sys
from pathlib import Path
import json
from typing import Dict, List, Tuple

class InstallationValidator:
    def __init__(self):
        self.results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "overall_status": "UNKNOWN",
            "components": {},
            "recommendations": []
        }
        
    def print_banner(self):
        """Affiche le banner de validation"""
        print("""
ðŸ” VALIDATION DE L'INSTALLATION
===============================
ðŸ›¡ï¸  HoneyPot Pro Max
ðŸ“‹ VÃ©rification de tous les composants
        """)

    def check_docker_services(self) -> Dict:
        """VÃ©rifie l'Ã©tat des services Docker"""
        print("\nðŸ³ VÃ©rification des services Docker...")
        
        expected_services = [
            "postgres_db_service",
            "backend_api_service", 
            "pgadmin_service",
            "frontend_nginx_service",
            "elasticsearch",
            "logstash",
            "kibana",
            "snort_ids",
            "wazuh_manager"
        ]
        
        result = {
            "status": "UNKNOWN",
            "running_services": [],
            "stopped_services": [],
            "missing_services": [],
            "details": {}
        }
        
        try:
            # Obtenir la liste des conteneurs
            cmd_result = subprocess.run(
                ["docker", "compose", "ps", "--format", "json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            containers = []
            for line in cmd_result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        containers.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            
            # VÃ©rifier chaque service attendu
            for service in expected_services:
                found = False
                for container in containers:
                    if service in container.get("Name", ""):
                        found = True
                        status = container.get("State", "unknown")
                        result["details"][service] = status
                        
                        if status == "running":
                            result["running_services"].append(service)
                            print(f"   âœ… {service}: RUNNING")
                        else:
                            result["stopped_services"].append(service)
                            print(f"   âŒ {service}: {status}")
                        break
                
                if not found:
                    result["missing_services"].append(service)
                    print(f"   âš ï¸  {service}: NOT FOUND")
            
            # DÃ©terminer le statut global
            if len(result["running_services"]) == len(expected_services):
                result["status"] = "HEALTHY"
                print(f"\nâœ… Tous les services Docker sont opÃ©rationnels ({len(result['running_services'])}/{len(expected_services)})")
            elif len(result["running_services"]) > 0:
                result["status"] = "PARTIAL"
                print(f"\nâš ï¸  Services partiellement opÃ©rationnels ({len(result['running_services'])}/{len(expected_services)})")
            else:
                result["status"] = "FAILED"
                print(f"\nâŒ Aucun service opÃ©rationnel")
                
        except subprocess.CalledProcessError as e:
            result["status"] = "ERROR"
            result["error"] = str(e)
            print(f"âŒ Erreur lors de la vÃ©rification Docker: {e}")
        
        return result

    def check_web_interfaces(self) -> Dict:
        """VÃ©rifie l'accessibilitÃ© des interfaces web"""
        print("\nðŸŒ VÃ©rification des interfaces web...")
        
        endpoints = {
            "HoneyPot HTTP": "http://localhost:9080",
            "HoneyPot HTTPS": "https://localhost:9443", 
            "API Documentation": "http://localhost:8000/docs",
            "Kibana": "http://localhost:5601",
            "pgAdmin": "http://localhost:5050"
        }
        
        result = {
            "status": "UNKNOWN",
            "accessible": [],
            "inaccessible": [],
            "details": {}
        }
        
        for name, url in endpoints.items():
            try:
                response = requests.get(url, timeout=10, verify=False)
                if response.status_code == 200:
                    result["accessible"].append(name)
                    result["details"][name] = {"status": "OK", "code": response.status_code}
                    print(f"   âœ… {name}: ACCESSIBLE ({response.status_code})")
                else:
                    result["inaccessible"].append(name)
                    result["details"][name] = {"status": "ERROR", "code": response.status_code}
                    print(f"   âš ï¸  {name}: HTTP {response.status_code}")
                    
            except requests.RequestException as e:
                result["inaccessible"].append(name)
                result["details"][name] = {"status": "ERROR", "error": str(e)}
                print(f"   âŒ {name}: INACCESSIBLE ({e})")
        
        # DÃ©terminer le statut
        if len(result["accessible"]) == len(endpoints):
            result["status"] = "HEALTHY"
        elif len(result["accessible"]) > 0:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "FAILED"
        
        return result

    def check_api_endpoints(self) -> Dict:
        """VÃ©rifie les endpoints de l'API backend"""
        print("\nðŸ”Œ VÃ©rification des endpoints API...")
        
        endpoints = {
            "Root": "/",
            "Register": "/register",
            "Login": "/login", 
            "MFA Setup": "/mfa/setup",
            "MFA Status": "/mfa/status",
            "Password List": "/list"
        }
        
        base_url = "http://localhost:8000"
        
        result = {
            "status": "UNKNOWN",
            "available": [],
            "unavailable": [],
            "details": {}
        }
        
        for name, endpoint in endpoints.items():
            try:
                url = f"{base_url}{endpoint}"
                response = requests.get(url, timeout=5)
                
                # Pour les endpoints qui requiÃ¨rent POST ou authentication
                if response.status_code in [200, 405, 422, 401]:
                    result["available"].append(name)
                    result["details"][name] = {"status": "OK", "code": response.status_code}
                    print(f"   âœ… {name}: DISPONIBLE ({response.status_code})")
                else:
                    result["unavailable"].append(name)
                    result["details"][name] = {"status": "ERROR", "code": response.status_code}
                    print(f"   âš ï¸  {name}: HTTP {response.status_code}")
                    
            except requests.RequestException as e:
                result["unavailable"].append(name)
                result["details"][name] = {"status": "ERROR", "error": str(e)}
                print(f"   âŒ {name}: ERREUR ({e})")
        
        if len(result["available"]) == len(endpoints):
            result["status"] = "HEALTHY"
        elif len(result["available"]) > 0:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "FAILED"
        
        return result

    def check_secrets_configuration(self) -> Dict:
        """VÃ©rifie la configuration des secrets"""
        print("\nðŸ” VÃ©rification des secrets...")
        
        result = {
            "status": "UNKNOWN",
            "secrets_found": [],
            "secrets_missing": [],
            "details": {}
        }
        
        expected_secrets = [
            "secrets/db_password.txt",
            "secrets/mfa_encryption_key.txt"
        ]
        
        for secret_path in expected_secrets:
            path = Path(secret_path)
            if path.exists():
                result["secrets_found"].append(secret_path)
                # VÃ©rifier les permissions (Windows compatible)
                try:
                    stat_info = path.stat()
                    result["details"][secret_path] = {
                        "status": "OK",
                        "size": stat_info.st_size,
                        "permissions": oct(stat_info.st_mode)[-3:]
                    }
                    print(f"   âœ… {secret_path}: TROUVÃ‰ ({stat_info.st_size} bytes)")
                except Exception as e:
                    result["details"][secret_path] = {"status": "ERROR", "error": str(e)}
                    print(f"   âš ï¸  {secret_path}: ERREUR PERMISSIONS ({e})")
            else:
                result["secrets_missing"].append(secret_path)
                result["details"][secret_path] = {"status": "MISSING"}
                print(f"   âŒ {secret_path}: MANQUANT")
        
        if len(result["secrets_found"]) == len(expected_secrets):
            result["status"] = "HEALTHY"
        elif len(result["secrets_found"]) > 0:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "FAILED"
        
        return result

    def check_monitoring_stack(self) -> Dict:
        """VÃ©rifie la stack de monitoring (ELK + Snort + Wazuh)"""
        print("\nðŸ“Š VÃ©rification de la stack de monitoring...")
        
        result = {
            "status": "UNKNOWN",
            "components": {},
            "overall_health": "UNKNOWN"
        }
        
        # VÃ©rifier Elasticsearch
        try:
            response = requests.get("http://localhost:9200/_cluster/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                result["components"]["elasticsearch"] = {
                    "status": "OK",
                    "cluster_status": health_data.get("status", "unknown"),
                    "nodes": health_data.get("number_of_nodes", 0)
                }
                print(f"   âœ… Elasticsearch: OK ({health_data.get('status', 'unknown')})")
            else:
                result["components"]["elasticsearch"] = {"status": "ERROR", "code": response.status_code}
                print(f"   âŒ Elasticsearch: HTTP {response.status_code}")
        except requests.RequestException as e:
            result["components"]["elasticsearch"] = {"status": "ERROR", "error": str(e)}
            print(f"   âŒ Elasticsearch: INACCESSIBLE ({e})")
        
        # VÃ©rifier Kibana
        try:
            response = requests.get("http://localhost:5601/api/status", timeout=10)
            if response.status_code == 200:
                result["components"]["kibana"] = {"status": "OK"}
                print("   âœ… Kibana: OK")
            else:
                result["components"]["kibana"] = {"status": "ERROR", "code": response.status_code}
                print(f"   âš ï¸  Kibana: HTTP {response.status_code}")
        except requests.RequestException as e:
            result["components"]["kibana"] = {"status": "ERROR", "error": str(e)}
            print(f"   âŒ Kibana: INACCESSIBLE ({e})")
        
        # VÃ©rifier Snort (via Docker)
        try:
            cmd_result = subprocess.run(
                ["docker", "logs", "snort_ids", "--tail", "5"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if cmd_result.returncode == 0:
                result["components"]["snort"] = {"status": "OK", "logs_available": True}
                print("   âœ… Snort IDS: OK")
            else:
                result["components"]["snort"] = {"status": "ERROR", "error": "No logs"}
                print("   âš ï¸  Snort IDS: PAS DE LOGS")
        except subprocess.TimeoutExpired:
            result["components"]["snort"] = {"status": "ERROR", "error": "Timeout"}
            print("   âŒ Snort IDS: TIMEOUT")
        except Exception as e:
            result["components"]["snort"] = {"status": "ERROR", "error": str(e)}
            print(f"   âŒ Snort IDS: ERREUR ({e})")
        
        # VÃ©rifier Wazuh
        try:
            cmd_result = subprocess.run(
                ["docker", "logs", "wazuh_manager", "--tail", "5"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if cmd_result.returncode == 0:
                result["components"]["wazuh"] = {"status": "OK", "logs_available": True}
                print("   âœ… Wazuh HIDS: OK")
            else:
                result["components"]["wazuh"] = {"status": "ERROR", "error": "No logs"}
                print("   âš ï¸  Wazuh HIDS: PAS DE LOGS")
        except subprocess.TimeoutExpired:
            result["components"]["wazuh"] = {"status": "ERROR", "error": "Timeout"}
            print("   âŒ Wazuh HIDS: TIMEOUT")
        except Exception as e:
            result["components"]["wazuh"] = {"status": "ERROR", "error": str(e)}
            print(f"   âŒ Wazuh HIDS: ERREUR ({e})")
        
        # DÃ©terminer le statut global
        healthy_components = [comp for comp in result["components"].values() if comp["status"] == "OK"]
        if len(healthy_components) == len(result["components"]):
            result["status"] = "HEALTHY"
        elif len(healthy_components) > 0:
            result["status"] = "PARTIAL"
        else:
            result["status"] = "FAILED"
        
        return result

    def generate_recommendations(self):
        """GÃ©nÃ¨re des recommandations basÃ©es sur les rÃ©sultats"""
        recommendations = []
        
        # VÃ©rifier les services Docker
        docker_status = self.results["components"].get("docker_services", {}).get("status")
        if docker_status == "FAILED":
            recommendations.append("ðŸ³ Lancer les services Docker: docker compose up -d --build")
        elif docker_status == "PARTIAL":
            recommendations.append("ðŸ”„ RedÃ©marrer les services en Ã©chec: docker compose restart")
        
        # VÃ©rifier les secrets
        secrets_status = self.results["components"].get("secrets", {}).get("status")
        if secrets_status in ["FAILED", "PARTIAL"]:
            recommendations.append("ðŸ” ExÃ©cuter le script de setup: python setup_dev_environment.py")
        
        # VÃ©rifier les interfaces web
        web_status = self.results["components"].get("web_interfaces", {}).get("status")
        if web_status in ["FAILED", "PARTIAL"]:
            recommendations.append("â° Attendre le dÃ©marrage complet (2-3 minutes)")
            recommendations.append("ðŸ” VÃ©rifier les logs: docker compose logs")
        
        # VÃ©rifier le monitoring
        monitoring_status = self.results["components"].get("monitoring", {}).get("status")
        if monitoring_status in ["FAILED", "PARTIAL"]:
            recommendations.append("ðŸ“Š VÃ©rifier la stack ELK: docker compose logs elasticsearch kibana logstash")
            recommendations.append("ðŸ›¡ï¸  VÃ©rifier Snort/Wazuh: docker compose logs snort_ids wazuh_manager")
        
        return recommendations

    def run_full_validation(self) -> Dict:
        """ExÃ©cute la validation complÃ¨te"""
        self.print_banner()
        
        # ExÃ©cuter toutes les vÃ©rifications
        self.results["components"]["docker_services"] = self.check_docker_services()
        self.results["components"]["web_interfaces"] = self.check_web_interfaces()
        self.results["components"]["api_endpoints"] = self.check_api_endpoints()
        self.results["components"]["secrets"] = self.check_secrets_configuration()
        self.results["components"]["monitoring"] = self.check_monitoring_stack()
        
        # GÃ©nÃ©rer les recommandations
        self.results["recommendations"] = self.generate_recommendations()
        
        # DÃ©terminer le statut global
        component_statuses = [comp.get("status") for comp in self.results["components"].values()]
        
        if all(status == "HEALTHY" for status in component_statuses):
            self.results["overall_status"] = "HEALTHY"
        elif any(status == "HEALTHY" for status in component_statuses):
            self.results["overall_status"] = "PARTIAL"
        else:
            self.results["overall_status"] = "FAILED"
        
        self.print_summary()
        return self.results

    def print_summary(self):
        """Affiche le rÃ©sumÃ© de validation"""
        status_emoji = {
            "HEALTHY": "âœ…",
            "PARTIAL": "âš ï¸",
            "FAILED": "âŒ",
            "UNKNOWN": "â“"
        }
        
        emoji = status_emoji.get(self.results["overall_status"], "â“")
        
        print(f"""
ðŸ“‹ RÃ‰SUMÃ‰ DE VALIDATION
======================
{emoji} Statut global: {self.results["overall_status"]}
ðŸ• Timestamp: {self.results["timestamp"]}

ðŸ“Š COMPOSANTS:
""")
        
        for component, details in self.results["components"].items():
            status = details.get("status", "UNKNOWN")
            emoji = status_emoji.get(status, "â“")
            component_name = component.replace("_", " ").title()
            print(f"   {emoji} {component_name}: {status}")
        
        if self.results["recommendations"]:
            print(f"\nðŸ’¡ RECOMMANDATIONS:")
            for rec in self.results["recommendations"]:
                print(f"   {rec}")
        
        print(f"""
ðŸŽ¯ PROCHAINES Ã‰TAPES:
   1. RÃ©soudre les problÃ¨mes identifiÃ©s ci-dessus
   2. Lancer les tests de sÃ©curitÃ©: python scripts/security_tests.py
   3. Consulter Kibana pour le monitoring: http://localhost:5601
   4. Commencer vos tests d'intrusion !

ðŸ“ Rapport sauvegardÃ©: validation_report.json
        """)
        
        # Sauvegarder le rapport
        with open("validation_report.json", "w") as f:
            json.dump(self.results, f, indent=2)

def main():
    """Fonction principale"""
    validator = InstallationValidator()
    results = validator.run_full_validation()
    
    # Code de sortie basÃ© sur le statut
    if results["overall_status"] == "HEALTHY":
        sys.exit(0)
    elif results["overall_status"] == "PARTIAL":
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == "__main__":
    main()
