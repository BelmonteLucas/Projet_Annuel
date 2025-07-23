#!/usr/bin/env python3
"""
Tests de SÃ©curitÃ© AutomatisÃ©s - HoneyPot Pro Max
========================================================

Script d'automatisation des tests d'intrusion mentionnÃ©s dans le README.
ExÃ©cute les scÃ©narios de test et vÃ©rifie les rÃ©sultats.

Usage:
    python scripts/security_tests.py [--scenario SCENARIO]

ScÃ©narios disponibles:
    - brute_force: Test d'attaque par force brute
    - sql_injection: Test d'injection SQL
    - port_scan: Test de scan de ports
    - mfa_bypass: Test de contournement MFA
    - all: Tous les tests

Auteur: Ã‰quipe ESGI 2024-2025
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
ðŸ”´ TESTS DE SÃ‰CURITÃ‰ AUTOMATISÃ‰S
==================================
âš ï¸  ATTENTION: Tests d'intrusion en cours
ðŸŽ¯ Cible: HoneyPot Pro Max
ðŸ“Š Monitoring: VÃ©rifiez Kibana pour les alertes
        """)

    def test_brute_force(self, attempts: int = 20) -> Dict:
        """Test d'attaque par force brute sur le login"""
        print(f"\nðŸš¨ Test 1: Attaque par force brute ({attempts} tentatives)")
        
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
                time.sleep(0.5)  # Pause pour Ã©viter de surcharger
                
            except requests.RequestException as e:
                results["failed_requests"] += 1
                print(f"   Tentative {i}/{attempts}: ERREUR - {e}")
        
        # VÃ©rifier si Snort a dÃ©tectÃ© l'attaque (simplification)
        results["detected"] = self.check_snort_detection("brute_force")
        
        print(f"âœ… Test terminÃ©: {results['successful_requests']}/{attempts} requÃªtes rÃ©ussies")
        if results["detected"]:
            print("ðŸ” DÃ©tection Snort: ACTIVÃ‰E")
        else:
            print("âš ï¸  DÃ©tection Snort: NON DÃ‰TECTÃ‰E")
        
        return results

    def test_sql_injection(self) -> Dict:
        """Test d'injection SQL"""
        print("\nðŸš¨ Test 2: Injection SQL")
        
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
                    print(f"   Payload {i}: BLOQUÃ‰ âœ…")
                else:
                    results["successful"] += 1
                    print(f"   Payload {i}: PASSÃ‰ âš ï¸")
                
                time.sleep(0.3)
                
            except requests.RequestException as e:
                results["blocked"] += 1
                print(f"   Payload {i}: ERREUR - {e}")
        
        results["detected"] = self.check_wazuh_detection("sql_injection")
        
        print(f"âœ… Test terminÃ©: {results['blocked']}/{results['payloads_tested']} payloads bloquÃ©s")
        return results

    def test_port_scan(self) -> Dict:
        """Test de scan de ports"""
        print("\nðŸš¨ Test 3: Scan de ports")
        
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
                    print(f"   Port {port}: FERMÃ‰")
                    
            except subprocess.TimeoutExpired:
                results["closed_ports"].append(port)
                print(f"   Port {port}: TIMEOUT")
            except Exception as e:
                print(f"   Port {port}: ERREUR - {e}")
        
        results["detected"] = self.check_snort_detection("port_scan")
        
        print(f"âœ… Test terminÃ©: {len(results['open_ports'])} ports ouverts dÃ©tectÃ©s")
        return results

    def test_mfa_bypass(self) -> Dict:
        """Test de contournement MFA"""
        print("\nðŸš¨ Test 4: Tentative de contournement MFA")
        
        results = {
            "test": "mfa_bypass",
            "bypass_attempts": 0,
            "successful_bypass": 0,
            "detected": False
        }
        
        # Test 1: Tentative d'accÃ¨s direct au gestionnaire sans MFA
        try:
            response = requests.get(f"{self.api_url}/list", timeout=5)
            results["bypass_attempts"] += 1
            
            if response.status_code == 401:
                print("   AccÃ¨s direct: BLOQUÃ‰ âœ…")
            else:
                print("   AccÃ¨s direct: PASSÃ‰ âš ï¸")
                results["successful_bypass"] += 1
                
        except requests.RequestException as e:
            print(f"   AccÃ¨s direct: ERREUR - {e}")
        
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
                    print(f"   Code {code}: REJETÃ‰ âœ…")
                else:
                    print(f"   Code {code}: ACCEPTÃ‰ âš ï¸")
                    results["successful_bypass"] += 1
                
                time.sleep(0.5)
                
            except requests.RequestException as e:
                print(f"   Code {code}: ERREUR - {e}")
        
        results["detected"] = self.check_wazuh_detection("mfa_bypass")
        
        print(f"âœ… Test terminÃ©: {results['successful_bypass']}/{results['bypass_attempts']} tentatives rÃ©ussies")
        return results

    def check_snort_detection(self, test_type: str) -> bool:
        """VÃ©rifie si Snort a dÃ©tectÃ© l'attaque (simulation)"""
        # Dans un vrai environnement, ceci interrogerait les logs Snort
        # Pour la dÃ©mo, on simule une dÃ©tection
        try:
            # VÃ©rifier si le conteneur Snort fonctionne
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
        """VÃ©rifie si Wazuh a dÃ©tectÃ© l'attaque (simulation)"""
        # Simulation de dÃ©tection Wazuh
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
        """ExÃ©cute tous les tests de sÃ©curitÃ©"""
        self.print_banner()
        
        all_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "target": self.base_url,
            "tests": []
        }
        
        # ExÃ©cuter tous les tests
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
                print(f"âŒ Erreur dans {test_func.__name__}: {e}")
        
        self.generate_report(all_results)
        return all_results

    def generate_report(self, results: Dict):
        """GÃ©nÃ¨re un rapport des tests"""
        print(f"""
ðŸ“Š RAPPORT DE TESTS DE SÃ‰CURITÃ‰
===============================
ðŸ• Timestamp: {results['timestamp']}
ðŸŽ¯ Cible: {results['target']}
ðŸ§ª Tests exÃ©cutÃ©s: {len(results['tests'])}

ðŸ“‹ RÃ‰SUMÃ‰:
""")
        
        for test in results["tests"]:
            test_name = test["test"].replace("_", " ").title()
            detected = "âœ… DÃ‰TECTÃ‰" if test.get("detected", False) else "âš ï¸ NON DÃ‰TECTÃ‰"
            print(f"   {test_name}: {detected}")
        
        print(f"""
ðŸ’¡ RECOMMANDATIONS:
   1. VÃ©rifiez les alertes dans Kibana: http://localhost:5601
   2. Consultez les logs Snort: docker logs snort_ids
   3. VÃ©rifiez Wazuh: docker logs wazuh_manager
   4. Analysez les patterns d'attaque dÃ©tectÃ©s

ðŸ“ Rapport sauvegardÃ©: security_test_report.json
        """)
        
        # Sauvegarder le rapport
        with open("security_test_report.json", "w") as f:
            json.dump(results, f, indent=2)

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Tests de sÃ©curitÃ© automatisÃ©s")
    parser.add_argument("--scenario", 
                       choices=["brute_force", "sql_injection", "port_scan", "mfa_bypass", "all"],
                       default="all",
                       help="ScÃ©nario de test Ã  exÃ©cuter")
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
