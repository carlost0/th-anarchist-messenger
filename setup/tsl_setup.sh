#!/usr/bin/env bash

# Get primary non-loopback IPv4 address
IP=$(ip -4 addr show scope global | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)

if [ -z "$IP" ]; then
    echo "Could not determine IP address!"
    exit 1
fi

echo "Using IP: $IP"

# Write san.cnf
cat > san.cnf <<EOF
[req]
distinguished_name=req
req_extensions = v3_req
prompt = no

[dn]
CN = $IP

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = $IP
EOF

echo "Generated san.cnf"

# Generate certificate + key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem -out cert.pem -config san.cnf

echo "Created cert.pem and key.pem (valid for 365 days)"

