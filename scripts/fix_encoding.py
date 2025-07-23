#!/usr/bin/env python3
"""
Script pour corriger les problèmes d'encodage dans les fichiers HTML
Corrige les caractères français mal encodés (UTF-8 double encodage)
"""

import os
import re
from pathlib import Path

def fix_encoding_issues(file_path):
    """
    Corrige les problèmes d'encodage courants dans un fichier
    """
    # Dictionnaire des corrections d'encodage
    encoding_fixes = {
        'Ã©': 'é',  # é mal encodé
        'Ã¨': 'è',  # è mal encodé  
        'Ã ': 'à',  # à mal encodé
        'Ã¡': 'á',  # á mal encodé
        'Ã§': 'ç',  # ç mal encodé
        'Ã¹': 'ù',  # ù mal encodé
        'Ã«': 'ë',  # ë mal encodé
        'Ã¯': 'ï',  # ï mal encodé
        'Ã´': 'ô',  # ô mal encodé
        'Ã®': 'î',  # î mal encodé
        'Ã¢': 'â',  # â mal encodé
        'Ã»': 'û',  # û mal encodé
        'Ã€': 'À',  # À mal encodé
        'Ã‰': 'É',  # É mal encodé
        'Ã‡': 'Ç',  # Ç mal encodé
        'ÃŠ': 'Ê',  # Ê mal encodé
        'Ã‹': 'Ë',  # Ë mal encodé
        'Ãˆ': 'È',  # È mal encodé
        'Ã\u00d1': 'Ñ',  # Ñ mal encodé
        'Ã±': 'ñ',  # ñ mal encodé
        'déjÃ ': 'déjà ',  # déjà mal encodé
        'Ã  ': 'à ',  # à suivi d'espace
        'âœ…': '✅',  # émoji checkmark
        'âš ï¸': '⚠️',  # émoji warning  
        'ðŸ"„': '🔄',  # émoji refresh
        'ðŸ"': '🔐',  # émoji lock
        'ðŸ"±': '📱',  # émoji phone
    }
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Sauvegarder le contenu original
        original_content = content
        
        # Appliquer les corrections
        for wrong_char, correct_char in encoding_fixes.items():
            content = content.replace(wrong_char, correct_char)
        
        # Vérifier si des modifications ont été faites
        if content != original_content:
            # Écrire le fichier corrigé
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

def main():
    """
    Fonction principale - corrige l'encodage du frontend
    """
    print("🔧 Correction des problèmes d'encodage...")
    
    # Chemin vers le fichier frontend
    project_root = Path(__file__).parent.parent
    frontend_file = project_root / "frontend" / "index.html"
    
    if not frontend_file.exists():
        print(f"❌ Fichier frontend non trouvé: {frontend_file}")
        return False
    
    print(f"📝 Correction du fichier: {frontend_file}")
    
    # Corriger le fichier
    if fix_encoding_issues(frontend_file):
        print("✅ Problèmes d'encodage corrigés avec succès!")
        return True
    else:
        print("ℹ️  Aucune correction nécessaire")
        return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
