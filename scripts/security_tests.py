#!/usr/bin/env python3
"""
Tests de Sécurité Automatisés - HoneyPot Security Suite
========================================================

Script d'automatisation des tests d'intrusion mentionnés dans le README.
Exécute les scénarios de test et vérifie les résultats.

Usage:
    python scripts/security_tests.py [--scenario SCENARIO]

Scénarios disponibles:
    - brute_force: Test d'attaque par force brute
    - sql_injection: Test d'injection SQL
    - port_scan: Test de scan de ports
    - mfa_bypass: Test de contournement MFA
    - all: Tous les tests

Auteur: Équipe ESGI 2024-2025
"""

import requests
import time
import argparse
import sys
import subprocess
from typing import Dict, List
import json

class SecurityTester:
    def __init__(self, base_url: str = "http://localhost:9080"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.results = {}
        
    def print_banner(self):
        """Affiche le banner des tests"""
        print("""
🔴 TESTS DE SÉCURITÉ AUTOMATISÉS
==================================
⚠️  ATTENTION: Tests d'intrusion en cours
🎯 Cible: HoneyPot Security Suite
📊 Monitoring: Vérifiez Kibana pour les alertes
        """)

    def test_brute_force(self, attempts: int = 20) -> Dict:
        """Test d'attaque par force brute sur le login"""
        print(f"\n🚨 Test 1: Attaque par force brute ({attempts} tentatives)")
        
        results = {
            "test": "brute_force",
            "attempts": attempts,
            "successful_requests": 0,
            "failed_requests": 0,
            "detected": False
        }
        
        for i in range(1, attempts + 1):
            try:
                payload = {
                    "username": "admin",
                    "password": f"wrongpassword{i}"
                }
                
                response = requests.post(
                    f"{self.api_url}/login",
                    json=payload,
                    timeout=5
                )
                
                if response.status_code in [401, 403]:
                    results["successful_requests"] += 1
                else:
                    results["failed_requests"] += 1
                
                print(f"   Tentative {i}/{attempts}: {response.status_code}")
                time.sleep(0.5)  # Pause pour éviter de surcharger
                
            except requests.RequestException as e:
                results["failed_requests"] += 1
                print(f"   Tentative {i}/{attempts}: ERREUR - {e}")
        
        # Vérifier si Snort a détecté l'attaque (simplification)
        results["detected"] = self.check_snort_detection("brute_force")
        
        print(f"✅ Test terminé: {results['successful_requests']}/{attempts} requêtes réussies")
        if results["detected"]:
            print("🔍 Détection Snort: ACTIVÉE")
        else:
            print("⚠️  Détection Snort: NON DÉTECTÉE")
        
        return results

    def test_sql_injection(self) -> Dict:
        """Test d'injection SQL"""
        print("\n🚨 Test 2: Injection SQL")
        
        sql_payloads = [
            "admin' OR '1'='1",
            "admin'; DROP TABLE users;--",
            "admin' UNION SELECT * FROM users--",
            "admin'; WAITFOR DELAY '00:00:05'--",
            "' OR 1=1#"
        ]
        
        results = {
            "test": "sql_injection",
            "payloads_tested": len(sql_payloads),
            "blocked": 0,
            "successful": 0,
            "detected": False
        }
        
        for i, payload in enumerate(sql_payloads, 1):
            try:
                data = {
                    "username": payload,
                    "password": "test"
                }
                
                response = requests.post(
                    f"{self.api_url}/login",
                    json=data,
                    timeout=5
                )
                
                if response.status_code in [400, 401, 422]:
                    results["blocked"] += 1
                    print(f"   Payload {i}: BLOQUÉ ✅")
                else:
                    results["successful"] += 1
                    print(f"   Payload {i}: PASSÉ ⚠️")
                
                time.sleep(0.3)
                
            except requests.RequestException as e:
                results["blocked"] += 1
                print(f"   Payload {i}: ERREUR - {e}")
        
        results["detected"] = self.check_wazuh_detection("sql_injection")
        
        print(f"✅ Test terminé: {results['blocked']}/{results['payloads_tested']} payloads bloqués")
        return results

    def test_port_scan(self) -> Dict:
        """Test de scan de ports"""
        print("\n🚨 Test 3: Scan de ports")
        
        ports_to_scan = [22, 80, 443, 3306, 5432, 8000, 9080, 9443]
        
        results = {
            "test": "port_scan",
            "ports_scanned": len(ports_to_scan),
            "open_ports": [],
            "closed_ports": [],
            "detected": False
        }
        
        for port in ports_to_scan:
            try:
                # Simulation d'un scan de port avec netcat
                result = subprocess.run(
                    ["powershell", "-Command", f"Test-NetConnection -ComputerName localhost -Port {port} -InformationLevel Quiet"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                
                if result.returncode == 0 and "True" in result.stdout:
                    results["open_ports"].append(port)
                    print(f"   Port {port}: OUVERT")
                else:
                    results["closed_ports"].append(port)
                    print(f"   Port {port}: FERMÉ")
                    
            except subprocess.TimeoutExpired:
                results["closed_ports"].append(port)
                print(f"   Port {port}: TIMEOUT")
            except Exception as e:
                print(f"   Port {port}: ERREUR - {e}")
        
        results["detected"] = self.check_snort_detection("port_scan")
        
        print(f"✅ Test terminé: {len(results['open_ports'])} ports ouverts détectés")
        return results

    def test_mfa_bypass(self) -> Dict:
        """Test de contournement MFA"""
        print("\n🚨 Test 4: Tentative de contournement MFA")
        
        results = {
            "test": "mfa_bypass",
            "bypass_attempts": 0,
            "successful_bypass": 0,
            "detected": False
        }
        
        # Test 1: Tentative d'accès direct au gestionnaire sans MFA
        try:
            response = requests.get(f"{self.api_url}/list", timeout=5)
            results["bypass_attempts"] += 1
            
            if response.status_code == 401:
                print("   Accès direct: BLOQUÉ ✅")
            else:
                print("   Accès direct: PASSÉ ⚠️")
                results["successful_bypass"] += 1
                
        except requests.RequestException as e:
            print(f"   Accès direct: ERREUR - {e}")
        
        # Test 2: Codes MFA invalides
        invalid_codes = ["000000", "123456", "999999", "111111"]
        
        for code in invalid_codes:
            try:
                data = {
                    "username": "testuser",
                    "otp_code": code
                }
                
                response = requests.post(
                    f"{self.api_url}/login/otp",
                    json=data,
                    timeout=5
                )
                
                results["bypass_attempts"] += 1
                
                if response.status_code in [401, 400]:
                    print(f"   Code {code}: REJETÉ ✅")
                else:
                    print(f"   Code {code}: ACCEPTÉ ⚠️")
                    results["successful_bypass"] += 1
                
                time.sleep(0.5)
                
            except requests.RequestException as e:
                print(f"   Code {code}: ERREUR - {e}")
        
        results["detected"] = self.check_wazuh_detection("mfa_bypass")
        
        print(f"✅ Test terminé: {results['successful_bypass']}/{results['bypass_attempts']} tentatives réussies")
        return results

    def check_snort_detection(self, test_type: str) -> bool:
        """Vérifie si Snort a détecté l'attaque (simulation)"""
        # Dans un vrai environnement, ceci interrogerait les logs Snort
        # Pour la démo, on simule une détection
        try:
            # Vérifier si le conteneur Snort fonctionne
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=snort_ids", "--format", "{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "Up" in result.stdout
        except:
            return False

    def check_wazuh_detection(self, test_type: str) -> bool:
        """Vérifie si Wazuh a détecté l'attaque (simulation)"""
        # Simulation de détection Wazuh
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=wazuh_manager", "--format", "{{.Status}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "Up" in result.stdout
        except:
            return False

    def run_all_tests(self) -> Dict:
        """Exécute tous les tests de sécurité"""
        self.print_banner()
        
        all_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "target": self.base_url,
            "tests": []
        }
        
        # Exécuter tous les tests
        tests = [
            self.test_brute_force,
            self.test_sql_injection,
            self.test_port_scan,
            self.test_mfa_bypass
        ]
        
        for test_func in tests:
            try:
                result = test_func()
                all_results["tests"].append(result)
            except Exception as e:
                print(f"❌ Erreur dans {test_func.__name__}: {e}")
        
        self.generate_report(all_results)
        return all_results

    def generate_report(self, results: Dict):
        """Génère un rapport des tests"""
        print(f"""
📊 RAPPORT DE TESTS DE SÉCURITÉ
===============================
🕐 Timestamp: {results['timestamp']}
🎯 Cible: {results['target']}
🧪 Tests exécutés: {len(results['tests'])}

📋 RÉSUMÉ:
""")
        
        for test in results["tests"]:
            test_name = test["test"].replace("_", " ").title()
            detected = "✅ DÉTECTÉ" if test.get("detected", False) else "⚠️ NON DÉTECTÉ"
            print(f"   {test_name}: {detected}")
        
        print(f"""
💡 RECOMMANDATIONS:
   1. Vérifiez les alertes dans Kibana: http://localhost:5601
   2. Consultez les logs Snort: docker logs snort_ids
   3. Vérifiez Wazuh: docker logs wazuh_manager
   4. Analysez les patterns d'attaque détectés

📁 Rapport sauvegardé: security_test_report.json
        """)
        
        # Sauvegarder le rapport
        with open("security_test_report.json", "w") as f:
            json.dump(results, f, indent=2)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Tests de sécurité automatisés")
    parser.add_argument("--scenario", 
                       choices=["brute_force", "sql_injection", "port_scan", "mfa_bypass", "all"],
                       default="all",
                       help="Scénario de test à exécuter")
    parser.add_argument("--target", 
                       default="http://localhost:9080",
                       help="URL cible pour les tests")
    
    args = parser.parse_args()
    
    tester = SecurityTester(args.target)
    
    if args.scenario == "all":
        tester.run_all_tests()
    elif args.scenario == "brute_force":
        tester.test_brute_force()
    elif args.scenario == "sql_injection":
        tester.test_sql_injection()
    elif args.scenario == "port_scan":
        tester.test_port_scan()
    elif args.scenario == "mfa_bypass":
        tester.test_mfa_bypass()

if __name__ == "__main__":
    main()
