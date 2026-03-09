# PD ML 2026 - Parkinson's Disease Screening API

Flask API server with ML models for Parkinson's disease screening.

## Project Structure

```
.
├── app.py                  # Main Flask application
├── config.py               # App configuration
├── gunicorn_config.py      # Gunicorn server settings
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version
├── Procfile                # Process command
├── Dockerfile              # Docker image build
├── docker-compose.yml      # Docker services (app + redis)
├── .env.example            # Environment variables template
├── .dockerignore           # Files excluded from Docker image
├── modelfromdata2024b/     # Trained ML model files (.pkl)
├── static/                 # CSS assets
└── .do/                    # DigitalOcean App Platform config (legacy)
```

## Run with Docker

### Prerequisites
- Docker & Docker Compose installed

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/chusakt/pd_ml_2026.git
cd pd_ml_2026

# 2. Create .env from template
cp .env.example .env
# Edit .env with your actual secrets

# 3. Build and run
docker compose up --build -d

# 4. Check logs
docker compose logs -f
```

App runs at `http://localhost:8080`

## Deploy on a Droplet (or any VPS)

### Recommended server: 8 vCPU / 16GB RAM (~$96/mo)

| Option     | Spec                 | Cost     | Use case             |
|------------|----------------------|----------|----------------------|
| Start here | 8 vCPU / 16GB RAM    | ~$96/mo  | Handles most traffic |
| Scale up   | 16 vCPU / 32GB RAM   | ~$192/mo | Heavy concurrent use |

### Deploy

```bash
# 1. SSH into your server
ssh root@your-server-ip

# 2. Install Docker
curl -fsSL https://get.docker.com | sh

# 3. Clone and setup
git clone https://github.com/chusakt/pd_ml_2026.git
cd pd_ml_2026
cp .env.example .env
# Edit .env with your actual secrets

# 4. Run
docker compose up --build -d
```

## Configuration

### Environment Variables (.env)

| Variable               | Description                      | Default                |
|------------------------|----------------------------------|------------------------|
| SECRET_KEY             | Flask secret key                 | change-me              |
| SQLALCHEMY_DATABASE_URI| Database connection string       | sqlite:///users.db     |
| FLASK_ENV              | Environment mode                 | production             |
| REDIS_HOST             | Redis hostname                   | redis (via docker)     |
| REDIS_PORT             | Redis port                       | 6379                   |
| APP_PORT               | Exposed app port                 | 8080                   |
| GUNICORN_WORKERS       | Number of gunicorn workers       | auto (cpu_count*2+1)   |

### Why Docker vs Previous Setup

| Setting    | Before (DO App Platform)         | Now (Docker)                          |
|------------|----------------------------------|---------------------------------------|
| Workers    | Hardcoded 9                      | Env var `GUNICORN_WORKERS` (default: auto) |
| Redis      | Exposed port 6379                | Internal only                         |
| Memory     | 32GB allocated                   | 12GB app limit, 256MB Redis           |
| Health     | None                             | App + Redis health checks             |
| Containers | 3 x $392/mo = $1,176/mo         | 1 container with 9 workers (~$96/mo)  |

Models load once via `preload_app = True`, so 1 container with 9 workers gives the same throughput as 3 containers.
