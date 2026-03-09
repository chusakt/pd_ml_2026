import multiprocessing
import os

bind = "0.0.0.0:8080"
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
threads = 2
timeout = 300
keepalive = 5
preload_app = True
worker_class = "gthread"
