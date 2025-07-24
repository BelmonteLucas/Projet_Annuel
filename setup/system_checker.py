#!/usr/bin/env python3
"""
Module de Vérification Système - HoneyPot Pro Max
================================================

Responsabilité unique : Vérifications des prérequis système
- Python version
- Docker installation et configuration
- Permissions et compatibilité OS

Usage:
    from setup.system_checker import SystemChecker
    checker = SystemChecker()
    if not checker.check_all():
        exit(1)

Auteur: Jakub WERLINSKI
"""

import sys
import platform
import subprocess
from pathlib import Path
from .colors import Colors, print_colored

class SystemChecker:
    """Gestionnaire des vérifications système"""
    
    def __init__(self):
        self.results = {
            'python': False,
            'python_packages': False,
            'openssl': False,
            'docker': False,
            'docker_mode': False,
            'permissions': False
        }
    
    def check_python_version(self) -> bool:
        """Vérifie la version Python"""
        print_colored("🐍 Vérification Python...", Colors.BLUE)
        
        if sys.version_info < (3, 8):
            print_colored("❌ Python 3.8+ requis", Colors.RED)
            print_colored(f"   Version actuelle: {sys.version.split()[0]}", Colors.YELLOW)
            return False
        
        print_colored(f"✅ Python {sys.version.split()[0]} - OK", Colors.GREEN)
        return True
    
    def check_python_packages(self) -> bool:
        """Vérifie et installe les packages Python essentiels"""
        print_colored("📦 Vérification packages Python...", Colors.BLUE)
        
        required_packages = [
            ('cryptography', 'Chiffrement des secrets'),
            ('pathlib', 'Gestion des chemins de fichiers'),
            ('subprocess', 'Exécution de commandes système')
        ]
        
        missing_packages = []
        
        for package_name, description in required_packages:
            try:
                if package_name == 'pathlib':
                    # pathlib est intégré à Python 3.4+
                    from pathlib import Path
                elif package_name == 'subprocess':
                    # subprocess est intégré à Python
                    import subprocess as sp
                elif package_name == 'cryptography':
                    from cryptography.fernet import Fernet
                    
                print_colored(f"   ✅ {package_name} - OK", Colors.GREEN)
                
            except ImportError:
                print_colored(f"   ❌ {package_name} - Manquant ({description})", Colors.RED)
                missing_packages.append(package_name)
        
        # Installation automatique des packages manquants
        if missing_packages:
            print_colored("🔧 Installation des packages manquants...", Colors.YELLOW)
            
            for package in missing_packages:
                try:
                    print_colored(f"   📥 Installation de {package}...", Colors.BLUE)
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", package
                    ], capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0:
                        print_colored(f"   ✅ {package} installé avec succès", Colors.GREEN)
                    else:
                        print_colored(f"   ❌ Échec installation {package}: {result.stderr.strip()}", Colors.RED)
                        return False
                        
                except subprocess.TimeoutExpired:
                    print_colored(f"   ❌ Timeout lors de l'installation de {package}", Colors.RED)
                    return False
                except Exception as e:
                    print_colored(f"   ❌ Erreur installation {package}: {e}", Colors.RED)
                    return False
        
        return True
    
    def check_openssl_installation(self) -> bool:
        """Vérifie l'installation d'OpenSSL"""
        print_colored("🔐 Vérification OpenSSL...", Colors.BLUE)
        
        try:
            # Test direct de la cryptography qui dépend d'OpenSSL
            from cryptography.fernet import Fernet
            test_key = Fernet.generate_key()
            cipher = Fernet(test_key)
            test_data = b"test"
            encrypted = cipher.encrypt(test_data)
            decrypted = cipher.decrypt(encrypted)
            
            if decrypted == test_data:
                print_colored("✅ OpenSSL - Fonctionnel via cryptography", Colors.GREEN)
                return True
            else:
                print_colored("❌ OpenSSL - Dysfonctionnement cryptographique", Colors.RED)
                return False
                
        except ImportError:
            print_colored("❌ OpenSSL - cryptography non installé", Colors.RED)
            return False
        except Exception as e:
            print_colored(f"❌ OpenSSL - Erreur: {e}", Colors.RED)
            
            # Instructions spécifiques par OS
            os_name = platform.system().lower()
            if os_name == "windows":
                print_colored("💡 Solution Windows:", Colors.YELLOW)
                print_colored("   pip install --upgrade cryptography", Colors.CYAN)
                print_colored("   Ou installer Visual Studio Build Tools", Colors.CYAN)
            elif os_name == "linux":
                print_colored("💡 Solution Linux:", Colors.YELLOW)
                print_colored("   sudo apt-get install libssl-dev libffi-dev", Colors.CYAN)
                print_colored("   pip install --upgrade cryptography", Colors.CYAN)
            elif os_name == "darwin":  # macOS
                print_colored("💡 Solution macOS:", Colors.YELLOW)
                print_colored("   brew install openssl libffi", Colors.CYAN)
                print_colored("   pip install --upgrade cryptography", Colors.CYAN)
            
            return False
    
    def check_docker_installation(self) -> bool:
        """Vérifie l'installation Docker"""
        print_colored("🐳 Vérification Docker...", Colors.BLUE)
        
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            docker_version = result.stdout.strip()
            print_colored(f"✅ {docker_version}", Colors.GREEN)
            return True
            
        except FileNotFoundError:
            print_colored("❌ Docker non installé", Colors.RED)
            print_colored("💡 https://www.docker.com/products/docker-desktop", Colors.CYAN)
            return False
        except subprocess.CalledProcessError:
            print_colored("❌ Docker installé mais non fonctionnel", Colors.RED)
            return False
    
    def check_docker_daemon(self) -> bool:
        """Vérifie que le daemon Docker fonctionne"""
        print_colored("⚙️  Vérification daemon Docker...", Colors.BLUE)
        
        try:
            subprocess.run(['docker', 'info'], 
                          capture_output=True, text=True, check=True)
            print_colored("✅ Docker daemon actif", Colors.GREEN)
            return True
        except subprocess.CalledProcessError:
            print_colored("❌ Docker daemon non démarré", Colors.RED)
            print_colored("💡 Démarrez Docker Desktop", Colors.CYAN)
            return False
    
    def check_docker_mode(self) -> bool:
        """Vérifie le mode Docker (Linux containers requis)"""
        print_colored("🐧 Vérification mode Docker...", Colors.BLUE)
        
        try:
            result = subprocess.run(['docker', 'version', '--format', '{{.Server.Os}}'], 
                                  capture_output=True, text=True, check=True)
            docker_os = result.stdout.strip()
            
            if docker_os == 'linux':
                print_colored("✅ Mode Linux Containers - OK", Colors.GREEN)
                return True
            else:
                print_colored("❌ Mode Windows Containers détecté", Colors.RED)
                print_colored("💡 Basculer vers Linux Containers:", Colors.CYAN)
                print_colored("   1. Clic droit sur Docker Desktop", Colors.CYAN)
                print_colored("   2. 'Switch to Linux containers'", Colors.CYAN)
                return False
                
        except subprocess.CalledProcessError:
            print_colored("⚠️  Mode Docker indéterminé", Colors.YELLOW)
            return False
    
    def check_system_info(self):
        """Affiche les informations système"""
        print_colored("💻 Informations système:", Colors.BLUE)
        print_colored(f"   OS: {platform.system()} {platform.release()}", Colors.CYAN)
        print_colored(f"   Architecture: {platform.machine()}", Colors.CYAN)
        print_colored(f"   Python: {sys.version.split()[0]}", Colors.CYAN)
    
    def check_all(self) -> bool:
        """Exécute toutes les vérifications"""
        print_colored("\n=== 🔍 VÉRIFICATIONS SYSTÈME ===", Colors.BOLD)
        
        self.check_system_info()
        
        # Vérifications critiques dans l'ordre logique
        self.results['python'] = self.check_python_version()
        
        if self.results['python']:
            self.results['python_packages'] = self.check_python_packages()
            self.results['openssl'] = self.check_openssl_installation()
        
        self.results['docker'] = self.check_docker_installation()
        
        if self.results['docker']:
            self.results['docker_mode'] = self.check_docker_daemon() and self.check_docker_mode()
        
        # Résumé
        critical_checks = [
            self.results['python'],
            self.results['python_packages'],
            self.results['openssl'],
            self.results['docker']
        ]
        all_passed = all(critical_checks)
        
        if all_passed and self.results['docker_mode']:
            print_colored("\n✅ Système entièrement compatible - Prêt pour l'installation", Colors.GREEN)
            return True
        elif all_passed:
            print_colored("\n⚠️  Système compatible - Docker à configurer", Colors.YELLOW)
            return True
        else:
            print_colored("\n❌ Prérequis manquants - Installation impossible", Colors.RED)
            self._show_missing_requirements()
            return False
    
    def _show_missing_requirements(self):
        """Affiche les prérequis manquants"""
        print_colored("\n🔧 Prérequis manquants:", Colors.YELLOW)
        
        if not self.results['python']:
            print_colored("   - Python 3.8+ requis", Colors.RED)
        if not self.results['python_packages']:
            print_colored("   - Packages Python manquants", Colors.RED)
        if not self.results['openssl']:
            print_colored("   - OpenSSL/cryptography non fonctionnel", Colors.RED)
        if not self.results['docker']:
            print_colored("   - Docker non installé ou non accessible", Colors.RED)
