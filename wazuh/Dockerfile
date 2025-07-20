FROM wazuh/wazuh-manager:4.7.2

COPY config/ossec.conf /var/ossec/etc/ossec.conf

# Expose necessary ports for Wazuh agent communication
EXPOSE 1514/tcp 55000/tcp

CMD ["/var/ossec/bin/wazuh-manager", "-f"]

