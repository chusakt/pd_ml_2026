#!/bin/bash
# ============================================================
# diagnose_post.sh — Run AFTER restart to check what happened.
# Usage: sudo bash diagnose_post.sh
# ============================================================

echo "=========================================="
echo " Post-incident diagnostics"
echo "=========================================="

echo ""
echo "--- 1. OOM Killer Events ---"
echo "(If you see entries here, the container was killed for using too much memory)"
dmesg -T | grep -iE "oom|killed|out of memory" | tail -20
echo ""

echo "--- 2. Docker container restart history ---"
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
echo ""

echo "--- 3. Docker logs: errors and warnings (last 200 lines) ---"
docker logs --tail 200 model_server-web-1 2>&1 | grep -iE "error|exception|killed|timeout|memory|oom|traceback|critical" | tail -30
echo ""

echo "--- 4. Docker logs: last lines before shutdown ---"
echo "(Look for the last successful request, then what came after)"
docker logs --tail 50 model_server-web-1 2>&1
echo ""

echo "--- 5. Docker events (last 24h) ---"
echo "(Look for 'die', 'oom', 'kill' events)"
docker events --since "24h" --until "$(date -Iseconds)" --filter "container=model_server-web-1" 2>&1 &
EVENTS_PID=$!
sleep 3
kill $EVENTS_PID 2>/dev/null
echo ""

echo "--- 6. Current memory state ---"
free -h
echo ""

echo "--- 7. Current disk state ---"
df -h /
echo ""

echo "--- 8. Leftover temp files in container ---"
docker exec model_server-web-1 sh -c 'ls -la /app/temp_* 2>/dev/null; echo "Count: $(ls /app/temp_* 2>/dev/null | wc -l)"' 2>&1
echo ""

echo "--- 9. Container resource usage right now ---"
docker stats --no-stream model_server-web-1 2>&1
echo ""

echo "=========================================="
echo " Key things to look for:"
echo "  - Section 1: OOM = memory ran out"
echo "  - Section 3: Traceback = code crash"
echo "  - Section 4: Last request before death"
echo "  - Section 5: 'die' event = container crashed"
echo "  - Section 8: Temp files = disk leak"
echo "=========================================="
