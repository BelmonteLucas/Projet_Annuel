#!/usr/bin/env python3
"""
Fix Line Endings - HoneyPot Pro Max
===================================

Script pour rÃ©soudre les problÃ¨mes de fins de ligne (LF/CRLF) 
aprÃ¨s un pull Git avec des diffÃ©rences de plateforme.

Usage:
    python scripts/fix_line_endings.py

Auteur: Ã‰quipe ESGI 2024-2025
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Affiche le banner du script"""
    print("""
ðŸ”§ CORRECTION DES FINS DE LIGNE
===============================
ðŸ›¡ï¸  HoneyPot Pro Max
ðŸ“ RÃ©solution des conflits LF/CRLF
    """)

def check_git_status():
    """VÃ©rifie s'il y a des modifications Git non commitÃ©es"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        return result.stdout.strip()
    except Exception as e:
        print(f"âŒ Erreur lors de la vÃ©rification Git: {e}")
        return None

def fix_line_endings():
    """Corrige les fins de ligne selon .gitattributes"""
    print("\nðŸ”„ Application des rÃ¨gles .gitattributes...")
    
    try:
        # Ã‰tape 1: S'assurer que .gitattributes est bien prÃ©sent
        if not Path('.gitattributes').exists():
            print("âŒ Fichier .gitattributes manquant. Veuillez faire un pull du repository.")
            return False
        
        # Ã‰tape 2: Renormaliser les fichiers
        print("ðŸ“ Renormalisation des fichiers...")
        result = subprocess.run(['git', 'add', '--renormalize', '.'], 
                              cwd='.', capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"âŒ Erreur lors de la renormalisation: {result.stderr}")
            return False
        
        # Ã‰tape 3: VÃ©rifier les changements
        status_output = check_git_status()
        if status_output:
            print(f"\nðŸ“‹ Fichiers modifiÃ©s aprÃ¨s normalisation:")
            for line in status_output.split('\n'):
                if line.strip():
                    print(f"   ðŸ“„ {line}")
            
            print("\nðŸ’¡ Actions recommandÃ©es:")
            print("   1. VÃ©rifiez les changements: git diff --cached")
            print("   2. Commitez les corrections: git commit -m 'Fix line endings'")
            print("   3. Poussez les changements: git push origin main")
        else:
            print("âœ… Aucune correction de fins de ligne nÃ©cessaire.")
        
        return True
        
    except Exception as e:
        print(f"âŒ Erreur lors de la correction: {e}")
        return False

def setup_git_config():
    """Configure Git pour gÃ©rer automatiquement les fins de ligne"""
    print("\nâš™ï¸  Configuration Git pour les fins de ligne...")
    
    configs = [
        ('core.autocrlf', 'input'),    # Convertir CRLF -> LF Ã  l'input
        ('core.safecrlf', 'true'),     # Avertir des conversions dangereuses
    ]
    
    for config_key, config_value in configs:
        try:
            subprocess.run(['git', 'config', config_key, config_value], 
                          cwd='.', check=True)
            print(f"   âœ… {config_key} = {config_value}")
        except subprocess.CalledProcessError as e:
            print(f"   âš ï¸  Impossible de configurer {config_key}: {e}")

def main():
    """Fonction principale"""
    print_banner()
    
    # VÃ©rification du rÃ©pertoire Git
    if not Path('.git').exists():
        print("âŒ Ce script doit Ãªtre exÃ©cutÃ© dans la racine du projet Git.")
        sys.exit(1)
    
    # Configuration Git
    setup_git_config()
    
    # Correction des fins de ligne
    if fix_line_endings():
        print("\nâœ… Correction des fins de ligne terminÃ©e avec succÃ¨s!")
        print("\nðŸ“ Note: Si votre collÃ¨gue continue d'avoir des problÃ¨mes,")
        print("   demandez-lui d'exÃ©cuter ce script aprÃ¨s chaque pull.")
    else:
        print("\nâŒ Ã‰chec de la correction des fins de ligne.")
        sys.exit(1)

if __name__ == "__main__":
    main()
