#!/bin/bash
set -e

echo "========================================="
echo "  PD ML 2026 - Server Setup Script"
echo "========================================="

# ---- 1. Install Docker ----
echo ""
echo "[1/8] Installing Docker..."
curl -fsSL https://get.docker.com | sh

# ---- 2. Clone repo ----
echo ""
echo "[2/8] Cloning repository..."
cd /root
git clone https://github.com/chusakt/pd_ml_2026.git
cd pd_ml_2026

# ---- 3. Create .env ----
echo ""
echo "[3/8] Creating .env from template..."
cp .env.example .env
echo ""
echo "  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo "  >>> YOU MUST EDIT .env NOW with your secrets     <<<"
echo "  >>> nano /root/pd_ml_2026/.env                   <<<"
echo "  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
echo ""
echo "  Fill in: SECRET_KEY, API_KEY (required)"
echo ""
read -p "  Press ENTER after you have edited .env (or Ctrl+C to stop)..."

# ---- 4. Build and start Docker ----
echo ""
echo "[4/8] Building and starting Docker containers..."
docker compose up --build -d

echo ""
echo "[5/8] Waiting for app to start..."
sleep 10

echo "  Testing app..."
curl -s http://localhost:8080/health && echo " <-- App is running!" || echo " <-- App not ready yet, check: docker compose logs -f"

# ---- 6. Install Nginx + Certbot ----
echo ""
echo "[6/8] Installing Nginx and Certbot..."
apt update -y
apt install -y nginx certbot python3-certbot-nginx

# ---- 7. Configure Nginx ----
echo ""
echo "[7/8] Configuring Nginx..."
cat > /etc/nginx/sites-available/api << 'NGINXCONF'
server {
    listen 80;
    server_name pdml26.thanavarp.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
NGINXCONF

ln -sf /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

# ---- 8. SSL Certificate ----
echo ""
echo "[8/8] Getting SSL certificate..."
certbot --nginx -d pdml26.thanavarp.com --non-interactive --agree-tos --email chusakt@gmail.com

# ---- 9. Firewall ----
echo ""
echo "Setting up firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw deny 8080
ufw --force enable

echo ""
echo "========================================="
echo "  SETUP COMPLETE!"
echo "========================================="
echo ""
echo "  API URL:  https://pdml26.thanavarp.com"
echo "  Health:   https://pdml26.thanavarp.com/health"
echo ""
echo "  .env location:    /root/pd_ml_2026/.env"
echo "  Nginx config:     /etc/nginx/sites-available/api"
echo "  Docker logs:      cd /root/pd_ml_2026 && docker compose logs -f"
echo "  Restart app:      cd /root/pd_ml_2026 && docker compose restart"
echo "  Rebuild app:      cd /root/pd_ml_2026 && docker compose up --build -d"
echo ""
