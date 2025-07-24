#!/usr/bin/env python3
"""
Module Générateur de Secrets - HoneyPot Pro Max
==============================================

Responsabilité unique : Génération et gestion des secrets
- Clés de chiffrement (MFA, DB)
- Mots de passe sécurisés
- Certificats SSL
- Structure sécurisée des répertoires

Usage:
    from setup.secrets_manager import SecretsManager
    manager = SecretsManager()
    manager.generate_all()

Auteur: Jakub WERLINSKI
"""

import os
import secrets
import string
import subprocess
from pathlib import Path
from cryptography.fernet import Fernet
from .colors import Colors, print_colored

class SecretsManager:
    """Gestionnaire de génération des secrets"""
    
    def __init__(self):
        self.secrets_dir = Path("secrets")
        self.backend_dir = Path("backend")
        
    def create_secure_directories(self) -> bool:
        """Crée les répertoires avec permissions sécurisées"""
        print_colored("📁 Création répertoires sécurisés...", Colors.BLUE)
        
        try:
            # Répertoire secrets principal
            if not self.secrets_dir.exists():
                self.secrets_dir.mkdir(mode=0o700, exist_ok=True)
                print_colored("✅ Répertoire secrets/ créé", Colors.GREEN)
            else:
                print_colored("ℹ️  Répertoire secrets/ existe déjà", Colors.BLUE)
                
            # Vérifier permissions Unix (Linux/Mac)
            if hasattr(os, 'chmod'):
                os.chmod(self.secrets_dir, 0o700)
            
            return True
            
        except Exception as e:
            print_colored(f"❌ Erreur création répertoires: {e}", Colors.RED)
            return False
    
    def generate_database_keys(self) -> bool:
        """Génère les clés de chiffrement pour la base de données"""
        print_colored("🔑 Génération clés de chiffrement DB...", Colors.BLUE)
        
        db_key_path = self.secrets_dir / "db_encryption_key.txt"
        
        if db_key_path.exists():
            print_colored("ℹ️  Clé DB existe déjà", Colors.BLUE)
            return True
            
        try:
            key = Fernet.generate_key()
            
            # Créer la clé uniquement dans secrets/
            with open(db_key_path, "wb") as f:
                f.write(key)
            
            # Permissions restrictives
            if hasattr(os, 'chmod'):
                os.chmod(db_key_path, 0o600)
            
            print_colored("✅ Clé de chiffrement DB générée", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"❌ Erreur génération clé DB: {e}", Colors.RED)
            return False
    
    def generate_mfa_key(self) -> bool:
        """Génère la clé de chiffrement MFA"""
        print_colored("🔐 Génération clé MFA...", Colors.BLUE)
        
        mfa_key_path = self.secrets_dir / "mfa_encryption_key.txt"
        
        if mfa_key_path.exists():
            print_colored("ℹ️  Clé MFA existe déjà", Colors.BLUE)
            return True
            
        try:
            mfa_key = Fernet.generate_key()
            
            with open(mfa_key_path, "wb") as f:
                f.write(mfa_key)
            
            # Permissions restrictives
            if hasattr(os, 'chmod'):
                os.chmod(mfa_key_path, 0o600)
            
            print_colored("✅ Clé MFA générée", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"❌ Erreur génération clé MFA: {e}", Colors.RED)
            return False
    
    def generate_database_password(self) -> bool:
        """Génère un mot de passe sécurisé pour PostgreSQL"""
        print_colored("🔒 Génération mot de passe DB...", Colors.BLUE)
        
        db_pwd_path = self.secrets_dir / "db_password.txt"
        
        if db_pwd_path.exists():
            print_colored("ℹ️  Mot de passe DB existe déjà", Colors.BLUE)
            return True
            
        try:
            # Génération d'un mot de passe fort (32 caractères, 4 types)
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(alphabet) for _ in range(32))
            
            # Vérifier qu'on a au moins un caractère de chaque type
            has_lower = any(c.islower() for c in password)
            has_upper = any(c.isupper() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_special = any(c in "!@#$%^&*" for c in password)
            
            # Régénérer si critères non respectés
            while not all([has_lower, has_upper, has_digit, has_special]):
                password = ''.join(secrets.choice(alphabet) for _ in range(32))
                has_lower = any(c.islower() for c in password)
                has_upper = any(c.isupper() for c in password)
                has_digit = any(c.isdigit() for c in password)
                has_special = any(c in "!@#$%^&*" for c in password)
            
            with open(db_pwd_path, "w", encoding='utf-8') as f:
                f.write(password)
            
            # Permissions restrictives
            if hasattr(os, 'chmod'):
                os.chmod(db_pwd_path, 0o600)
            
            print_colored("✅ Mot de passe DB généré (32 chars, 4 types)", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"❌ Erreur génération mot de passe: {e}", Colors.RED)
            return False
    
    def generate_ssl_certificates(self) -> bool:
        """Génère les certificats SSL pour HTTPS"""
        print_colored("🔐 Génération certificats SSL...", Colors.BLUE)
        
        cert_path = self.secrets_dir / "nginx.crt"
        key_path = self.secrets_dir / "nginx.key"
        
        if cert_path.exists() and key_path.exists():
            print_colored("ℹ️  Certificats SSL existent déjà", Colors.BLUE)
            return True
        
        try:
            # Tentative avec OpenSSL
            cmd = [
                'openssl', 'req', '-x509', '-newkey', 'rsa:4096', 
                '-keyout', str(key_path), '-out', str(cert_path), 
                '-days', '365', '-nodes', '-subj',
                '/C=FR/ST=IDF/L=Paris/O=ESGI/OU=CyberSecurity/CN=localhost'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Permissions restrictives
            if hasattr(os, 'chmod'):
                os.chmod(cert_path, 0o644)
                os.chmod(key_path, 0o600)
            
            print_colored("✅ Certificats SSL générés (OpenSSL)", Colors.GREEN)
            return True
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_colored("⚠️  OpenSSL non disponible, certificats de développement", Colors.YELLOW)
            
            # Certificats factices pour développement
            try:
                cert_content = """-----BEGIN CERTIFICATE-----
# Certificat SSL auto-signé pour développement HoneyPot Pro Max
# Généré automatiquement - NE PAS UTILISER EN PRODUCTION
-----END CERTIFICATE-----"""
                
                key_content = """-----BEGIN PRIVATE KEY-----
# Clé privée SSL pour développement HoneyPot Pro Max  
# Généré automatiquement - NE PAS UTILISER EN PRODUCTION
-----END PRIVATE KEY-----"""
                
                with open(cert_path, 'w', encoding='utf-8') as f:
                    f.write(cert_content)
                with open(key_path, 'w', encoding='utf-8') as f:
                    f.write(key_content)
                
                print_colored("✅ Certificats factices créés", Colors.GREEN)
                return True
                
            except Exception as e:
                print_colored(f"❌ Erreur certificats factices: {e}", Colors.RED)
                return False
    
    def validate_secrets(self) -> bool:
        """Valide que tous les secrets sont présents"""
        print_colored("🔍 Validation des secrets...", Colors.BLUE)
        
        required_secrets = [
            self.secrets_dir / "mfa_encryption_key.txt",
            self.secrets_dir / "db_password.txt", 
            self.secrets_dir / "db_encryption_key.txt",
            self.secrets_dir / "nginx.crt",
            self.secrets_dir / "nginx.key"
        ]
        
        missing_secrets = []
        for secret_path in required_secrets:
            if not secret_path.exists():
                missing_secrets.append(str(secret_path))
        
        if missing_secrets:
            print_colored("❌ Secrets manquants:", Colors.RED)
            for secret in missing_secrets:
                print_colored(f"   - {secret}", Colors.RED)
            return False
        
        print_colored("✅ Tous les secrets sont présents", Colors.GREEN)
        return True
    
    def generate_all(self) -> bool:
        """Génère tous les secrets nécessaires"""
        print_colored("\n=== 🔒 GÉNÉRATION DES SECRETS ===", Colors.BOLD)
        
        success_steps = []
        
        # Étapes de génération
        success_steps.append(self.create_secure_directories())
        success_steps.append(self.generate_database_keys())
        success_steps.append(self.generate_mfa_key())
        success_steps.append(self.generate_database_password())
        success_steps.append(self.generate_ssl_certificates())
        
        # Validation finale
        validation_ok = self.validate_secrets()
        
        if all(success_steps) and validation_ok:
            print_colored("\n✅ Génération des secrets terminée avec succès", Colors.GREEN)
            return True
        else:
            print_colored("\n❌ Problèmes lors de la génération des secrets", Colors.RED)
            return False
