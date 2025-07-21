#!/usr/bin/env python3
"""
Setup Development Environment - HoneyPot Pro Max
======================================================

Script d'initialisation automatique pour le projet ESGI.
Cree les secrets, configure l'environnement et prepare le deploiement.

Usage:
    python setup_dev_environment.py

Auteur: Equipe ESGI 2024-2025
"""

import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet
import secrets
import string

def print_banner():
    """Affiche le banner du projet"""
    print("""
HoneyPot Pro Max - Setup Environment
============================================
Projet Annuel ESGI 2024-2025
Configuration automatique de l'environnement de developpement
    """)

def create_secrets_directory():
    """Cree le repertoire secrets avec les bonnes permissions"""
    secrets_dir = Path("secrets")
    if not secrets_dir.exists():
        secrets_dir.mkdir(mode=0o700)
        print("[OK] Repertoire 'secrets/' cree avec permissions securisees")
    else:
        print("[INFO] Repertoire 'secrets/' existe deja")

def generate_mfa_key():
    """Genere une cle de chiffrement MFA unique"""
    mfa_key_path = Path("secrets/mfa_encryption_key.txt")
    
    if not mfa_key_path.exists():
        # Generer une cle Fernet (AES-256)
        key = Fernet.generate_key()
        
        # Sauvegarder la cle
        with open(mfa_key_path, "wb") as f:
            f.write(key)
        
        # Permissions restrictives (lecture seule pour le proprietaire)
        mfa_key_path.chmod(0o600)
        
        print("[OK] Cle de chiffrement MFA generee (AES-256)")
        print(f"     Stockee dans: {mfa_key_path}")
    else:
        print("[INFO] Cle MFA existe deja")

def generate_db_password():
    """Genere un mot de passe securise pour PostgreSQL"""
    db_password_path = Path("secrets/db_password.txt")
    
    if not db_password_path.exists():
        # Generer un mot de passe securise (32 caracteres)
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for i in range(32))
        
        # Sauvegarder le mot de passe
        with open(db_password_path, "w") as f:
            f.write(password)
        
        # Permissions restrictives
        db_password_path.chmod(0o600)
        
        print("[OK] Mot de passe PostgreSQL genere")
        print(f"     Stocke dans: {db_password_path}")
    else:
        print("[INFO] Mot de passe DB existe deja")

def migrate_existing_certificates():
    """Migre les certificats existants vers secrets/"""
    old_cert = Path("nginx.crt")
    old_key = Path("nginx.key")
    new_cert = Path("secrets/nginx.crt")
    new_key = Path("secrets/nginx.key")
    
    moved_files = []
    
    if old_cert.exists() and not new_cert.exists():
        old_cert.rename(new_cert)
        new_cert.chmod(0o644)
        moved_files.append("nginx.crt")
    
    if old_key.exists() and not new_key.exists():
        old_key.rename(new_key)
        new_key.chmod(0o600)
        moved_files.append("nginx.key")
    
    if moved_files:
        print(f"[OK] Certificats migres vers secrets/: {', '.join(moved_files)}")
        return True
    
    return False

