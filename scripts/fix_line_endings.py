#!/usr/bin/env python3
"""
Fix Line Endings - HoneyPot Pro Max
===================================

Script pour résoudre les problèmes de fins de ligne (LF/CRLF) 
après un pull Git avec des différences de plateforme.

Usage:
    python scripts/fix_line_endings.py

Auteur: Équipe ESGI 2024-2025
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    """Affiche le banner du script"""
    print("""
🔧 CORRECTION DES FINS DE LIGNE
===============================
🛡️  HoneyPot Pro Max
📝 Résolution des conflits LF/CRLF
    """)

def check_git_status():
    """Vérifie s'il y a des modifications Git non commitées"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='.')
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Erreur lors de la vérification Git: {e}")
        return None

def fix_line_endings():
    """Corrige les fins de ligne selon .gitattributes"""
    print("\n🔄 Application des règles .gitattributes...")
    
    try:
        # Étape 1: S'assurer que .gitattributes est bien présent
        if not Path('.gitattributes').exists():
            print("❌ Fichier .gitattributes manquant. Veuillez faire un pull du repository.")
            return False
        
        # Étape 2: Renormaliser les fichiers
        print("📝 Renormalisation des fichiers...")
        result = subprocess.run(['git', 'add', '--renormalize', '.'], 
                              cwd='.', capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Erreur lors de la renormalisation: {result.stderr}")
            return False
        
        # Étape 3: Vérifier les changements
        status_output = check_git_status()
        if status_output:
            print(f"\n📋 Fichiers modifiés après normalisation:")
            for line in status_output.split('\n'):
                if line.strip():
                    print(f"   📄 {line}")
            
            print("\n💡 Actions recommandées:")
            print("   1. Vérifiez les changements: git diff --cached")
            print("   2. Commitez les corrections: git commit -m 'Fix line endings'")
            print("   3. Poussez les changements: git push origin main")
        else:
            print("✅ Aucune correction de fins de ligne nécessaire.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False

def setup_git_config():
    """Configure Git pour gérer automatiquement les fins de ligne"""
    print("\n⚙️  Configuration Git pour les fins de ligne...")
    
    configs = [
        ('core.autocrlf', 'input'),    # Convertir CRLF -> LF à l'input
        ('core.safecrlf', 'true'),     # Avertir des conversions dangereuses
    ]
    
    for config_key, config_value in configs:
        try:
            subprocess.run(['git', 'config', config_key, config_value], 
                          cwd='.', check=True)
            print(f"   ✅ {config_key} = {config_value}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Impossible de configurer {config_key}: {e}")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérification du répertoire Git
    if not Path('.git').exists():
        print("❌ Ce script doit être exécuté dans la racine du projet Git.")
        sys.exit(1)
    
    # Configuration Git
    setup_git_config()
    
    # Correction des fins de ligne
    if fix_line_endings():
        print("\n✅ Correction des fins de ligne terminée avec succès!")
        print("\n📝 Note: Si votre collègue continue d'avoir des problèmes,")
        print("   demandez-lui d'exécuter ce script après chaque pull.")
    else:
        print("\n❌ Échec de la correction des fins de ligne.")
        sys.exit(1)

if __name__ == "__main__":
    main()
