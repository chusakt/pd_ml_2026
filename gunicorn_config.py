import os

bind = "0.0.0.0:8080"
# ML prediction is CPU-bound; too many workers exhaust RAM
# (each worker loads all 8 models + scipy/librosa/parselmouth).
# On 16 GB / 8 vCPU droplet with 12 GB Docker limit → 3 workers is safe.
workers = int(os.getenv("GUNICORN_WORKERS", 3))
threads = 2
timeout = 300
keepalive = 5
preload_app = True
worker_class = "gthread"