def generate_ssl_certificates():
    """Genere les certificats SSL auto-signes dans secrets/"""
    cert_path = Path("secrets/nginx.crt")
    key_path = Path("secrets/nginx.key")
    
    if not cert_path.exists() or not key_path.exists():
        try:
            import subprocess
            print("[INFO] Generation des certificats SSL...")
            
            # Commande OpenSSL pour generer certificat auto-signe
            cmd = [
                "openssl", "req", "-x509", "-newkey", "rsa:4096",
                "-keyout", str(key_path),
                "-out", str(cert_path),
                "-days", "365", "-nodes",
                "-subj", "/C=FR/ST=IDF/L=Paris/O=ESGI/OU=Security/CN=localhost"
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Permissions restrictives
            cert_path.chmod(0o644)
            key_path.chmod(0o600)
            
            print("[OK] Certificats SSL generes dans secrets/")
            print(f"     Certificat: {cert_path}")
            print(f"     Cle privee: {key_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Echec generation SSL: {e}")
            print("        Installez OpenSSL ou copiez manuellement les certificats")
            return False
        except FileNotFoundError:
            print("[WARNING] OpenSSL non trouve")
            print("          Copiez manuellement nginx.crt et nginx.key dans secrets/")
            return False
    else:
        print("[INFO] Certificats SSL existent deja dans secrets/")
    
    return True

def check_docker():
    """Verifie que Docker est disponible"""
    try:
        import subprocess
        result = subprocess.run(["docker", "--version"], 
                               capture_output=True, text=True, check=True)
        print(f"[OK] {result.stdout.strip()}")
        
        result = subprocess.run(["docker", "compose", "version"], 
                               capture_output=True, text=True, check=True)
        print(f"[OK] {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Docker ou Docker Compose non disponible")
        print("        Installez Docker Desktop avant de continuer")
        return False
    except FileNotFoundError:
        print("[ERROR] Docker non trouve dans le PATH")
        return False

def validate_environment():
    """Valide que l'environnement est pret"""
    print("\n=== VALIDATION DE L'ENVIRONNEMENT ===")
    
    checks = [
        ("Secrets", Path("secrets").exists()),
        ("Cle MFA", Path("secrets/mfa_encryption_key.txt").exists()),
        ("Mot de passe DB", Path("secrets/db_password.txt").exists()),
        ("Certificat SSL", Path("secrets/nginx.crt").exists()),
        ("Cle privee SSL", Path("secrets/nginx.key").exists()),
        ("Docker Compose", Path("docker-compose.yml").exists())
    ]
    
    all_good = True
    for check_name, check_result in checks:
        status = "[OK]" if check_result else "[MISSING]"
        print(f"{status} {check_name}")
        if not check_result:
            all_good = False
    
    if all_good:
        print("\n[SUCCESS] Environnement pret pour le deploiement !")
        print("          Commande suivante: docker compose up -d --build")
    else:
        print("\n[WARNING] Certains elements sont manquants")
        print("          Verifiez les erreurs ci-dessus")
    
    return all_good

def update_gitignore():
    """Met a jour .gitignore pour proteger les secrets"""
    gitignore_content = """
# Secrets et donnees sensibles
secrets/
*.key
*.crt
*.env
.env*

# Donnees Docker
docker-data/
postgres-data/

# Logs
*.log
logs/

# Fichiers temporaires
*.tmp
*.temp
__pycache__/
*.pyc
"""
    
    gitignore_path = Path(".gitignore")
    
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            existing_content = f.read()
        
        if "secrets/" not in existing_content:
            with open(gitignore_path, "a") as f:
                f.write(gitignore_content)
            print("[OK] .gitignore mis a jour pour proteger les secrets")
        else:
            print("[INFO] .gitignore deja configure")
    else:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content.strip())
        print("[OK] .gitignore cree pour proteger les secrets")

def print_next_steps():
    """Affiche les prochaines etapes"""
    print("""
=== PROCHAINES ETAPES ===
1. Lancez l'environnement: docker compose up -d --build
2. Attendez 2-3 minutes pour le demarrage complet
3. Verifiez l'installation: python scripts/validate_installation.py
4. Acces web:
   - HoneyPot HTTPS: https://localhost:9443
   - API Docs: http://localhost:8000/docs
   - Kibana: http://localhost:5601
   - pgAdmin: http://localhost:5050

Bon test de securite !
    """)

def main():
    """Fonction principale"""
    print_banner()
    
    print("\n=== CONFIGURATION DE L'ENVIRONNEMENT ===")
    
    # Etape 1: Creer le repertoire secrets
    create_secrets_directory()
    
    # Etape 2: Generer la cle MFA
    generate_mfa_key()
    
    # Etape 3: Generer le mot de passe DB
    generate_db_password()
    
    # Etape 4: Migrer et generer les certificats SSL
    migrate_existing_certificates()
    generate_ssl_certificates()
    
    # Etape 5: Verifier Docker
    docker_ok = check_docker()
    
    # Etape 6: Mettre a jour .gitignore
    update_gitignore()
    
    # Etape 7: Validation finale
    env_ready = validate_environment()
    
    if env_ready and docker_ok:
        print_next_steps()
        sys.exit(0)
    else:
        print("\n[ERROR] Configuration incomplete")
        sys.exit(1)

if __name__ == "__main__":
    main()
