#!/bin/bash
# ============================================================
# diagnose_live.sh — Run this WHILE the container is unresponsive
# (before restarting). Captures system + container state.
# Usage: sudo bash diagnose_live.sh
# ============================================================

LOGDIR="/root/diagnose_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOGDIR"

echo "=== Saving diagnostics to $LOGDIR ==="

# --- Host-level ---
echo "[1/8] Host memory..."
free -h                          > "$LOGDIR/host_memory.txt" 2>&1

echo "[2/8] Host disk..."
df -h                            > "$LOGDIR/host_disk.txt" 2>&1

echo "[3/8] Top processes by memory..."
ps aux --sort=-%mem | head -30   > "$LOGDIR/host_top_mem.txt" 2>&1

echo "[4/8] OOM killer history (dmesg)..."
dmesg -T | grep -iE "oom|killed|out of memory" > "$LOGDIR/host_oom.txt" 2>&1

# --- Docker-level ---
echo "[5/8] Docker container status..."
docker ps -a                     > "$LOGDIR/docker_ps.txt" 2>&1
docker stats --no-stream         > "$LOGDIR/docker_stats.txt" 2>&1

echo "[6/8] Docker inspect (web container)..."
docker inspect model_server-web-1  > "$LOGDIR/docker_inspect.txt" 2>&1

echo "[7/8] Docker logs (last 500 lines)..."
docker logs --tail 500 model_server-web-1  > "$LOGDIR/docker_logs.txt" 2>&1

echo "[8/8] Docker events (last 1 hour)..."
docker events --since "1h" --until "$(date -Iseconds)" > "$LOGDIR/docker_events.txt" 2>&1 &
EVENTS_PID=$!
sleep 3
kill $EVENTS_PID 2>/dev/null

# --- Quick test ---
echo "[bonus] Trying to reach the app..."
curl -s -o /dev/null -w "HTTP status: %{http_code}, Time: %{time_total}s\n" \
  --max-time 10 http://localhost:8080/ > "$LOGDIR/curl_test.txt" 2>&1

echo ""
echo "=== Done. Files saved in $LOGDIR ==="
ls -la "$LOGDIR"
