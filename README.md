# PD ML 2026 - Parkinson's Disease Screening API

Flask API server with ML models for Parkinson's disease screening.

## Project Structure

```
.
├── app.py                  # Main Flask application
├── config.py               # App configuration
├── gunicorn_config.py      # Gunicorn server settings
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image build
├── docker-compose.yml      # Docker services (app + redis)
├── setup_server.sh         # One-command server setup script
├── .env.example            # Environment variables template
├── modelfromdata2024b/     # Trained ML model files (.pkl)
└── static/                 # CSS assets
```

## Quick Install on Server (one command)

SSH into a fresh **Ubuntu 24.04** server and run:

```bash
curl -O https://raw.githubusercontent.com/chusakt/pd_ml_2026/main/setup_server.sh
chmod +x setup_server.sh
./setup_server.sh
```

This script will automatically:

1. Install Docker
2. Clone the repo
3. Create `.env` with secrets (pauses for you to edit)
4. Build and start Docker containers (app + redis)
5. Install Nginx + Let's Encrypt SSL for `pdml26.
6. Configure firewall

After it finishes, your API is live at `https://pdml26.domain.com`

## Manual Setup

### 1. Create a Droplet / VPS

- **Ubuntu 24.04**
- Recommended: **8 vCPU / 16GB RAM** (~$96/mo)
- Region: closest to your users (Singapore if Thailand)
- Add your SSH key


| Option     | Spec               | Cost     | Use case             |
| ------------ | -------------------- | ---------- | ---------------------- |
| Start here | 8 vCPU / 16GB RAM  | ~$96/mo  | Handles most traffic |
| Scale up   | 16 vCPU / 32GB RAM | ~$192/mo | Heavy concurrent use |

### 2. SSH in and setup

```bash
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone repo
git clone https://github.com/chusakt/pd_ml_2026.git
cd pd_ml_2026

# Create .env
cp .env.example .env
nano .env
```

### 3. Build and run

```bash
docker compose up --build -d
```

### 4. Verify

```bash
docker compose ps
docker compose logs -f
curl http://localhost:8080/health
```

### 5. Setup HTTPS (Nginx + Let's Encrypt)

Point your domain A record to the server IP first.

```bash
# Install Nginx + Certbot
apt update -y
apt install -y nginx certbot python3-certbot-nginx
```

Create Nginx config:

```bash
cat > /etc/nginx/sites-available/api << 'EOF'
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
EOF

ln -sf /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

Get SSL:

```bash
certbot --nginx -d pdml26.thanavarp.com
```

### 6. Firewall

```bash
ufw allow 22
ufw allow 80
ufw allow 443
ufw deny 8080
ufw enable
```

## Configuration

### Environment Variables (.env)


| Variable                | Description                   | Default              |
| ------------------------- | ------------------------------- | ---------------------- |
| SECRET_KEY              | Flask secret key (random hex) | change-me            |
| SQLALCHEMY_DATABASE_URI | Database connection string    | sqlite:///users.db   |
| FLASK_ENV               | Environment mode              | production           |
| REDIS_HOST              | Redis hostname                | redis                |
| REDIS_PORT              | Redis port                    | 6379                 |
| APP_PORT                | Exposed app port              | 8080                 |
| GUNICORN_WORKERS        | Number of gunicorn workers    | auto (cpu_count*2+1) |
| API_KEY                 | API key for authentication    | (required)           |

### API Authentication

All requests require the `X-API-Key` header (except `/health`):

```bash
curl -X POST https://pdml26.thanavarp.com/predict_dualtap \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"data": "..."}'
```

Without a valid key you get `401 Unauthorized`.

## Common Commands

```bash
cd /root/pd_ml_2026

# View logs
docker compose logs -f

# Restart
docker compose restart

# Rebuild after code changes
git pull
docker compose up --build -d

# Check SSL renewal
certbot renew --dry-run

# Edit .env after setup and restart
nano /root/pd_ml_2026/.env
cd /root/pd_ml_2026 && docker compose restart
```

## Update .env Only

If you only changed `.env` (no code changes), just restart the containers:

```bash
nano /root/pd_ml_2026/.env
cd /root/pd_ml_2026 && docker compose restart
```

No rebuild needed — `restart` picks up new env values.

## Fresh Reinstall

If you want to wipe everything and start over:

```bash
# Stop and remove everything
cd /root/pd_ml_2026
docker compose down

# Delete the repo folder
cd /root
rm -rf pd_ml_2026

# Run setup again
./setup_server.sh
```
