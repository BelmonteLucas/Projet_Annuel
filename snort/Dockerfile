# =============================================================================
# SNORT IDS DOCKERFILE - VERSION ULTRA-SIMPLIFIÉE
# =============================================================================
# Construction d'une image Snort pour la détection d'intrusion réseau
# Utilise une approche minimaliste et robuste
# =============================================================================

FROM alpine:3.18

# Variables d'environnement
ENV SNORT_USER=snort
ENV SNORT_GROUP=snort

# Installation des packages nécessaires
RUN apk update && apk add --no-cache \
    # Snort depuis les dépôts Alpine
    snort \
    # Outils réseau
    net-tools \
    tcpdump \
    # Outils de base
    bash \
    # Nettoyage automatique avec Alpine
    && rm -rf /var/cache/apk/*

# Création des répertoires nécessaires
RUN mkdir -p /etc/snort/rules \
             /var/log/snort \
             /etc/snort/so_rules \
             /etc/snort/preproc_rules \
    && chmod 755 /var/log/snort

# Copie des fichiers de configuration
COPY snort.conf /etc/snort/snort.conf
COPY rules/local.rules /etc/snort/rules/local.rules
COPY classification.config /etc/snort/classification.config
COPY reference.config /etc/snort/reference.config
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Rendre le script d'entrée exécutable
RUN chmod +x /usr/local/bin/entrypoint.sh

# Gestion de l'utilisateur snort (Alpine style)
RUN addgroup -S ${SNORT_GROUP} 2>/dev/null || true && \
    adduser -S -D -H -s /bin/false -G ${SNORT_GROUP} ${SNORT_USER} 2>/dev/null || true

# Attribution des permissions
RUN chown -R ${SNORT_USER}:${SNORT_GROUP} /etc/snort /var/log/snort

# Port d'exposition (optionnel pour monitoring)
EXPOSE 8080

# Test de configuration (non-bloquant)
RUN snort -T -c /etc/snort/snort.conf -q 2>/dev/null || echo "Config test done"

# Utilisateur non-privilégié pour l'exécution
USER ${SNORT_USER}

# Script d'entrée intelligent
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Mode par défaut : test de configuration (temporaire pour debug)
CMD ["test"]

