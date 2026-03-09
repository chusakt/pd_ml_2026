# DigitalOcean Deployment Guide

## 1. Create a Droplet
- Choose **Ubuntu 24.04**
- Size: **8 vCPU / 16GB RAM** (~$96/mo)
- Region: closest to your users (Singapore if Thailand)
- Add your SSH key

## 2. SSH in and setup

```bash
# Connect
ssh root@your-droplet-ip

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone your repo
git clone https://github.com/chusakt/pd_ml_2026.git
cd pd_ml_2026

# Create .env
cp .env.example .env
nano .env
```

Edit `.env` with your actual values:
```
SECRET_KEY=451802e16a13efa5da771a73158f5290556b208ba76152e82b69afe012c3e0d9
SQLALCHEMY_DATABASE_URI=sqlite:///users.db
FLASK_ENV=production
REDIS_HOST=redis
REDIS_PORT=6379
APP_PORT=8080
GUNICORN_WORKERS=9
```

## 3. Build and run

```bash
docker compose up --build -d
```

## 4. Verify

```bash
# Check containers running
docker compose ps

# Check logs
docker compose logs -f

# Test the API
curl http://localhost:8080/
```

## 5. Open firewall (allow traffic)

```bash
ufw allow 8080
ufw allow 22
ufw enable
```

Your API will be at `http://your-droplet-ip:8080`

## 6. Setup HTTPS with Nginx + Let's Encrypt (free, recommended)

You need a domain (e.g., `pdml26.thanavarp.com`) pointing to your Droplet IP.

### 6.1 Point your domain to the Droplet
- Go to your domain registrar (e.g., Namecheap, Cloudflare, GoDaddy)
- Add an **A record**: `pdml26.thanavarp.com` → `your-droplet-ip`
- Wait for DNS to propagate (usually a few minutes)

### 6.2 Install Nginx and Certbot

```bash
apt update
apt install -y nginx certbot python3-certbot-nginx
```

### 6.3 Configure Nginx

```bash
nano /etc/nginx/sites-available/api
```

Paste this:
```nginx
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
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### 6.4 Get SSL certificate (auto-renew)

```bash
certbot --nginx -d pdml26.thanavarp.com
```

Follow the prompts. Certbot will automatically:
- Get a free SSL certificate
- Configure Nginx for HTTPS
- Set up auto-renewal (cron)

### 6.5 Update firewall

```bash
ufw allow 80
ufw allow 443
ufw deny 8080    # block direct access, force HTTPS through Nginx
```

### Done

Your API is now at `https://pdml26.thanavarp.com`

### Verify SSL renewal

```bash
certbot renew --dry-run
```
