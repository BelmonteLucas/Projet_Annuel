#!/usr/bin/env python3
"""
Script pour corriger tous les problèmes d'encodage dans le fichier HTML
"""

import re

def fix_all_encoding_issues():
    file_path = r"c:\Users\Admin\OneDrive\Bureau\ESGI\Projet Annnuel\Projet_Annuel\frontend\index.html"
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corrections d'encodage
    replacements = [
        # Caractères de base mal encodés
        ('Ã©', 'é'),
        ('Ã¨', 'è'),
        ('Ã ', 'à'),
        ('Ã¡', 'á'),
        ('Ã§', 'ç'),
        ('Ã¹', 'ù'),
        ('Ã«', 'ë'),
        ('Ã¯', 'ï'),
        ('Ã´', 'ô'),
        ('Ã®', 'î'),
        ('Ã¢', 'â'),
        ('Ã»', 'û'),
        ('Ã€', 'À'),
        ('Ã‰', 'É'),
        ('Ã‡', 'Ç'),
        ('ÃŠ', 'Ê'),
        ('Ã‹', 'Ë'),
        ('Ãˆ', 'È'),
        ('Ã±', 'ñ'),
        
        # Caractères spéciaux avec espaces insécables
        ('DéjÃ\xa0', 'Déjà '),
        ('déjÃ\xa0', 'déjà '),
        ('Ã\xa0', 'à '),
        
        # Émojis mal encodés - utilisation directe
        ('ðŸ"„', '🔄'),
        ('ðŸ"', '🔐'),  
        ('ðŸ"±', '📱'),
        ('ðŸšª', '🚪'),
        ('ðŸ†•', '🆕'),
        ('âœ…', '✅'),
        ('âš\xa0ï¸', '⚠️'),
        ('âš ï¸', '⚠️'),
        
        # Patterns spécifiques trouvés
        ('Authentification Ã\xa0 deux facteurs', 'Authentification à deux facteurs'),
        ('l\'authentification Ã\xa0 deux facteurs', 'l\'authentification à deux facteurs'),
        ('code Ã\xa0 6 chiffres', 'code à 6 chiffres'),
        ('requis Ã\xa0 chaque', 'requis à chaque'),
        ('mise Ã\xa0 jour', 'mise à jour'),
        ('Ã\xa0 partir', 'à partir'),
        ('déjÃ\xa0 enregistrés', 'déjà enregistrés'),
        ('déjÃ\xa0 activé', 'déjà activé'),
        ('déjÃ\xa0 activée', 'déjà activée'),
        ('déjÃ\xa0 fait', 'déjà fait'),
    ]
    
    # Appliquer les corrections de base
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Correction spéciale pour l'émoji clé avec caractère problématique
    content = content.replace('\uf511', '🔑')
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Toutes les corrections d'encodage appliquées !")

if __name__ == "__main__":
    fix_all_encoding_issues()
