#!/usr/bin/env python3
"""
Module Utilitaires Communs - HoneyPot Pro Max
============================================

Responsabilité unique : Fonctions utilitaires partagées
- Gestion des couleurs console
- Fonctions d'affichage
- Constantes communes

Usage:
    from setup.colors import Colors, print_colored
    print_colored("Message", Colors.GREEN)

Auteur: Jakub WERLINSKI
"""

class Colors:
    """Codes couleur ANSI pour l'affichage console"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.END):
    """Affiche un message avec couleur ANSI"""
    print(f"{color}{message}{Colors.END}")

def print_banner():
    """Affiche le banner principal du projet"""
    print_colored(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                HoneyPot Pro Max - Setup Environment          ║
║                      Projet Annuel - Jakub WERLINSKI        ║
║                                                               ║
║  🔧 Configuration automatique complète de l'environnement    ║
║  🐳 Docker + 📝 Encodage + 🔒 Sécurité + ✅ Validation      ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
""")

def print_section_header(title: str):
    """Affiche un en-tête de section formaté"""
    print_colored(f"\n=== {title} ===", Colors.BOLD)
