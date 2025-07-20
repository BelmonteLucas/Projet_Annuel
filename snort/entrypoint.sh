#!/bin/sh
# =============================================================================
# SNORT ENTRYPOINT SCRIPT (Alpine Linux compatible)
# =============================================================================
# Script d'entrée pour le conteneur Snort
# Gère différents modes de fonctionnement
# =============================================================================

set -e

# Configuration par défaut
SNORT_CONFIG="/etc/snort/snort.conf"
LOG_DIR="/var/log/snort"
ALERT_MODE="fast"

# Fonction d'aide
show_help() {
    echo "Snort IDS Container - Options disponibles:"
    echo "  test     - Teste la configuration Snort"
    echo "  daemon   - Lance Snort en mode démon sur toutes les interfaces"
    echo "  monitor  - Lance Snort en mode monitoring (par défaut)"
    echo "  help     - Affiche cette aide"
    echo ""
    echo "Variables d'environnement:"
    echo "  INTERFACE - Interface réseau à monitorer (défaut: any)"
    echo "  ALERT_MODE - Mode d'alerte: fast, full, none (défaut: fast)"
    echo ""
    echo "Exemples:"
    echo "  docker run snort-ids test"
    echo "  docker run -e INTERFACE=eth0 snort-ids daemon"
}

# Test de la configuration
test_config() {
    echo "=== Test de la configuration Snort ==="
    snort -T -c "$SNORT_CONFIG"
    echo "=== Configuration OK ==="
}

# Mode démon (production)
run_daemon() {
    local interface=${INTERFACE:-any}
    echo "=== Démarrage Snort en mode démon ==="
    echo "Interface: $interface"
    echo "Mode d'alerte: $ALERT_MODE"
    echo "Logs: $LOG_DIR"
    
    # Vérifier que l'interface existe (sauf pour 'any') - Alpine version
    if [ "$interface" != "any" ] && ! ip link show "$interface" >/dev/null 2>&1; then
        echo "ATTENTION: Interface $interface non trouvée, utilisation de 'any'"
        interface="any"
    fi
    
    exec snort -c "$SNORT_CONFIG" -i "$interface" -A "$ALERT_MODE" -l "$LOG_DIR" -D
}

# Mode monitoring (test/développement)
run_monitor() {
    local interface=${INTERFACE:-any}
    echo "=== Démarrage Snort en mode monitoring ==="
    echo "Interface: $interface"
    echo "Mode d'alerte: $ALERT_MODE"
    echo "Logs: $LOG_DIR"
    
    # En mode monitoring, on n'utilise pas le mode démon
    exec snort -c "$SNORT_CONFIG" -i "$interface" -A "$ALERT_MODE" -l "$LOG_DIR" -v
}

# Mode principal
case "${1:-monitor}" in
    test)
        test_config
        ;;
    daemon)
        run_daemon
        ;;
    monitor)
        run_monitor
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        # Si c'est une option Snort directe, la passer
        if echo "$1" | grep -q "^-"; then
            exec snort "$@"
        else
            echo "Mode non reconnu: $1"
            show_help
            exit 1
        fi
        ;;
esac
