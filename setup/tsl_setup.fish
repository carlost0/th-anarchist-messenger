#!/usr/bin/env fish

# Get primary IPv4
set ip (ip -4 addr show scope global | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n 1)
if test -z "$ip"
    echo "Could not determine IP address!"
    exit 1
end

echo "Using IP: $ip"

set config_file "../config/san.cnf"

# Write san.cnf line by line (minimal)
echo "[req]" > $config_file
echo "distinguished_name = req_distinguished_name" >> $config_file
echo "req_extensions = v3_req" >> $config_file
echo "prompt = no" >> $config_file
echo "" >> $config_file

echo "[req_distinguished_name]" >> $config_file
echo "C = US" >> $config_file
echo "ST = State" >> $config_file
echo "L = City" >> $config_file
echo "O = Org" >> $config_file
echo "CN = $ip" >> $config_file
echo "" >> $config_file

echo "[v3_req]" >> $config_file
echo "subjectAltName = @alt_names" >> $config_file
echo "" >> $config_file

echo "[alt_names]" >> $config_file
echo "IP.1 = $ip" >> $config_file

echo "Generated san.cnf at $config_file"

# Generate certificate + key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "../config/key.pem" -out "../config/cert.pem" -config $config_file

echo "Created cert.pem and key.pem (valid for 365 days) in ../config"

