#!/usr/bin/env python3
"""
Détection des Conflits de Ports - HoneyPot Pro Max
==================================================

Script de vérification automatique des conflits de ports avant démarrage.
Identifie les ports occupés et propose des solutions.

Usage:
    python scripts/check_port_conflicts.py
    python scripts/check_port_conflicts.py --fix-automatically

Auteur: Jakub WERLINSKI
"""

import socket
import subprocess
import sys
import json
import argparse
from pathlib import Path
import re

class PortConflictChecker:
    def __init__(self):
        self.project_ports = {
            # Format: port -> (service_name, criticality, variable_name)
            9080: ("Frontend HTTP", "LOW", "FRONTEND_HTTP_PORT"),
            9443: ("Frontend HTTPS", "LOW", "FRONTEND_HTTPS_PORT"), 
            8000: ("Backend API", "MEDIUM", "BACKEND_PORT"),
            5432: ("PostgreSQL", "MEDIUM", "POSTGRES_PORT"),
            5601: ("Kibana", "MEDIUM", "KIBANA_PORT"),
            5050: ("pgAdmin", "LOW", "PGADMIN_PORT"),
            9200: ("Elasticsearch", "HIGH", "ELASTICSEARCH_PORT"),
            5044: ("Logstash", "MEDIUM", "LOGSTASH_PORT"),
            1514: ("Snort IDS", "CRITICAL", None),  # UDP
            1515: ("Wazuh Agents", "CRITICAL", None),
            55000: ("Wazuh API", "CRITICAL", None)
        }
        
        self.conflicts = []
        self.solutions = []
        
    def print_banner(self):
        """Affiche le banner de vérification"""
        print("""
🔌 VÉRIFICATION DES CONFLITS DE PORTS
====================================
🛡️ HoneyPot Pro Max
🔍 Détection automatique des ports occupés
        """)

    def is_port_in_use(self, port: int, protocol: str = "tcp") -> bool:
        """Vérifie si un port est utilisé"""
        try:
            if protocol == "tcp":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.5)  # Timeout plus court
                    result = s.connect_ex(('127.0.0.1', port))
                    return result == 0
            else:  # UDP
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(0.5)  # Timeout plus court
                    try:
                        s.bind(('127.0.0.1', port))
                        return False
                    except OSError:
                        return True
        except Exception:
            return False

    def get_process_using_port(self, port: int) -> str:
        """Identifie le processus utilisant un port"""
        try:
            if sys.platform == "win32":
                # Windows
                result = subprocess.run(
                    f'netstat -ano | findstr :{port}',
                    shell=True, capture_output=True, text=True
                )
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if f':{port}' in line and 'LISTENING' in line:
                            pid = line.split()[-1]
                            # Obtenir le nom du processus
                            tasklist_result = subprocess.run(
                                f'tasklist /FI "PID eq {pid}" /FO CSV',
                                shell=True, capture_output=True, text=True
                            )
                            if tasklist_result.stdout:
                                lines = tasklist_result.stdout.split('\n')[1:]
                                if lines and len(lines) > 0:
                                    process_name = lines[0].split(',')[0].strip('"')
                                    return f"{process_name} (PID: {pid})"
            else:
                # Linux/Mac
                result = subprocess.run(
                    f'lsof -i :{port}',
                    shell=True, capture_output=True, text=True
                )
                if result.stdout:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    if lines:
                        parts = lines[0].split()
                        return f"{parts[0]} (PID: {parts[1]})"
            
            return "Processus inconnu"
        except Exception as e:
            return f"Erreur lors de l'identification: {e}"

    def check_all_ports(self):
        """Vérifie tous les ports du projet"""
        print("🔍 Vérification des ports...")
        
        for port, (service, criticality, var_name) in self.project_ports.items():
            protocol = "udp" if port == 1514 else "tcp"
            
            if self.is_port_in_use(port, protocol):
                process = self.get_process_using_port(port)
                conflict = {
                    "port": port,
                    "service": service,
                    "criticality": criticality,
                    "variable_name": var_name,
                    "protocol": protocol,
                    "conflicting_process": process
                }
                self.conflicts.append(conflict)
                
                # Couleur selon criticité
                color = {
                    "LOW": "🟢",
                    "MEDIUM": "🟡", 
                    "HIGH": "🟠",
                    "CRITICAL": "🔴"
                }[criticality]
                
                print(f"   {color} CONFLIT Port {port} ({protocol.upper()}) - {service}")
                print(f"      └─ Utilisé par: {process}")
            else:
                print(f"   ✅ Port {port} ({protocol.upper()}) - {service} : LIBRE")

    def generate_solutions(self):
        """Génère des solutions pour chaque conflit"""
        if not self.conflicts:
            print("\n🎉 Aucun conflit détecté ! Vous pouvez lancer le projet.")
            return
            
        print(f"\n⚠️  {len(self.conflicts)} conflit(s) détecté(s)")
        print("\n🛠️ SOLUTIONS RECOMMANDÉES")
        print("=" * 50)
        
        for i, conflict in enumerate(self.conflicts, 1):
            port = conflict["port"]
            service = conflict["service"]
            criticality = conflict["criticality"]
            var_name = conflict["variable_name"]
            process = conflict["conflicting_process"]
            
            print(f"\n{i}. 🔌 Port {port} - {service} ({criticality})")
            print(f"   Conflit avec: {process}")
            
            if criticality in ["LOW", "MEDIUM"]:
                suggested_port = self.find_free_port(port + 1)
                print(f"   💡 Solution: Modifier le port vers {suggested_port}")
                if var_name:
                    print(f"   🔧 Variable: {var_name}={suggested_port}")
                    
                solution = {
                    "original_port": port,
                    "suggested_port": suggested_port,
                    "variable_name": var_name,
                    "docker_compose_change": f'"{port}:{port}" -> "{suggested_port}:{port}"'
                }
                self.solutions.append(solution)
                
            elif criticality == "HIGH":
                print(f"   ⚠️  Service critique - Vérifiez si vous pouvez arrêter:")
                print(f"   🛑 {process}")
                print(f"   💡 Ou modifiez la configuration Elasticsearch")
                
            else:  # CRITICAL
                print(f"   🚨 Service de sécurité critique !")
                print(f"   🛑 Processus à arrêter: {process}")
                print(f"   ⚠️  Impact: Monitoring de sécurité affecté")
                if port == 55000:
                    print(f"   🔧 Alternative: Modifier docker-compose.yml")
                    print(f"      Changer '55000:55000' -> '55001:55000'")
                    print(f"      Puis adapter config Wazuh si nécessaire")

    def find_free_port(self, start_port: int) -> int:
        """Trouve un port libre à partir d'un port donné"""
        for port in range(start_port, start_port + 100):
            if not self.is_port_in_use(port):
                return port
        return start_port + 1000  # fallback

    def generate_docker_compose_patch(self):
        """Génère un patch pour docker-compose.yml"""
        if not self.solutions:
            return
            
        print(f"\n📝 PATCH DOCKER-COMPOSE.YML")
        print("=" * 50)
        print("# Modifications recommandées pour docker-compose.yml:")
        print()
        
        for solution in self.solutions:
            original = solution["original_port"]
            suggested = solution["suggested_port"]
            change = solution["docker_compose_change"]
            
            print(f"# Port {original} -> {suggested}")
            print(f"# Changer: {change}")
            print()

    def save_report(self, filename: str = "port_conflict_report.json"):
        """Sauvegarde un rapport JSON"""
        report = {
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "total_ports_checked": len(self.project_ports),
            "conflicts_found": len(self.conflicts),
            "conflicts": self.conflicts,
            "solutions": self.solutions,
            "status": "CONFLICTS_FOUND" if self.conflicts else "ALL_CLEAR"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n📊 Rapport sauvegardé: {filename}")

    def check_windows_reserved_ports(self):
        """Vérifie les ports réservés par Windows"""
        if sys.platform != "win32":
            return
            
        try:
            result = subprocess.run(
                'netsh int ipv4 show excludedportrange protocol=tcp',
                shell=True, capture_output=True, text=True
            )
            
            if result.stdout and "excludedportrange" in result.stdout.lower():
                print("\n🪟 PORTS RÉSERVÉS WINDOWS DÉTECTÉS")
                print("=" * 50)
                print("Certains conflits peuvent être dus aux ports réservés par Windows.")
                print("Consultez la sortie complète avec:")
                print("netsh int ipv4 show excludedportrange protocol=tcp")
                
        except Exception as e:
            print(f"Impossible de vérifier les ports réservés Windows: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Vérification des conflits de ports pour HoneyPot Pro Max"
    )
    parser.add_argument(
        "--report", 
        default="port_conflict_report.json",
        help="Nom du fichier de rapport JSON"
    )
    parser.add_argument(
        "--no-report", 
        action="store_true",
        help="Ne pas générer de rapport"
    )
    
    args = parser.parse_args()
    
    checker = PortConflictChecker()
    checker.print_banner()
    
    # Vérifications principales
    checker.check_all_ports()
    checker.generate_solutions()
    checker.generate_docker_compose_patch()
    checker.check_windows_reserved_ports()
    
    # Rapport
    if not args.no_report:
        checker.save_report(args.report)
    
    # Code de sortie
    if checker.conflicts:
        critical_conflicts = [
            c for c in checker.conflicts 
            if c["criticality"] in ["HIGH", "CRITICAL"]
        ]
        if critical_conflicts:
            print("\n🚨 CONFLITS CRITIQUES DÉTECTÉS - Action requise avant démarrage")
            sys.exit(2)
        else:
            print("\n⚠️  Conflits détectés - Recommandations disponibles")
            sys.exit(1)
    else:
        print("\n✅ Aucun conflit - Prêt pour le démarrage")
        sys.exit(0)

if __name__ == "__main__":
    main()
