#!/usr/bin/env python3
"""
Rapport de Conformité README - HoneyPot Pro Max
=====================================================

Compare l'état réel du projet avec ce qui est décrit dans le README.
Génère un rapport de conformité détaillé.

Usage:
    python scripts/readme_compliance_check.py

Auteur: Équipe ESGI 2024-2025
"""

import json
import os
from pathlib import Path
import subprocess
import requests

class ReadmeComplianceChecker:
    def __init__(self):
        self.compliance_report = {
            "timestamp": "",
            "overall_compliance": 0,
            "sections": {},
            "missing_elements": [],
            "implemented_elements": [],
            "recommendations": []
        }
    
    def check_architecture_components(self):
        """Vérifie les composants d'architecture mentionnés dans le README"""
        print("🏗️ Vérification de l'architecture...")
        
        components = {
            "docker-compose.yml": {"exists": Path("docker-compose.yml").exists(), "description": "Orchestration Docker"},
            "nginx.conf": {"exists": Path("nginx.conf").exists(), "description": "Configuration NGINX SSL"},
            "secrets/": {"exists": Path("secrets").exists(), "description": "Gestion sécurisée des secrets"},
            "elk/": {"exists": Path("elk").exists(), "description": "Stack ELK pour monitoring"},
            "snort/": {"exists": Path("snort").exists(), "description": "Configuration Snort IDS"},
            "wazuh/": {"exists": Path("wazuh").exists(), "description": "Configuration Wazuh HIDS"},
            "backend/main.py": {"exists": Path("backend/main.py").exists(), "description": "API FastAPI"},
            "frontend/index.html": {"exists": Path("frontend/index.html").exists(), "description": "Interface HoneyPot Pro Max"}
        }
        
        implemented = 0
        total = len(components)
        
        for component, info in components.items():
            if info["exists"]:
                print(f"   ✅ {component}: {info['description']}")
                implemented += 1
                self.compliance_report["implemented_elements"].append(f"Architecture: {component}")
            else:
                print(f"   ❌ {component}: MANQUANT - {info['description']}")
                self.compliance_report["missing_elements"].append(f"Architecture: {component}")
        
        self.compliance_report["sections"]["architecture"] = {
            "score": (implemented / total) * 100,
            "implemented": implemented,
            "total": total
        }
        
        return (implemented / total) * 100

    def check_readme_features(self):
        """Vérifie les fonctionnalités décrites dans le README"""
        print("\n🔐 Vérification des fonctionnalités...")
        
        features = {
            "MFA/2FA System": self.check_mfa_implementation(),
            "Password Manager": self.check_password_manager(),
            "SSL/HTTPS": self.check_ssl_implementation(),
            "Monitoring Stack": self.check_monitoring_stack(),
            "Security Tests": self.check_security_tests(),
            "Installation Scripts": self.check_installation_scripts()
        }
        
        implemented = sum(1 for implemented in features.values() if implemented)
        total = len(features)
        
        for feature, is_implemented in features.items():
            status = "✅" if is_implemented else "❌"
            print(f"   {status} {feature}")
            
            if is_implemented:
                self.compliance_report["implemented_elements"].append(f"Feature: {feature}")
            else:
                self.compliance_report["missing_elements"].append(f"Feature: {feature}")
        
        self.compliance_report["sections"]["features"] = {
            "score": (implemented / total) * 100,
            "implemented": implemented,
            "total": total
        }
        
        return (implemented / total) * 100

    def check_mfa_implementation(self):
        """Vérifie l'implémentation MFA"""
        try:
            # Vérifier l'endpoint MFA
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200 and "mfa" in response.text.lower():
                return True
        except:
            pass
        
        # Vérifier dans le code backend
        if Path("backend/main.py").exists():
            with open("backend/main.py", "r", encoding="utf-8") as f:
                content = f.read()
                return "mfa" in content.lower() and "totp" in content.lower()
        
        return False

    def check_password_manager(self):
        """Vérifie l'implémentation du gestionnaire de mots de passe"""
        if Path("frontend/index.html").exists():
            with open("frontend/index.html", "r", encoding="utf-8") as f:
                content = f.read()
                return "honeypot" in content.lower() and "password" in content.lower()
        return False

    def check_ssl_implementation(self):
        """Vérifie l'implémentation SSL"""
        ssl_files = Path("nginx.crt").exists() and Path("nginx.key").exists()
        nginx_config = False
        
        if Path("nginx.conf").exists():
            with open("nginx.conf", "r", encoding="utf-8") as f:
                content = f.read()
                nginx_config = "ssl" in content.lower() and "443" in content
        
        return ssl_files and nginx_config

    def check_monitoring_stack(self):
        """Vérifie la stack de monitoring"""
        elk_dirs = all(Path(f"elk/{component}").exists() for component in ["elasticsearch", "logstash", "kibana"])
        security_dirs = Path("snort").exists() and Path("wazuh").exists()
        
        return elk_dirs and security_dirs

    def check_security_tests(self):
        """Vérifie les scripts de test de sécurité"""
        return Path("scripts/security_tests.py").exists()

    def check_installation_scripts(self):
        """Vérifie les scripts d'installation"""
        return Path("setup_dev_environment.py").exists()

    def check_readme_urls(self):
        """Vérifie les URLs mentionnées dans le README"""
        print("\n🌐 Vérification des URLs du README...")
        
        urls = {
            "HoneyPot HTTP": "http://localhost:9080",
            "HoneyPot HTTPS": "https://localhost:9443",
            "API Documentation": "http://localhost:8000/docs",
            "Kibana": "http://localhost:5601",
            "pgAdmin": "http://localhost:5050"
        }
        
        accessible = 0
        total = len(urls)
        
        for name, url in urls.items():
            try:
                response = requests.get(url, timeout=5, verify=False)
                if response.status_code == 200:
                    print(f"   ✅ {name}: ACCESSIBLE")
                    accessible += 1
                    self.compliance_report["implemented_elements"].append(f"URL: {name}")
                else:
                    print(f"   ⚠️ {name}: HTTP {response.status_code}")
                    self.compliance_report["missing_elements"].append(f"URL: {name} (HTTP {response.status_code})")
            except:
                print(f"   ❌ {name}: INACCESSIBLE")
                self.compliance_report["missing_elements"].append(f"URL: {name} (inaccessible)")
        
        self.compliance_report["sections"]["urls"] = {
            "score": (accessible / total) * 100,
            "accessible": accessible,
            "total": total
        }
        
        return (accessible / total) * 100

    def check_documentation_accuracy(self):
        """Vérifie l'exactitude de la documentation"""
        print("\n📋 Vérification de la documentation...")
        
        checks = {
            "Installation en 5 minutes": self.check_quick_install(),
            "Script setup_dev_environment.py": Path("setup_dev_environment.py").exists(),
            "Commande docker compose up": self.check_docker_compose(),
            "Scripts de validation": Path("scripts/validate_installation.py").exists(),
            "Tests de sécurité": Path("scripts/security_tests.py").exists()
        }
        
        accurate = sum(1 for is_accurate in checks.values() if is_accurate)
        total = len(checks)
        
        for check, is_accurate in checks.items():
            status = "✅" if is_accurate else "❌"
            print(f"   {status} {check}")
            
            if is_accurate:
                self.compliance_report["implemented_elements"].append(f"Documentation: {check}")
            else:
                self.compliance_report["missing_elements"].append(f"Documentation: {check}")
        
        self.compliance_report["sections"]["documentation"] = {
            "score": (accurate / total) * 100,
            "accurate": accurate,
            "total": total
        }
        
        return (accurate / total) * 100

    def check_quick_install(self):
        """Vérifie si l'installation rapide fonctionne"""
        return Path("setup_dev_environment.py").exists() and Path("docker-compose.yml").exists()

    def check_docker_compose(self):
        """Vérifie la configuration Docker Compose"""
        try:
            result = subprocess.run(["docker", "compose", "config"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False

    def generate_recommendations(self):
        """Génère des recommandations d'amélioration"""
        recommendations = []
        
        # Recommandations basées sur les éléments manquants
        if "URL: HoneyPot HTTP" in [item for item in self.compliance_report["missing_elements"] if "URL:" in item]:
            recommendations.append("🚀 Démarrer l'application: docker compose up -d")
        
        if "Architecture: secrets/" in self.compliance_report["missing_elements"]:
            recommendations.append("🔐 Exécuter le setup: python setup_dev_environment.py")
        
        if any("Feature:" in item for item in self.compliance_report["missing_elements"]):
            recommendations.append("⚙️ Implémenter les fonctionnalités manquantes")
        
        if any("Documentation:" in item for item in self.compliance_report["missing_elements"]):
            recommendations.append("📝 Mettre à jour la documentation")
        
        # Recommandations générales
        if self.compliance_report["overall_compliance"] < 90:
            recommendations.append("🎯 Viser 90%+ de conformité pour la présentation")
        
        self.compliance_report["recommendations"] = recommendations
        return recommendations

    def run_full_compliance_check(self):
        """Exécute la vérification complète de conformité"""
        print("""
📋 VÉRIFICATION DE CONFORMITÉ README
===================================
🛡️ HoneyPot Pro Max
📊 Comparaison projet réel vs documentation
        """)
        
        # Exécuter toutes les vérifications
        architecture_score = self.check_architecture_components()
        features_score = self.check_readme_features()
        urls_score = self.check_readme_urls()
        documentation_score = self.check_documentation_accuracy()
        
        # Calculer le score global
        overall_score = (architecture_score + features_score + urls_score + documentation_score) / 4
        self.compliance_report["overall_compliance"] = round(overall_score, 1)
        
        # Générer les recommandations
        recommendations = self.generate_recommendations()
        
        # Afficher le résumé
        self.print_compliance_summary()
        
        return self.compliance_report

    def print_compliance_summary(self):
        """Affiche le résumé de conformité"""
        score = self.compliance_report["overall_compliance"]
        
        # Déterminer l'emoji et le niveau
        if score >= 90:
            emoji = "🎉"
            level = "EXCELLENT"
        elif score >= 80:
            emoji = "✅"
            level = "TRÈS BON"
        elif score >= 70:
            emoji = "⚠️"
            level = "BON"
        else:
            emoji = "❌"
            level = "À AMÉLIORER"
        
        print(f"""
📊 RÉSUMÉ DE CONFORMITÉ
======================
{emoji} Score global: {score}% ({level})

📋 DÉTAIL PAR SECTION:
""")
        
        for section_name, section_data in self.compliance_report["sections"].items():
            section_score = round(section_data["score"], 1)
            implemented = section_data.get("implemented", section_data.get("accessible", section_data.get("accurate", 0)))
            total = section_data["total"]
            
            print(f"   • {section_name.title()}: {section_score}% ({implemented}/{total})")
        
        if self.compliance_report["recommendations"]:
            print(f"\n💡 RECOMMANDATIONS:")
            for rec in self.compliance_report["recommendations"]:
                print(f"   {rec}")
        
        print(f"""
🎯 OBJECTIF: 90%+ pour une présentation parfaite
📁 Rapport détaillé: readme_compliance_report.json
        """)
        
        # Sauvegarder le rapport
        with open("readme_compliance_report.json", "w", encoding="utf-8") as f:
            json.dump(self.compliance_report, f, indent=2)

def main():
    """Fonction principale"""
    checker = ReadmeComplianceChecker()
    report = checker.run_full_compliance_check()
    
    # Code de retour basé sur le score
    if report["overall_compliance"] >= 90:
        return 0
    elif report["overall_compliance"] >= 70:
        return 1
    else:
        return 2

if __name__ == "__main__":
    exit(main())
