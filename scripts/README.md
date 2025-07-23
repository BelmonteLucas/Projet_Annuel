# Scripts de Maintenance - HoneyPot Pro Max

Ce répertoire contient les scripts de maintenance et d'utilitaires pour le projet.

## 📋 Scripts Disponibles

| 🛠️ Script | 🎯 Utilité | 📝 Usage |
|-----------|------------|----------|
| **`check_port_conflicts.py`** | Détection conflits ports | `python scripts/check_port_conflicts.py` |
| **`security_tests.py`** | Tests de sécurité automatisés | `python scripts/security_tests.py --scenario all` |
| **`validate_installation.py`** | Validation installation complète | `python scripts/validate_installation.py` |
| **`test_fresh_install.py`** | Test installation fraîche | `python scripts/test_fresh_install.py` |
| **`fix_line_endings.py`** | Correction encodage UTF-8 | `python scripts/fix_line_endings.py` |

## 🎯 Scripts de Production vs Démonstration

- **Production** : `check_port_conflicts.py`, `validate_installation.py`, `security_tests.py`
- **Maintenance** : `fix_line_endings.py`, `test_fresh_install.py`

> **Note** : Les scripts de démonstration ont été intégrés dans le script principal

## 📊 Utilisation Recommandée

```bash
# Avant installation
python scripts/check_port_conflicts.py

# Après installation  
python scripts/validate_installation.py

# Tests de sécurité
python scripts/security_tests.py --scenario all

# Maintenance encodage
python scripts/fix_line_endings.py
```
