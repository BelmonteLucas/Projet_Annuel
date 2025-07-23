#!/usr/bin/env python3
"""
Module de Configuration Projet - HoneyPot Pro Max
================================================

Responsabilité unique : Configuration et standardisation
- Encodage UTF-8 
- Configuration Git (.gitattributes, .editorconfig)
- Normalisation des fichiers existants

Usage:
    from setup.project_configurator import ProjectConfigurator
    configurator = ProjectConfigurator()
    configurator.configure_all()

Auteur: Équipe ESGI 2024-2025
"""

from pathlib import Path
from .colors import Colors, print_colored

class ProjectConfigurator:
    """Gestionnaire de configuration du projet"""
    
    def __init__(self):
        self.project_root = Path(".")
        
    def create_gitattributes(self) -> bool:
        """Crée le fichier .gitattributes pour l'encodage"""
        print_colored("📝 Configuration .gitattributes...", Colors.BLUE)
        
        gitattributes_content = """# Configuration encodage et fins de ligne - HoneyPot Pro Max
* text=auto eol=lf

# Code source - UTF-8 obligatoire
*.py text eol=lf encoding=utf-8
*.js text eol=lf encoding=utf-8
*.html text eol=lf encoding=utf-8
*.css text eol=lf encoding=utf-8
*.json text eol=lf encoding=utf-8
*.yml text eol=lf encoding=utf-8
*.yaml text eol=lf encoding=utf-8
*.md text eol=lf encoding=utf-8
*.txt text eol=lf encoding=utf-8
*.conf text eol=lf encoding=utf-8
*.sh text eol=lf encoding=utf-8

# Scripts Windows - UTF-8 avec BOM
*.ps1 text eol=crlf encoding=utf-8-bom
*.bat text eol=crlf encoding=utf-8
*.cmd text eol=crlf encoding=utf-8

# Docker et configuration
Dockerfile* text eol=lf encoding=utf-8
docker-compose*.yml text eol=lf encoding=utf-8
.gitignore text eol=lf encoding=utf-8
.gitattributes text eol=lf encoding=utf-8

# Fichiers binaires
*.crt binary
*.key binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
"""
        
        try:
            with open('.gitattributes', 'w', encoding='utf-8') as f:
                f.write(gitattributes_content)
            print_colored("✅ .gitattributes créé", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"❌ Erreur .gitattributes: {e}", Colors.RED)
            return False
    
    def create_editorconfig(self) -> bool:
        """Crée le fichier .editorconfig pour l'uniformité des éditeurs"""
        print_colored("⚙️  Configuration .editorconfig...", Colors.BLUE)
        
        editorconfig_content = """# Configuration universelle des éditeurs - HoneyPot Pro Max
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4
max_line_length = 88

[*.{js,html,css}]
indent_size = 2
max_line_length = 100

[*.md]
trim_trailing_whitespace = false
max_line_length = 80

[*.{yml,yaml}]
indent_size = 2

[*.ps1]
charset = utf-8-bom
end_of_line = crlf
indent_size = 4

[*.{bat,cmd}]
charset = utf-8
end_of_line = crlf
indent_size = 2
"""
        
        try:
            with open('.editorconfig', 'w', encoding='utf-8') as f:
                f.write(editorconfig_content)
            print_colored("✅ .editorconfig créé", Colors.GREEN)
            return True
        except Exception as e:
            print_colored(f"❌ Erreur .editorconfig: {e}", Colors.RED)
            return False
    
    def normalize_existing_files(self) -> bool:
        """Normalise l'encodage des fichiers existants"""
        print_colored("🔄 Normalisation fichiers existants...", Colors.BLUE)
        
        text_extensions = ['.md', '.txt', '.py', '.js', '.html', '.css', 
                          '.json', '.yml', '.yaml', '.conf', '.ps1']
        
        converted_count = 0
        error_count = 0
        
        for ext in text_extensions:
            for file_path in self.project_root.rglob(f'*{ext}'):
                # Ignorer les répertoires Git et backups
                if '.git' in str(file_path) or 'backup' in str(file_path):
                    continue
                
                try:
                    # Lire avec détection automatique
                    with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
                        content = f.read()
                    
                    # Réécrire en UTF-8 (avec ou sans BOM selon le type)
                    encoding = 'utf-8-sig' if ext == '.ps1' else 'utf-8'
                    with open(file_path, 'w', encoding=encoding, newline='\n') as f:
                        f.write(content)
                    
                    converted_count += 1
                    
                except Exception as e:
                    print_colored(f"⚠️  Erreur {file_path}: {str(e)[:50]}...", Colors.YELLOW)
                    error_count += 1
        
        if error_count == 0:
            print_colored(f"✅ {converted_count} fichiers normalisés", Colors.GREEN)
            return True
        else:
            print_colored(f"⚠️  {converted_count} fichiers OK, {error_count} erreurs", Colors.YELLOW)
            return True  # Continue malgré quelques erreurs
    
    def configure_all(self) -> bool:
        """Exécute toute la configuration du projet"""
        print_colored("\n=== 📝 CONFIGURATION PROJET ===", Colors.BOLD)
        
        steps_success = []
        
        steps_success.append(self.create_gitattributes())
        steps_success.append(self.create_editorconfig())
        steps_success.append(self.normalize_existing_files())
        
        if all(steps_success):
            print_colored("\n✅ Configuration projet terminée", Colors.GREEN)
            return True
        else:
            print_colored("\n⚠️  Configuration partiellement réussie", Colors.YELLOW)
            return True  # Pas critique
