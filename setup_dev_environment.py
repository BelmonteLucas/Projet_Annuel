#!/usr/bin/env python3
"""
Setup Development Environment v2.0 - HoneyPot Pro Max
====================================================

Script principal d'installation avec architecture modulaire.
Responsabilité unique : Orchestrer les différents modules.

Usage:
    python setup_dev_environment.py [options]
    
Options:
    --skip-docker       Ignorer vérifications Docker
    --skip-encoding     Ignorer configuration encodage  
    --skip-ports        Ignorer vérification ports
    --quick             Installation rapide (skip non-critiques)

Auteur: Équipe ESGI 2024-2025
"""

import sys
import argparse
from pathlib import Path

# Import des modules spécialisés
try:
    from setup.colors import print_banner, print_colored, Colors
    from setup.system_checker import SystemChecker
    from setup.secrets_manager import SecretsManager
    from setup.project_configurator import ProjectConfigurator
except ImportError as e:
    print(f"❌ Erreur import modules: {e}")
    print("💡 Assurez-vous d'être dans le répertoire racine du projet")
    sys.exit(1)

class SetupOrchestrator:
    """Orchestrateur principal du setup"""
    
    def __init__(self, args):
        self.args = args
        self.results = {
            'system_check': False,
            'port_check': False,
            'secrets_generation': False,
            'project_config': False
        }
    
    def check_ports(self) -> bool:
        """Vérifie les conflits de ports (délégué au script existant)"""
        if self.args.skip_ports:
            print_colored("⏭️  Vérification ports ignorée", Colors.YELLOW)
            return True
            
        print_colored("\n=== 🔌 VÉRIFICATION CONFLITS PORTS ===", Colors.BOLD)
        
        try:
            import subprocess
            scripts_dir = Path("scripts")
            port_checker_script = scripts_dir / "check_port_conflicts.py"
            
            if not port_checker_script.exists():
                print_colored("⚠️  Script de vérification des ports non trouvé", Colors.YELLOW)
                return True
                
            result = subprocess.run([
                sys.executable, str(port_checker_script), "--no-report"
            ], capture_output=True, text=True)
            
            # Afficher seulement les conflits critiques pour ne pas polluer
            if result.returncode == 2:  # Conflits critiques
                print_colored("🚨 CONFLITS CRITIQUES DÉTECTÉS", Colors.RED)
                print_colored("💡 Exécutez: python scripts/check_port_conflicts.py", Colors.CYAN)
                print_colored("   pour voir les détails et solutions", Colors.CYAN)
                
                if not self.args.quick:
                    response = input("\nContinuer malgré les conflits ? (y/N): ").lower().strip()
                    if response not in ['y', 'yes', 'oui']:
                        print_colored("❌ Installation interrompue", Colors.RED)
                        sys.exit(1)
                        
            elif result.returncode == 1:  # Conflits mineurs
                print_colored("⚠️  Conflits mineurs détectés - Continuons", Colors.YELLOW)
            else:  # Pas de conflits
                print_colored("✅ Aucun conflit de port", Colors.GREEN)
                
            return True
            
        except Exception as e:
            print_colored(f"⚠️  Erreur vérification ports: {e}", Colors.YELLOW)
            return True  # Continue en cas d'erreur
    
    def create_validation_summary(self):
        """Crée un résumé de validation final"""
        print_colored("\n=== ✅ RÉSUMÉ DE L'INSTALLATION ===", Colors.BOLD)
        
        required_files = [
            'docker-compose.yml',
            'backend/main.py', 
            'frontend/index.html',
            'secrets/db_password.txt',
            'secrets/mfa_encryption_key.txt',
            'backend/db_encryption_key.txt'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print_colored("❌ Fichiers critiques manquants:", Colors.RED)
            for file in missing_files:
                print_colored(f"   - {file}", Colors.RED)
            return False
        
        # Afficher le statut de chaque étape
        steps = [
            ("Vérifications système", self.results['system_check']),
            ("Vérification ports", self.results['port_check']),
            ("Génération secrets", self.results['secrets_generation']),
            ("Configuration projet", self.results['project_config'])
        ]
        
        for step_name, success in steps:
            status = "✅" if success else "❌"
            color = Colors.GREEN if success else Colors.RED
            print_colored(f"{status} {step_name}", color)
        
        all_critical_ok = all([
            self.results['system_check'],
            self.results['secrets_generation']
        ])
        
        return all_critical_ok
    
    def print_next_steps(self):
        """Affiche les prochaines étapes"""
        print_colored(f"""
{Colors.GREEN}╔═══════════════════════════════════════════════════════════════╗
║                    🎉 INSTALLATION TERMINÉE !                ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}🚀 PROCHAINES ÉTAPES :{Colors.END}

{Colors.CYAN}1. Démarrer l'environnement :{Colors.END}
   docker compose up -d --build

{Colors.CYAN}2. Vérifier les services :{Colors.END}
   docker compose ps

{Colors.CYAN}3. Accéder aux interfaces :{Colors.END}
   • Frontend :  http://localhost:9080
   • Backend :   http://localhost:8000/docs  
   • Kibana :    http://localhost:5601
   • pgAdmin :   http://localhost:5050

{Colors.CYAN}4. En cas de problème :{Colors.END}
   python scripts/validate_installation.py

{Colors.GREEN}✅ Environnement prêt pour le développement !{Colors.END}
""")
    
    def run_setup(self):
        """Exécute l'installation complète"""
        print_banner()
        
        # 1. Vérifications système (critique)
        system_checker = SystemChecker()
        self.results['system_check'] = system_checker.check_all()
        
        if not self.results['system_check']:
            print_colored("\n❌ Prérequis système non respectés", Colors.RED)
            sys.exit(1)
        
        # 2. Vérification ports (importante mais pas bloquante)
        self.results['port_check'] = self.check_ports()
        
        # 3. Génération secrets (critique)
        secrets_manager = SecretsManager()
        self.results['secrets_generation'] = secrets_manager.generate_all()
        
        if not self.results['secrets_generation']:
            print_colored("\n❌ Impossible de générer les secrets", Colors.RED)
            sys.exit(1)
        
        # 4. Configuration projet (importante mais pas bloquante)
        if not self.args.skip_encoding:
            project_configurator = ProjectConfigurator()
            self.results['project_config'] = project_configurator.configure_all()
        else:
            print_colored("⏭️  Configuration encodage ignorée", Colors.YELLOW)
            self.results['project_config'] = True
        
        # 5. Validation finale
        if self.create_validation_summary():
            self.print_next_steps()
            sys.exit(0)
        else:
            print_colored("\n❌ Installation incomplète", Colors.RED)
            sys.exit(1)

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Setup automatique HoneyPot Pro Max v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
    python setup_dev_environment.py                 # Installation complète
    python setup_dev_environment.py --quick         # Installation rapide
    python setup_dev_environment.py --skip-docker   # Sans vérif Docker
        """
    )
    
    parser.add_argument('--skip-docker', action='store_true', 
                       help='Ignorer les vérifications Docker')
    parser.add_argument('--skip-encoding', action='store_true',
                       help='Ignorer la configuration encodage')
    parser.add_argument('--skip-ports', action='store_true',
                       help='Ignorer la vérification des ports')
    parser.add_argument('--quick', action='store_true',
                       help='Installation rapide (skip confirmations)')
    
    args = parser.parse_args()
    
    # Lancer l'orchestrateur
    orchestrator = SetupOrchestrator(args)
    orchestrator.run_setup()

if __name__ == "__main__":
    main()
