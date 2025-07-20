FROM snort/snort3:latest

WORKDIR /etc/snort

COPY snort.conf .
COPY rules/local.rules ./rules/

# Expose Snort's default port (optional, for external access if needed)
EXPOSE 8080

CMD ["snort", "-c", "/etc/snort/snort.conf", "-i", "eth0", "-A", "alert_json", "-l", "/var/log/snort"]

