import os

bind = "0.0.0.0:8080"
# ML prediction is CPU-bound; too many workers exhaust RAM
# (each worker loads all 8 models + scipy/librosa/parselmouth).
# On 16 GB / 8 vCPU droplet with 12 GB Docker limit → 3 workers is safe.
workers = int(os.getenv("GUNICORN_WORKERS", 3))
threads = 2
timeout = 300
graceful_timeout = 30
keepalive = 5
preload_app = True
worker_class = "gthread"

# Recycle workers to release native memory held by numpy/scipy/parselmouth/librosa.
# Without this the workers slowly bloat and the server appears to "hang" after
# running for hours/days. Jitter avoids all workers recycling at once.
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 500))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 100))


def post_worker_init(worker):
    # Start background schedulers AFTER fork in each worker. They use Redis
    # locks so only one worker actually fires each scheduled task.
    # Starting threads before fork (at module import with preload_app=True) is a
    # known fork-after-thread footgun — child workers can inherit broken locks.
    try:
        import app as _app
        _app.start_background_schedulers()
    except Exception as e:
        print(f"Failed to start background schedulers: {e}")


def worker_abort(worker):
    # Fired when gunicorn's master kills a worker that exceeded `timeout`
    # (e.g. stuck on parselmouth/librosa). Alert before the process dies.
    try:
        import app as _app
        _app.send_error_alert(
            "worker_abort",
            f"Gunicorn worker pid={worker.pid} aborted (likely timeout > {timeout}s).\n"
            f"This usually means a request hung in native code (parselmouth/librosa) "
            f"or the worker ran out of memory.",
        )
    except Exception as e:
        print(f"worker_abort hook failed: {e}")


def worker_int(worker):
    try:
        import app as _app
        _app.send_error_alert(
            "worker_int",
            f"Gunicorn worker pid={worker.pid} received SIGINT/SIGQUIT.",
        )
    except Exception as e:
        print(f"worker_int hook failed: {e}")
