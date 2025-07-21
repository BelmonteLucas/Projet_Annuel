#!/usr/bin/env python3
"""
Audit des Fichiers - HoneyPot Security Suite
============================================

Script d'audit pour identifier les fichiers inutilisés, redondants 
ou obsolètes dans le projet.

Usage:
    python scripts/audit_files.py

Auteur: Équipe ESGI 2024-2025
"""

import os
import sys
from pathlib import Path
import json
import re
from typing import Dict, List, Set

class ProjectAuditor:
    def __init__(self):
        self.project_root = Path(".")
        self.audit_results = {
            "timestamp": "",
            "summary": {},
            "unused_files": [],
            "redundant_files": [],
            "obsolete_files": [],
            "recommendations": []
        }
        
        # Fichiers à ignorer dans l'audit
        self.ignore_patterns = {
            ".git",
            "__pycache__",
            "*.pyc",
            "*.log",
            "node_modules",
            ".env",
            "*.tmp"
        }
        
        # Extensions de fichiers de code/config
        self.code_extensions = {".py", ".js", ".html", ".css", ".yml", ".yaml", ".conf", ".txt", ".md", ".sh"}
        
    def print_banner(self):
        """Affiche le banner d'audit"""
        print("""
🔍 AUDIT DES FICHIERS DU PROJET
===============================
🛡️  HoneyPot Security Suite
📋 Analyse des fichiers inutilisés et redondants
        """)

    def get_all_project_files(self) -> List[Path]:
        """Récupère tous les fichiers du projet"""
        all_files = []
        
        for root, dirs, files in os.walk(self.project_root):
            # Ignorer certains dossiers
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.ignore_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                if not any(pattern in str(file_path) for pattern in self.ignore_patterns):
                    all_files.append(file_path.relative_to(self.project_root))
        
        return all_files

    def analyze_docker_references(self) -> Set[str]:
        """Analyse les références dans docker-compose.yml"""
        referenced_files = set()
        
        docker_compose = Path("docker-compose.yml")
        if docker_compose.exists():
            with open(docker_compose, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Chercher les build contexts
                build_matches = re.findall(r'build:\s*\.?/?([^\s\n]+)', content)
                for match in build_matches:
                    referenced_files.add(match.strip("./"))
                
                # Chercher les volumes mappés
                volume_matches = re.findall(r'-\s*\.?/?([^:]+):', content)
                for match in volume_matches:
                    if not match.startswith("./"):
                        referenced_files.add(match.strip("./"))
                
                # Chercher les fichiers de configuration
                config_matches = re.findall(r'\.?/?([^:\s\n]+\.(conf|yml|yaml|crt|key|txt))', content)
                for match, ext in config_matches:
                    referenced_files.add(match.strip("./"))
        
        return referenced_files

    def analyze_script_references(self) -> Set[str]:
        """Analyse les références dans les scripts Python"""
        referenced_files = set()
        
        # Analyser tous les scripts Python
        for py_file in self.project_root.rglob("*.py"):
            if ".git" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Chercher les imports de fichiers locaux
                    import_matches = re.findall(r'from\s+([^\s]+)\s+import|import\s+([^\s\n,]+)', content)
                    for match in import_matches:
                        module = match[0] or match[1]
                        if "." in module and not module.startswith("from"):
                            referenced_files.add(f"{module.replace('.', '/')}.py")
                    
                    # Chercher les références à des fichiers
                    file_matches = re.findall(r'["\']([^"\']*\.(py|txt|conf|yml|yaml|html|css|js|crt|key))["\']', content)
                    for match, ext in file_matches:
                        if not match.startswith("http") and not match.startswith("/"):
                            referenced_files.add(match.strip("./"))
                            
            except Exception as e:
                print(f"Erreur lecture {py_file}: {e}")
        
        return referenced_files

    def analyze_html_references(self) -> Set[str]:
        """Analyse les références dans les fichiers HTML/CSS/JS"""
        referenced_files = set()
        
        # Analyser les fichiers web
        web_files = list(self.project_root.rglob("*.html")) + \
                   list(self.project_root.rglob("*.css")) + \
                   list(self.project_root.rglob("*.js"))
        
        for web_file in web_files:
            if ".git" in str(web_file):
                continue
                
            try:
                with open(web_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Chercher les références dans HTML/CSS/JS
                    patterns = [
                        r'src=["\']([^"\']+)["\']',
                        r'href=["\']([^"\']+)["\']',
                        r'url\(["\']?([^"\']+)["\']?\)',
                        r'@import\s+["\']([^"\']+)["\']'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if not match.startswith("http") and not match.startswith("#"):
                                referenced_files.add(match.strip("./"))
                                
            except Exception as e:
                print(f"Erreur lecture {web_file}: {e}")
        
        return referenced_files

    def identify_unused_files(self) -> List[Dict]:
        """Identifie les fichiers potentiellement inutilisés"""
        print("\n🔍 Analyse des fichiers inutilisés...")
        
        all_files = self.get_all_project_files()
        docker_refs = self.analyze_docker_references()
        script_refs = self.analyze_script_references()
        html_refs = self.analyze_html_references()
        
        # Combiner toutes les références
        all_refs = docker_refs | script_refs | html_refs
        
        # Fichiers essentiels (ne jamais marquer comme inutilisés)
        essential_files = {
            "README.md",
            "docker-compose.yml",
            ".gitignore",
            "nginx.conf",
            "nginx.crt",
            "nginx.key",
            "setup_dev_environment.py"
        }
        
        unused_files = []
        
        for file_path in all_files:
            file_str = str(file_path)
            
            # Ignorer les fichiers essentiels
            if file_str in essential_files:
                continue
            
            # Ignorer les rapports générés automatiquement
            if any(pattern in file_str for pattern in ["_report.json", "_test_", "validation_report"]):
                continue
                
            # Vérifier si le fichier est référencé
            is_referenced = any(ref in file_str or file_str in ref for ref in all_refs)
            
            if not is_referenced:
                unused_files.append({
                    "file": file_str,
                    "size": file_path.stat().st_size if file_path.exists() else 0,
                    "reason": "Aucune référence trouvée"
                })
                print(f"   ⚠️  {file_str}: potentiellement inutilisé")
        
        return unused_files

    def identify_redundant_files(self) -> List[Dict]:
        """Identifie les fichiers redondants"""
        print("\n🔄 Analyse des fichiers redondants...")
        
        redundant_files = []
        
        # Vérifier les doublons évidents
        all_files = self.get_all_project_files()
        
        # Grouper par nom de base
        file_groups = {}
        for file_path in all_files:
            base_name = file_path.stem
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(file_path)
        
        # Identifier les groupes avec plusieurs versions
        for base_name, files in file_groups.items():
            if len(files) > 1 and any("old" in str(f) or "backup" in str(f) or "copy" in str(f) for f in files):
                for file_path in files:
                    if any(pattern in str(file_path).lower() for pattern in ["old", "backup", "copy", "_2", "temp"]):
                        redundant_files.append({
                            "file": str(file_path),
                            "size": file_path.stat().st_size if file_path.exists() else 0,
                            "reason": f"Version alternative de {base_name}"
                        })
                        print(f"   ♻️  {file_path}: version redondante")
        
        return redundant_files

    def identify_obsolete_files(self) -> List[Dict]:
        """Identifie les fichiers obsolètes"""
        print("\n📅 Analyse des fichiers obsolètes...")
        
        obsolete_files = []
        
        # Patterns de fichiers potentiellement obsolètes
        obsolete_patterns = [
            "test_",
            "_test",
            "example",
            "sample",
            "demo",
            ".bak",
            ".old"
        ]
        
        all_files = self.get_all_project_files()
        
        for file_path in all_files:
            file_str = str(file_path).lower()
            
            for pattern in obsolete_patterns:
                if pattern in file_str:
                    obsolete_files.append({
                        "file": str(file_path),
                        "size": file_path.stat().st_size if file_path.exists() else 0,
                        "reason": f"Contient le pattern '{pattern}'"
                    })
                    print(f"   📅 {file_path}: potentiellement obsolète")
                    break
        
        return obsolete_files

    def generate_recommendations(self) -> List[str]:
        """Génère des recommandations de nettoyage"""
        recommendations = []
        
        total_unused = len(self.audit_results["unused_files"])
        total_redundant = len(self.audit_results["redundant_files"])
        total_obsolete = len(self.audit_results["obsolete_files"])
        
        if total_unused > 0:
            recommendations.append(f"🗑️  Supprimer {total_unused} fichier(s) inutilisé(s)")
        
        if total_redundant > 0:
            recommendations.append(f"♻️  Nettoyer {total_redundant} fichier(s) redondant(s)")
        
        if total_obsolete > 0:
            recommendations.append(f"📅 Archiver/supprimer {total_obsolete} fichier(s) obsolète(s)")
        
        # Calcul de l'espace récupérable
        total_size = 0
        for file_list in [self.audit_results["unused_files"], 
                         self.audit_results["redundant_files"], 
                         self.audit_results["obsolete_files"]]:
            total_size += sum(f["size"] for f in file_list)
        
        if total_size > 1024:
            size_mb = total_size / 1024 / 1024
            recommendations.append(f"💾 Espace récupérable: {size_mb:.2f} MB")
        
        return recommendations

    def run_audit(self) -> Dict:
        """Exécute l'audit complet"""
        self.print_banner()
        
        # Exécuter les analyses
        self.audit_results["unused_files"] = self.identify_unused_files()
        self.audit_results["redundant_files"] = self.identify_redundant_files()
        self.audit_results["obsolete_files"] = self.identify_obsolete_files()
        self.audit_results["recommendations"] = self.generate_recommendations()
        
        # Résumé
        self.audit_results["summary"] = {
            "total_unused": len(self.audit_results["unused_files"]),
            "total_redundant": len(self.audit_results["redundant_files"]),
            "total_obsolete": len(self.audit_results["obsolete_files"]),
            "total_issues": len(self.audit_results["unused_files"]) + 
                           len(self.audit_results["redundant_files"]) + 
                           len(self.audit_results["obsolete_files"])
        }
        
        self.print_summary()
        return self.audit_results

    def print_summary(self):
        """Affiche le résumé de l'audit"""
        summary = self.audit_results["summary"]
        
        print(f"""
📋 RÉSUMÉ DE L'AUDIT
====================
🗑️  Fichiers inutilisés: {summary['total_unused']}
♻️  Fichiers redondants: {summary['total_redundant']}
📅 Fichiers obsolètes: {summary['total_obsolete']}
🔢 Total problèmes: {summary['total_issues']}

💡 RECOMMANDATIONS:
""")
        
        for rec in self.audit_results["recommendations"]:
            print(f"   {rec}")
        
        if summary['total_issues'] == 0:
            print("\n✅ Projet propre ! Aucun fichier inutilisé détecté.")
        else:
            print(f"\n⚠️  {summary['total_issues']} fichier(s) à examiner.")
        
        print("\n📁 Rapport détaillé: file_audit_report.json")
        
        # Sauvegarder le rapport
        with open("file_audit_report.json", "w", encoding="utf-8") as f:
            json.dump(self.audit_results, f, indent=2, default=str)

def main():
    """Fonction principale"""
    auditor = ProjectAuditor()
    results = auditor.run_audit()
    
    # Code de sortie basé sur les résultats
    if results["summary"]["total_issues"] == 0:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
