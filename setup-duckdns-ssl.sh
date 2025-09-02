#!/bin/bash

# DuckDNS SSL Setup Script
# Usage: ./setup-duckdns-ssl.sh yourdomain.duckdns.org your_duckdns_token

DOMAIN=$1
TOKEN=$2

if [ -z "$DOMAIN" ] || [ -z "$TOKEN" ]; then
    echo "Usage: $0 yourdomain.duckdns.org your_duckdns_token"
    exit 1
fi

echo "Setting up SSL for DuckDNS domain: $DOMAIN"

# Update IP address in DuckDNS
echo "Updating DuckDNS IP..."
curl "https://www.duckdns.org/update?domains=${DOMAIN%%.duckdns.org}&token=$TOKEN&ip="

# Create DNS challenge hook for certbot
mkdir -p /home/ubuntu/certbot-hooks

cat > /home/ubuntu/certbot-hooks/auth-hook.sh << EOF
#!/bin/bash
# This hook is called before the challenge is given to certbot
echo "Setting DNS TXT record for \$CERTBOT_DOMAIN"
curl "https://www.duckdns.org/update?domains=\${CERTBOT_DOMAIN%%.duckdns.org}&token=$TOKEN&txt=\$CERTBOT_VALIDATION"
sleep 30
EOF

cat > /home/ubuntu/certbot-hooks/cleanup-hook.sh << EOF
#!/bin/bash
# This hook is called after the challenge is processed by certbot
echo "Clearing DNS TXT record for \$CERTBOT_DOMAIN"
curl "https://www.duckdns.org/update?domains=\${CERTBOT_DOMAIN%%.duckdns.org}&token=$TOKEN&txt=removed&clear=true"
EOF

chmod +x /home/ubuntu/certbot-hooks/*.sh

# Request SSL certificate using DNS challenge
sudo certbot certonly \
    --manual \
    --preferred-challenges dns \
    --manual-auth-hook /home/ubuntu/certbot-hooks/auth-hook.sh \
    --manual-cleanup-hook /home/ubuntu/certbot-hooks/cleanup-hook.sh \
    -d $DOMAIN \
    --agree-tos \
    --manual-public-ip-logging-ok

echo "SSL certificate setup complete!"
echo "Certificate files will be at: /etc/letsencrypt/live/$DOMAIN/"
