#!/bin/sh
set -e

DB_PASSWORD_SECRET_FILE="/run/secrets/db_password"
# Le répertoire home de l'utilisateur pgadmin dans le conteneur est /var/lib/pgadmin
PGADMIN_HOME="/var/lib/pgadmin"
PGPASS_FILE_IN_CONTAINER="${PGADMIN_HOME}/.pgpass" 
# Notez le "." pour un fichier caché

# S'assurer que le répertoire cible existe (normalement, il devrait)
mkdir -p "$PGADMIN_HOME"

if [ -f "$DB_PASSWORD_SECRET_FILE" ]; then
    DB_PASSWORD=$(cat "$DB_PASSWORD_SECRET_FILE")
    PGPASS_LINE="db:5432:postgres:postgres:${DB_PASSWORD}"

    echo "$PGPASS_LINE" > "$PGPASS_FILE_IN_CONTAINER"
    # L'utilisateur pgadmin (UID 5050) doit être propriétaire et avoir les droits
    # chown 5050:5050 "$PGPASS_FILE_IN_CONTAINER" # Normalement, le script s'exécute en tant que root avant de passer à l'utilisateur pgadmin, ou pgAdmin gère cela.
    chmod 600 "$PGPASS_FILE_IN_CONTAINER" # Permissions strictes pour pgpass
    echo "Dynamic pgpass file generated at $PGPASS_FILE_IN_CONTAINER for pgAdmin."
else
    echo "Warning: DB password secret file ($DB_PASSWORD_SECRET_FILE) not found for pgAdmin."
    rm -f "$PGPASS_FILE_IN_CONTAINER"
fi

# Exécute le point d'entrée original de pgAdmin
# Ce script s'exécute en tant que root initialement, puis pgAdmin change d'utilisateur.
exec /entrypoint.sh