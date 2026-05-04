#  note questionnaire list check what's wrong
# ส่วนที่2 แบบคัดกรองอาการโรคพาร์กินสัน
# 1. ท่านเคยมีอาการสั่นที่มือ หรือขา โดยมีอาการขณะพักหรืออยู่เฉยๆ
# 2. ท่านเขียนหนังสือช้าลง หรือเขียนหนังสือตัวเล็กลงกว่าเดิม
# 3. ท่านรู้สึกว่าเคลื่อนไหวช้าลงกว่าเมื่อก่อน เช่น การหวีผม แต่งตัว อาบน้ำ หรือรู้สึกว่าการติดกระดุม หรือเปิดฝาขวดน้ำทำได้ลำบากกว่าเก่า
# 4. มีคนบอกว่าเสียงของท่านเบาลงกว่าเมื่อก่อน หรือผู้ฟังต้องถามซ้ำบ่อย ๆ เพราะไม่ได้ยินเสียงท่านพูด
# 5. ท่านรู้สึกว่าแขนของท่านแกว่งน้อยลงเวลาเดิน
# 6.ท่านเดินก้าวสั้นๆ และเดินซอยเท้าถี่
# 7. ท่านมีอาการก้าวขาไม่ออก หรือก้าวติด ขณะเริ่มต้นออกเดิน หรือกำลังเดิน หรือหมุนตัว
# 8. ท่านมีปัญหาพุ่งตัวไปข้างหน้าขณะเดินทำให้ก้าวตามไม่ทัน หรือหยุดเดินทันทีได้ยาก
# 9. ท่านมีอาการข้อใดข้อหนึ่งต่อไปนี้ พลิกตัวได้ลำบากเวลานอน หรือลุกจากที่นอนลำบาก หรือหลังจากนั่งลงแล้ว ท่านรู้สึกว่าลุกยาก หรือลุกลำบาก
# 10. อาการสั่น เคลื่อนไหวช้า หรือแข็งเกร็งเริ่มที่ข้างใดข้างหนึ่งของร่างกายก่อน
# แบบสอบถามเกี่ยวกับอาการนอกเหนือจากการเคลื่อนไหว (Non-mortor) จำนวน 5 ข้อ
# 11. ท่านทราบว่า ตนเองมีอาการพูดออกเสียง หรือตะโกน หรือขยับแขนขาที่อาจจะสอดคล้องกับความฝัน หรือตกเตียงขณะนอนหลับ หรือเคยได้รับการบอกจากคู่นอน หรือผู้ดูแล ว่าท่านมีอาการดังกล่าว
# 12. ท่านมีอาการง่วงนอนระหว่างวันมากผิดปกติ หรือผลอยหลับระหว่างขณะทำกิจกรรมเป็นประจำ
# 13. ท่านรู้สึกว่าการได้กลิ่นของท่านลดลง
# 14. ในช่วง 3 เดือนที่ผ่านมา ท่านมีอาการท้องผูกเรื้อรัง โดยถ่ายน้อยกว่า 3 ครั้ง/ สัปดาห์
# 15. ท่านมีอาการซึมเศร้า ร้องไห้ง่ายกว่าปกติ หรือขาดความสนใจต่อสิ่งแวดล้อมรอบข้าง หรือสิ่งที่เคยให้ความสนุกสนานในอดีต
# แบบสอบถามเกี่ยวกับอาการโรคพาร์กินสันเทียม (atypical Parkinsonism) จำนวน 5 ข้อ
# 16. ท่านเคยเห็นภาพหลอน หรือได้ยินเสียง โดยที่ไม่มีตัวตน
# 17. ท่านมีอาการหน้ามืด มึน หรือเวียนศีรษะ เวลาลุกยืน และอาการมักจะดีขึ้น หรือหายไปหลังจากที่นั่งหรือนอน
# 18. ท่านมีปัญหาการควบคุมปัสสาวะ เช่น กลั้นปัสสาวะไม่ได้ ปัสสาวะคั่งเป็นประจำ
# 19. ท่านมีปัญหาความคิดวิเคราะห์ ความจำ การคำนวณ ที่แย่ลง นานมากกว่า 1 ปีขึ้นไป
# 20. มีปัญหาการทรงตัว หรือหกล้มบ่อย ตั้งแต่ในระยะแรกที่เกิดอาการ เคลื่อนไหวช้า แข็งเกร็ง หรือสั่น
# case 1

# --
from flask import Flask, request, jsonify
import json
import math
import numpy as np
from statistics import mean
import os
import pickle
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.stats import kurtosis, skew
import EntropyHub as EH
import base64
import parselmouth
from parselmouth.praat import call
import statistics
from scipy.stats.mstats import zscore
import uuid
import pandas as pd
import requests
import zipfile
import matplotlib  # <- Add this line
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

import redis
from flask_cors import CORS
import threading
from datetime import datetime, timezone, timedelta

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Use Docker's service name as the Redis host.
# Socket timeouts are critical: without them, a Redis hiccup blocks every
# request thread indefinitely in before_request, and the whole server hangs.
redis_conn = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    socket_timeout=2,
    socket_connect_timeout=2,
    health_check_interval=30,
    retry_on_timeout=False,
)




# url = 'https://notify-api.line.me/api/notify'
# LINE_CHANNEL_ACCESS_TOKEN = 'faMFKYVDu3jdD2HMrCCJiERZ4J9aKZKBElenrzOCeDM'
# LINE_USER_ID = 'bangkok73'
# def send_text(text):
#     LINE_HEADERS = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+LINE_CHANNEL_ACCESS_TOKEN}
#     session_post = requests.post(url, headers=LINE_HEADERS , data = {'message':text})
#     print(session_post.text)

# Global variable to keep track of API request count
request_count = 0  # Initialize request counter
# Global variable to track successful requests
successful_request_count = 0

# Telegram credentials come from .env (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID).
# If TELEGRAM_BOT_TOKEN is unset, both daily summaries and error alerts no-op.
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '').strip()

def send_telegram_message(message, parse_mode=None):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
        }
        if parse_mode:
            payload['parse_mode'] = parse_mode
        response = requests.post(telegram_url, json=payload, timeout=5)
        if response.status_code == 200:
            print("Message sent successfully via Telegram.")
        else:
            print(f"Failed to send message: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error sending message via Telegram: {e}")


# --- Error-alert Telegram bot ---
# By default reuses the main TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID. To send
# error alerts to a separate bot/chat, set TELEGRAM_ERROR_BOT_TOKEN and/or
# TELEGRAM_ERROR_CHAT_ID in .env.
TELEGRAM_ERROR_BOT_TOKEN = os.getenv('TELEGRAM_ERROR_BOT_TOKEN', '').strip() or TELEGRAM_BOT_TOKEN
TELEGRAM_ERROR_CHAT_ID = os.getenv('TELEGRAM_ERROR_CHAT_ID', '').strip() or TELEGRAM_CHAT_ID
ERROR_ALERT_THROTTLE_SECONDS = int(os.getenv('ERROR_ALERT_THROTTLE_SECONDS', 300))


def send_error_alert(error_type: str, detail: str):
    """Send an error alert via the dedicated error bot, with per-type throttling.

    Why throttle: if an endpoint starts erroring on every request, sending one
    Telegram message per error would flood the chat AND hit Telegram's per-bot
    rate limits. Within the throttle window, suppressed errors are counted and
    the count is appended to the next alert.
    """
    if not TELEGRAM_ERROR_BOT_TOKEN or not TELEGRAM_ERROR_CHAT_ID:
        return
    try:
        throttle_key = f"error_alert_throttle:{error_type}"
        count_key = f"error_alert_count:{error_type}"
        try:
            got_slot = redis_conn.set(
                throttle_key, '1', nx=True, ex=ERROR_ALERT_THROTTLE_SECONDS
            )
        except Exception:
            # If Redis is down, alert anyway — that's exactly when we need to know.
            got_slot = True

        if not got_slot:
            try:
                redis_conn.incr(count_key)
                redis_conn.expire(count_key, ERROR_ALERT_THROTTLE_SECONDS)
            except Exception:
                pass
            return

        suppressed = 0
        try:
            v = redis_conn.get(count_key)
            if v:
                suppressed = int(v)
            redis_conn.delete(count_key)
        except Exception:
            pass

        TH_TZ = timezone(timedelta(hours=7))
        now = datetime.now(TH_TZ).strftime('%Y-%m-%d %H:%M:%S')
        text = (
            f"🚨 API Error: {error_type}\n"
            f"🕒 {now} (Thai time)\n"
            f"pid={os.getpid()}\n\n"
            f"{detail[:3500]}"
        )
        if suppressed:
            mins = ERROR_ALERT_THROTTLE_SECONDS // 60
            text += f"\n\n(+{suppressed} more of this type suppressed in last {mins} min)"

        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_ERROR_BOT_TOKEN}/sendMessage"
        requests.post(
            telegram_url,
            json={'chat_id': TELEGRAM_ERROR_CHAT_ID, 'text': text},
            timeout=5,
        )
    except Exception as e:
        # Never let alerting break a request.
        print(f"send_error_alert failed: {e}")


def report_route_error(endpoint: str, exc: Exception):
    """Capture traceback and alert. Call from route-level except blocks."""
    import traceback
    tb = traceback.format_exc()
    send_error_alert(
        error_type=f"{endpoint}:{type(exc).__name__}",
        detail=f"{endpoint} raised {type(exc).__name__}: {exc}\n\n{tb}",
    )

# --- Endpoint call counter (stored in Redis, shared across workers) ---
TRACKED_ENDPOINTS = [
    'predict_questionaire',
    'predict_dualtap',
    'predict_pinchtosize',
    'predict_tremor_rest',
    'predict_tremor_post',
    'predict_gait_stab',
    'predict_gait_walk',
    'predict_voice_ahh',
    'predict_voice_ypl',
    'predict_voice_ahh_mp3',
    'predict_voice_ypl_mp3',
    'predict_voting',
]

# Endpoints that take a multipart file upload instead of a JSON body. Saved
# payloads for these are raw bytes, replayed via test_client form-data.
FILE_UPLOAD_ENDPOINTS = {'predict_voice_ahh_mp3', 'predict_voice_ypl_mp3'}

# --- Saved-payload self-test ---
# Each successful prediction saves its request payload to TEST_PAYLOADS_DIR,
# overwriting any previous one for that endpoint. /selftest (and the Telegram
# /selftest command) replays those payloads through the live app's test client
# to verify each endpoint still produces a valid prediction.
TEST_PAYLOADS_DIR = os.getenv('TEST_PAYLOADS_DIR', '/app/test_payloads')
SELFTEST_HEADER = 'X-Selftest-Run'  # marker to skip counters during self-test
try:
    os.makedirs(TEST_PAYLOADS_DIR, exist_ok=True)
except Exception as e:
    print(f"Could not create {TEST_PAYLOADS_DIR}: {e}")


def _save_test_payload(endpoint: str, kind: str, data) -> None:
    """Persist the newest successful payload for an endpoint.

    kind='json' → data is a dict, written as UTF-8 JSON.
    kind='file' → data is raw bytes, written as a binary blob.
    """
    try:
        if kind == 'json':
            path = os.path.join(TEST_PAYLOADS_DIR, f"{endpoint}.json")
            tmp = path + ".tmp"
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            os.replace(tmp, path)
        elif kind == 'file':
            path = os.path.join(TEST_PAYLOADS_DIR, f"{endpoint}.bin")
            tmp = path + ".tmp"
            with open(tmp, 'wb') as f:
                f.write(data)
            os.replace(tmp, path)
    except Exception as e:
        print(f"Failed to save test payload for {endpoint}: {e}")


def run_selftest(target=None) -> dict:
    """Replay saved payloads through Flask's test client. Returns per-endpoint dict.

    target=None → run every TRACKED_ENDPOINTS.
    target='predict_voice_ahh' → just that one.
    """
    import time as _time
    import io
    targets = [target] if target else list(TRACKED_ENDPOINTS)
    results = {}
    client = app.test_client()
    headers = {SELFTEST_HEADER: '1'}
    if API_KEY:
        headers['X-API-Key'] = API_KEY

    for ep in targets:
        if ep not in TRACKED_ENDPOINTS:
            results[ep] = {'status': 'unknown_endpoint'}
            continue

        is_file = ep in FILE_UPLOAD_ENDPOINTS
        path = os.path.join(
            TEST_PAYLOADS_DIR,
            f"{ep}.bin" if is_file else f"{ep}.json",
        )
        if not os.path.exists(path):
            results[ep] = {'status': 'no_payload'}
            continue

        try:
            t0 = _time.time()
            if is_file:
                with open(path, 'rb') as f:
                    blob = f.read()
                resp = client.post(
                    f'/{ep}',
                    data={'file': (io.BytesIO(blob), 'replay.mp3')},
                    content_type='multipart/form-data',
                    headers=headers,
                )
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    body = json.load(f)
                resp = client.post(f'/{ep}', json=body, headers=headers)
            elapsed_ms = int((_time.time() - t0) * 1000)
            data = resp.get_json(silent=True) or {}
            ok = (
                200 <= resp.status_code < 300
                and 'error' not in data
                and str(data.get('prediction', '')) != '2'
            )
            results[ep] = {
                'status': 'ok' if ok else 'fail',
                'http': resp.status_code,
                'prediction': data.get('prediction'),
                'error': data.get('error'),
                'time_ms': elapsed_ms,
            }
        except Exception as e:
            results[ep] = {'status': 'error', 'error': str(e)}

    return results


def _format_selftest_results(results: dict) -> str:
    lines = ["🔧 Self-test results"]
    for ep, r in results.items():
        st = r.get('status')
        if st == 'ok':
            lines.append(f"✅ {ep} ({r.get('time_ms', '?')}ms) → {r.get('prediction')}")
        elif st == 'fail':
            err = r.get('error') or f"prediction={r.get('prediction')}"
            lines.append(f"❌ {ep} ({r.get('time_ms', '?')}ms) → {err}")
        elif st == 'no_payload':
            lines.append(f"⚠️ {ep} — no saved payload yet")
        elif st == 'unknown_endpoint':
            lines.append(f"❓ {ep} — not tracked")
        elif st == 'error':
            lines.append(f"💥 {ep} — {r.get('error')}")
        else:
            lines.append(f"? {ep} — {st}")
    return "\n".join(lines)


def send_chart_summary():
    """Send a per-endpoint call/success summary as a Telegram bar chart.

    Reads + resets `endpoint_success_counts` and `endpoint_fail_counts`. Skips
    sending entirely if there were no calls since the last reset.
    """
    try:
        TH_TZ = timezone(timedelta(hours=7))
        now = datetime.now(TH_TZ)

        success = redis_conn.hgetall('endpoint_success_counts') or {}
        failure = redis_conn.hgetall('endpoint_fail_counts') or {}

        def _get(d, key):
            return int(d.get(key.encode(), d.get(key, 0)))

        rows = []
        max_total = 0
        grand_succ = 0
        grand_total = 0
        for ep in TRACKED_ENDPOINTS:
            s = _get(success, ep)
            f = _get(failure, ep)
            t = s + f
            rate = (s / t * 100) if t else 0
            rows.append((ep, s, t, rate))
            if t > max_total:
                max_total = t
            grand_succ += s
            grand_total += t

        if grand_total == 0:
            # No traffic last hour; reset (defensive) and skip the message.
            try:
                redis_conn.delete('endpoint_success_counts', 'endpoint_fail_counts')
            except Exception:
                pass
            print(f"Chart summary: no calls since last reset, skipping send")
            return

        BAR_WIDTH = 18
        chart_lines = []
        # Strip the redundant "predict_" prefix to fit on a phone screen.
        for ep, s, t, rate in rows:
            short = ep.replace('predict_', '')
            bar_len = round((t / max_total) * BAR_WIDTH) if max_total else 0
            bar = '█' * bar_len + '·' * (BAR_WIDTH - bar_len)
            chart_lines.append(f"{short:<14} {bar} {t:>3} ({rate:>5.1f}%)")

        grand_rate = (grand_succ / grand_total * 100) if grand_total else 0
        text = (
            f"📈 รายงานสรุปประจำวัน (20:00)\n"
            f"📅 {now.strftime('%Y-%m-%d %H:%M')} (เวลาไทย)\n"
            f"```\n"
            + "\n".join(chart_lines)
            + f"\n```\n"
            f"รวม: {grand_total} ครั้ง • success {grand_rate:.1f}%"
        )

        send_telegram_message(text, parse_mode='Markdown')

        try:
            redis_conn.delete('endpoint_success_counts', 'endpoint_fail_counts')
        except Exception:
            pass
        print(f"Chart summary sent at {now}: total={grand_total}, success_rate={grand_rate:.1f}%")
    except Exception as e:
        print(f"Error sending chart summary: {e}")


def _chart_summary_scheduler():
    """Background thread: fire send_chart_summary once a day at 20:00 Thai time."""
    import time as _time
    TH_TZ = timezone(timedelta(hours=7))
    TARGET_HOUR = 20
    while True:
        try:
            now = datetime.now(TH_TZ)
            target = now.replace(hour=TARGET_HOUR, minute=0, second=0, microsecond=0)
            if now >= target:
                target += timedelta(days=1)
            wait_seconds = (target - now).total_seconds()
            print(f"Chart summary scheduler: next run at {target}, waiting {wait_seconds:.0f}s")
            _time.sleep(wait_seconds)

            # Cross-worker lock keyed by date — only one worker actually sends.
            lock_key = f"chart_summary_lock:{datetime.now(TH_TZ).strftime('%Y-%m-%d')}"
            try:
                got_lock = redis_conn.set(lock_key, os.getpid(), nx=True, ex=3600)
            except Exception as e:
                print(f"Chart summary lock check failed: {e}")
                got_lock = False
            if got_lock:
                send_chart_summary()
        except Exception as e:
            print(f"Chart summary scheduler error: {e}")
            _time.sleep(60)


# --- Scheduled container restart (every midnight Thai time) ---
# Strategy: a worker thread sleeps until midnight, sends a Telegram heads-up,
# then SIGTERMs PID 1 (gunicorn master). The Dockerfile uses `CMD [...]` exec
# form so PID 1 is gunicorn master; killing it triggers Docker's
# `restart: unless-stopped` policy, which brings up a fresh container.

def _trigger_restart(reason: str):
    """Notify Telegram, then SIGTERM gunicorn master so Docker restarts the container."""
    import time as _time
    import signal
    TH_TZ = timezone(timedelta(hours=7))
    now = datetime.now(TH_TZ).strftime('%Y-%m-%d %H:%M:%S')
    send_telegram_message(
        f"🔄 Restarting model server\n"
        f"📅 {now} (Thai time)\n"
        f"Reason: {reason}"
    )
    _time.sleep(2)  # Give Telegram a moment to deliver before we tear down.
    try:
        os.kill(1, signal.SIGTERM)
    except ProcessLookupError:
        # Not running with PID 1 as gunicorn master (e.g. local dev) — fall back
        # to signaling our own master process group.
        try:
            os.kill(os.getppid(), signal.SIGTERM)
        except Exception as e:
            print(f"Restart fallback SIGTERM failed: {e}")
    except Exception as e:
        print(f"Restart SIGTERM to PID 1 failed: {e}")


def _midnight_restart_scheduler():
    """Background thread: trigger a coordinated container restart at 00:00 Thai time."""
    import time as _time
    TH_TZ = timezone(timedelta(hours=7))
    while True:
        try:
            now = datetime.now(TH_TZ)
            target = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            wait_seconds = (target - now).total_seconds()
            print(f"Midnight restart scheduler: next trigger at {target}, waiting {wait_seconds:.0f}s")
            _time.sleep(wait_seconds)

            # Cross-worker lock so only one worker actually triggers the restart.
            lock_key = f"midnight_restart_lock:{datetime.now(TH_TZ).strftime('%Y-%m-%d')}"
            try:
                got_lock = redis_conn.set(lock_key, os.getpid(), nx=True, ex=3600)
            except Exception as e:
                print(f"Midnight restart lock check failed: {e}")
                got_lock = False

            if got_lock:
                _trigger_restart("scheduled midnight restart")
                # We're being torn down — but loop one more time defensively.
                _time.sleep(60)
            else:
                # Another worker is handling it; wait past midnight before re-looping.
                _time.sleep(120)
        except Exception as e:
            print(f"Midnight restart scheduler error: {e}")
            _time.sleep(60)


def _container_boot_id() -> str:
    """Stable unique id per container instance (resets on restart, not on worker recycle)."""
    try:
        # /proc/1/stat field 22 (1-indexed) = process start time in clock ticks since system boot.
        # Combined with hostname this is unique per gunicorn-master start = per container start.
        with open("/proc/1/stat") as f:
            fields = f.read().split()
        return f"{os.uname().nodename}:{fields[21]}"
    except Exception:
        # Plain Python / non-Linux fallback: just use hostname (will dedupe within one process).
        try:
            return os.uname().nodename
        except Exception:
            return "unknown-host"


def announce_startup_once():
    """Send a 'server started' Telegram message exactly once per container boot.

    All workers call this; a Redis NX lock keyed on the master process's start
    time ensures only one worker wins. Worker recycles do not re-announce
    because the boot_id stays the same until the container itself restarts.
    """
    boot_id = _container_boot_id()
    key = f"container_announced:{boot_id}"
    try:
        won = redis_conn.set(key, os.getpid(), nx=True, ex=86400)
    except Exception as e:
        print(f"Startup announce lock check failed: {e}")
        return
    if not won:
        return
    TH_TZ = timezone(timedelta(hours=7))
    now = datetime.now(TH_TZ).strftime('%Y-%m-%d %H:%M:%S')
    workers = os.getenv('GUNICORN_WORKERS', '?')
    send_telegram_message(
        f"✅ Model server started\n"
        f"📅 {now} (Thai time)\n"
        f"workers={workers}, boot_id={boot_id}"
    )


# --- Telegram command listener (long-polling) ---
# Lets you trigger /selftest from Telegram. A Redis lock ensures only one
# worker actually polls Telegram, so we don't get duplicate processing.
TELEGRAM_POLLER_LOCK_KEY = "telegram_poller_lock"
TELEGRAM_POLLER_LOCK_TTL = 120  # seconds

_TG_HELP = (
    "Commands:\n"
    "/selftest — replay saved payloads on every endpoint\n"
    "/selftest <endpoint> — replay just one (e.g. predict_voice_ahh)\n"
    "/list — show which endpoints have a saved payload\n"
    "/help — this help"
)


def _run_and_report_selftest(target):
    """Run self-test in a thread so the Telegram listener can keep polling."""
    try:
        send_telegram_message(
            f"🔧 Running self-test{(' for ' + target) if target else ' (all endpoints)'}..."
        )
        results = run_selftest(target)
        send_telegram_message(_format_selftest_results(results))
    except Exception as e:
        send_telegram_message(f"Self-test crashed: {e}")


def _handle_telegram_command(text: str):
    parts = text.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else None

    if cmd in ('/selftest', '/test'):
        threading.Thread(
            target=_run_and_report_selftest, args=(arg,), daemon=True
        ).start()
    elif cmd == '/list':
        try:
            files = sorted(os.listdir(TEST_PAYLOADS_DIR))
        except Exception as e:
            send_telegram_message(f"Error listing payloads: {e}")
            return
        if not files:
            send_telegram_message("No saved test payloads yet.")
        else:
            send_telegram_message("Saved payloads:\n" + "\n".join(files))
    elif cmd in ('/help', '/start'):
        send_telegram_message(_TG_HELP)
    else:
        send_telegram_message(f"Unknown command: {cmd}\n\n{_TG_HELP}")


def _telegram_bot_listener():
    """Long-poll Telegram for commands. One worker holds the poll lock at a time.

    Authorization: only messages from chat_id == TELEGRAM_CHAT_ID are processed.
    Anyone else sending the bot a message is silently ignored.
    """
    import time as _time
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram listener: no token/chat_id, not starting")
        return

    offset = 0
    have_lock = False
    while True:
        try:
            if not have_lock:
                got = redis_conn.set(
                    TELEGRAM_POLLER_LOCK_KEY,
                    os.getpid(),
                    nx=True,
                    ex=TELEGRAM_POLLER_LOCK_TTL,
                )
                if not got:
                    _time.sleep(TELEGRAM_POLLER_LOCK_TTL // 2)
                    continue
                have_lock = True
                print(f"Telegram listener: pid {os.getpid()} acquired poller lock")

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
            resp = requests.get(
                url,
                params={'offset': offset, 'timeout': 25},
                timeout=30,
            )
            try:
                redis_conn.expire(TELEGRAM_POLLER_LOCK_KEY, TELEGRAM_POLLER_LOCK_TTL)
            except Exception:
                pass

            if resp.status_code != 200:
                print(f"Telegram getUpdates {resp.status_code}: {resp.text[:200]}")
                _time.sleep(10)
                continue

            data = resp.json()
            for update in data.get('result', []):
                offset = update['update_id'] + 1
                msg = update.get('message') or update.get('channel_post') or {}
                text = msg.get('text', '') or ''
                from_chat = (msg.get('chat') or {}).get('id')
                if str(from_chat) != str(TELEGRAM_CHAT_ID):
                    continue
                if text.startswith('/'):
                    try:
                        _handle_telegram_command(text)
                    except Exception as e:
                        send_telegram_message(f"Command error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"Telegram listener network error: {e}")
            have_lock = False  # release lock implicitly via TTL
            _time.sleep(10)
        except Exception as e:
            print(f"Telegram listener error: {e}")
            _time.sleep(30)


_scheduler_started = False
_scheduler_lock = threading.Lock()

def start_background_schedulers():
    """Idempotent — safe to call from gunicorn post_worker_init in every worker.

    Starts the midnight-restart loop, the 20:00 chart-summary loop, and the
    Telegram command listener. Sends a one-time 'server started' Telegram.
    """
    global _scheduler_started
    with _scheduler_lock:
        if not _scheduler_started:
            threading.Thread(target=_midnight_restart_scheduler, daemon=True).start()
            threading.Thread(target=_chart_summary_scheduler, daemon=True).start()
            threading.Thread(target=_telegram_bot_listener, daemon=True).start()
            _scheduler_started = True
    # Call from every worker; Redis NX lock makes it idempotent across workers.
    announce_startup_once()

# Under gunicorn the post_worker_init hook starts the schedulers after fork.
# For `python app.py` / Flask dev server, the start happens at __main__ below.


# app = Flask(__name__)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

# =====================================


# --- CORS / Proxy support (required for browser webapps calling this API) ---
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

cors_origins_env = os.getenv('CORS_ORIGINS', '').strip()
if cors_origins_env:
    CORS_ORIGINS = [o.strip() for o in cors_origins_env.split(',') if o.strip()]
else:
    # Defaults for local development (set CORS_ORIGINS in production)
    CORS_ORIGINS = [
        'http://localhost:3000', 'http://127.0.0.1:3000',
        'http://localhost:5173', 'http://127.0.0.1:5173',
    ]

CORS_SUPPORTS_CREDENTIALS = os.getenv('CORS_SUPPORTS_CREDENTIALS', 'false').lower() in ('1','true','yes','y')

# If you enable credentials, you MUST NOT use '*' as an allowed origin.
if CORS_SUPPORTS_CREDENTIALS and '*' in CORS_ORIGINS:
    CORS_ORIGINS = [o for o in CORS_ORIGINS if o != '*']

CORS(
    app,
    resources={r'/*': {'origins': CORS_ORIGINS}},
    supports_credentials=CORS_SUPPORTS_CREDENTIALS,
    allow_headers=['Content-Type', 'Authorization', 'X-API-Key'],
    methods=['GET', 'POST', 'OPTIONS'],
)

# --- API Key Authentication ---
API_KEY = os.getenv("API_KEY")

@app.before_request
def check_api_key():
    # Skip preflight OPTIONS requests
    if request.method == 'OPTIONS':
        return ('', 204)
    # Skip health check endpoint
    if request.path == '/health':
        return
    # Require API key if set
    if API_KEY:
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401


@app.after_request
def track_endpoint_success(response):
    """Bump per-endpoint success/fail counters AND save the latest successful
    request payload for self-test replay.

    Self-test replays carry the X-Selftest-Run header and are excluded from
    counters and payload capture (they replay an already-saved payload).
    """
    try:
        endpoint_name = (request.path or '').lstrip('/')
        if endpoint_name not in TRACKED_ENDPOINTS:
            return response
        if request.headers.get(SELFTEST_HEADER) == '1':
            return response

        is_success = False
        if 200 <= response.status_code < 300:
            data = response.get_json(silent=True) or {}
            if 'error' in data:
                is_success = False
            elif str(data.get('prediction', '')) == '2':
                is_success = False
            else:
                is_success = True

        try:
            bucket = 'endpoint_success_counts' if is_success else 'endpoint_fail_counts'
            redis_conn.hincrby(bucket, endpoint_name, 1)
        except Exception:
            pass

        # Save the newest successful JSON payload for self-test replay.
        # File-upload endpoints save themselves inside the route because the
        # multipart stream is consumed by the time we get here.
        if (
            is_success
            and endpoint_name not in FILE_UPLOAD_ENDPOINTS
            and request.is_json
        ):
            try:
                req_body = request.get_json(silent=True)
                if req_body is not None:
                    _save_test_payload(endpoint_name, 'json', req_body)
            except Exception:
                pass
    except Exception:
        pass
    return response


# =====================================


# @app.before_request
# def increment_request_count():
#     global request_count
#     if request.endpoint != "static":  # Ignore static file requests
#         request_count += 1  # Increment the request count

#         # Send an update every 10 requests
#         if request_count % 20 == 0:
#             send_telegram_message(f"API request count is now at {request_count}.")

#         # Reset the count when it reaches 10,000
#         if request_count >= 1000:
#             send_telegram_message(f"API request count has reached {request_count}. Resetting the counter.")
#             request_count = 0



limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["120 per second"]
)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = {
        "status": e.code,
        "message": e.description
    }
    return jsonify(response), e.code


@app.errorhandler(Exception)
def handle_generic_exception(e):
    try:
        report_route_error(request.path or 'unknown', e)
    except Exception:
        pass
    response = {
        "status": 500,
        "message": "An unexpected error occurred."
    }
    return jsonify(response), 500



# Load the trained model from the pickle file
modeltouse_dual = "trained_model_dualtap__SMOTE.pkl"
modeltouse_pinch = "trained_model_pinch_fe_SMOTE.pkl"
modeltouse_tremor_resthand = "trained_model_RestHand_featu_SMOTE.pkl"
modeltouse_tremor_posthand = "trained_model_PosturalHand_f_SMOTE.pkl"
modeltouse_tremor_reststabi = "trained_model_PosturalStabil_SMOTE.pkl"
modeltouse_tremor_restwalk = "trained_model_walk_feature.c_SMOTE.pkl"
modeltouse_voice_YPL = "trained_model_voice_fe_YaiParLarn_SMOTE.pkl"
modeltouse_voice_ahh = "trained_model_voice_fe_Ahh_SMOTE.pkl"

base_path2 = "./modelfromdata2024b"
modeltouse_dual = os.path.join(base_path2, modeltouse_dual)
modeltouse_pinch = os.path.join(base_path2, modeltouse_pinch)
modeltouse_tremor_resthand = os.path.join(base_path2, modeltouse_tremor_resthand)
modeltouse_tremor_posthand = os.path.join(base_path2, modeltouse_tremor_posthand)
modeltouse_tremor_reststabi = os.path.join(base_path2, modeltouse_tremor_reststabi)
modeltouse_tremor_restwalk = os.path.join(base_path2, modeltouse_tremor_restwalk)
modeltouse_voice_YPL = os.path.join(base_path2, modeltouse_voice_YPL)
modeltouse_voice_ahh = os.path.join(base_path2, modeltouse_voice_ahh)

with open(modeltouse_dual, 'rb') as f:
    model_dual = pickle.load(f)
with open(modeltouse_pinch, 'rb') as f:
    model_pinch = pickle.load(f)
with open(modeltouse_tremor_resthand, 'rb') as f:
    model_tremor_resthand = pickle.load(f)
with open(modeltouse_tremor_posthand, 'rb') as f:
    model_tremor_posthand = pickle.load(f)
with open(modeltouse_tremor_reststabi, 'rb') as f:
    model_tremor_stabi = pickle.load(f)
with open(modeltouse_tremor_restwalk, 'rb') as f:
    model_tremor_walk = pickle.load(f)
with open(modeltouse_voice_YPL, 'rb') as f:
    model_voice_YPL = pickle.load(f)
with open(modeltouse_voice_ahh, 'rb') as f:
    model_voice_AHH = pickle.load(f)


@app.route('/predict_questionaire', methods=['POST'])  
def predict_questionaire():
    try:
        # send_text("App called: predict_questionaire")
        # send_telegram_message("App called: predict_questionaire")
        if request.is_json:
            req = request.get_json()

            # Read the request data as a string and convert to list of float
            read_feat = req['data']
            list_of_floats = [float(item) for item in read_feat.split(',')]

            # Convert to DataFrame for processing
            df3 = pd.DataFrame([list_of_floats])

            # Check if there are at least 5 occurrences of "1" in the DataFrame
            if (df3.values == 1).sum() >= 5:
                return jsonify({"prediction": "1"})
            else:
                return jsonify({"prediction": "0"})

    except Exception as e:
        report_route_error('predict_questionaire', e)
        return jsonify({"error": str(e), "prediction": "2"})



# Function to extract TapCount and additional statistics from the JSON input
def extract_tapcount_statistics(data):
    score = data['score']

    # Extract circle data
    jL = data['recording']['circleL']
    jR = data['recording']['circleR']
    cLx, cLy = jL['x'], jL['y']
    cRx, cRy = jR['x'], jR['y']
    cRadius = jL['r']

    distancEachPoint = []
    inLeft = 0
    inRight = 0
    jf = data['recording']['taps']
    ts_instroke_mean = []

    for jstroke in jf:
        jjj = jstroke['data']
        ts_instroke = []
        for jjjj in jjj:
            xpo, ypo, ts_ = jjjj['x'], jjjj['y'], jjjj['ts']
            ts_instroke.append(ts_)

            # Compare to L and R, then decide which side
            if (xpo - cLx) >= (cRx - xpo):
                inRight += 1
                dispo = math.sqrt((xpo - cRx) ** 2 + (ypo - cRy) ** 2)
                distancEachPoint.append(dispo)
            else:
                inLeft += 1
                dispo = math.sqrt((xpo - cLx) ** 2 + (ypo - cLy) ** 2)
                distancEachPoint.append(dispo)

        ts_instroke_mean.append(mean(ts_instroke))

    countinside = sum(map(lambda x: x < cRadius, distancEachPoint))
    countall = len(distancEachPoint)
    ppInsideToAll = countinside / countall if countall > 0 else 0

    try:
        if inLeft / inRight > 1:
            ppLeftToRight = inRight / inLeft
        else:
            ppLeftToRight = inLeft / inRight
    except ZeroDivisionError:
        ppLeftToRight = 0

    tDiff = [item1 - item2 for item1, item2 in zip(ts_instroke_mean[1:], ts_instroke_mean[:-1])]
    tDiff_mean = mean(tDiff) if tDiff else 0
    tDiff_max = max(tDiff) if tDiff else 0
    tDiff_min = min(tDiff) if tDiff else 0

    tap_points_list = [len(tap['data']) for tap in jf]
    maxTapPoints = np.max(tap_points_list) if tap_points_list else 0
    stdTapPoints = np.std(tap_points_list) if tap_points_list else 0
    meanTapPoints = np.mean(tap_points_list) if tap_points_list else 0
    tapCount = len(tap_points_list)

    features = {
        "Score": score,
        "Tap Count": tapCount,
        "Max Tap Points": maxTapPoints,
        "Std Tap Points": stdTapPoints,
        "Mean Tap Points": meanTapPoints,
        "Total Points": countall,
        "ppInsideToAll": ppInsideToAll,
        "ppLeftToRight": ppLeftToRight,
        "tDiff_mean": tDiff_mean,
        "tDiff_max": tDiff_max,
        "tDiff_min": tDiff_min
    }

    return features

# Route for the homepage
@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/')
def home():
    return "<h1>Welcome to god world 2</h1><p>xxxxxxxxx</p>"

# Route for the about page
@app.route('/about')
def about():
    return "<h1>About Page</h1><p>This is a simple Flask web app!</p>"


@app.route('/selftest', methods=['POST'])
def selftest_endpoint():
    """Replay the saved payload(s) and return per-endpoint pass/fail.

    Body / query: optional `endpoint` to test just one. Otherwise tests all.
    Self-test calls are excluded from chart counters and payload-capture
    (they carry the X-Selftest-Run header internally).
    """
    target = request.args.get('endpoint')
    if not target and request.is_json:
        target = (request.get_json(silent=True) or {}).get('endpoint')
    return jsonify(run_selftest(target))


@app.route('/saved_payloads', methods=['GET'])
def saved_payloads_endpoint():
    try:
        files = sorted(os.listdir(TEST_PAYLOADS_DIR))
    except Exception as e:
        return jsonify({"error": str(e), "files": []}), 500
    out = []
    for fn in files:
        full = os.path.join(TEST_PAYLOADS_DIR, fn)
        try:
            st = os.stat(full)
            out.append({
                "file": fn,
                "size_bytes": st.st_size,
                "mtime": int(st.st_mtime),
            })
        except Exception:
            out.append({"file": fn})
    return jsonify({"payloads": out})

# Route to receive JSON data and make predictions
@app.route('/predict_dualtap', methods=['POST'])
def predict_dualtap():
    global successful_request_count  # Use the global counter
    try:
        # send_text("App called: predict_dualtap")
        # send_telegram_message("App called: predict_dualtap")
        # Get JSON data from request
        data = request.get_json()

        # Extract features from the JSON data
        features = extract_tapcount_statistics(data)

        # Convert dictionary values to a flat list
        features_ = list(features.values())

        # Convert to a 2D NumPy array
        X_test = np.array(features_).reshape(1, -1)

        # Predict on the test set
        y_pred = model_dual.predict(X_test)

        # Return the prediction as a JSON response
        # response = {
        #     "prediction": int(y_pred[0])
        # }
        response = {
            "prediction": str(y_pred[0])
        }        
        # # Send a Telegram message every 10 successful requests
        # if successful_request_count % 10 == 0:
        #     send_telegram_message(f"Completed {successful_request_count} successful predictions.")

        # # Reset the counter after 1,000 successful requests
        # if successful_request_count >= 1000:
        #     send_telegram_message(f"Reached {successful_request_count} successful predictions. Resetting the counter.")
        #     successful_request_count = 0
                    
        return jsonify(response)

    except Exception as e:
        report_route_error('predict_dualtap', e)
        return jsonify({"error": str(e), "prediction": "2"})



# Define moving average function
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

# Function to process JSON data and extract features
def process_pinch_data(data):
    # Initialize variables and lists for calculations
    extracted_values = []
    CountAllHandOff = 0
    allSignSwitchCount = 0
    x_mts_start_stack = []
    x_mts_end_stack = []
    x_norm_std_stack = []
    x_norm_mean_stack = []
    x_mx1_std_stack = []
    x_mx1_mean_stack = []
    x_mx2_std_stack = []
    x_mx2_mean_stack = []
    x_my1_std_stack = []
    x_my1_mean_stack = []
    x_my2_std_stack = []
    x_my2_mean_stack = []

    # Check if 'data' exists in the JSON structure
    if 'data' in data:
        for indata in data['data']:
            if 'meta' in indata:  # If 'meta' exists, extract "target" and "absoluteTime"
                j_meta = indata['meta']

                # Initialize variables to store calculations
                mts, mx1, mx2, my1, my2, mdia = [], [], [], [], [], []

                # Check if 'data' key exists next to 'meta'
                if 'data' in indata:
                    j_indata = indata['data']

                    # Perform calculations based on the data
                    for k_injdata in j_indata:
                        CountAllHandOff += 1
                        for m_inkdata in k_injdata:
                            mts.append(m_inkdata['timestamp'])
                            mx1.append(m_inkdata['x1'])
                            mx2.append(m_inkdata['x2'])
                            my1.append(m_inkdata['y1'])
                            my2.append(m_inkdata['y2'])
                            mdia.append(m_inkdata['diameter'])

                    # Smoothing and sign-switch counting for mdia
                    mvWindow = 25
                    if len(mdia) > mvWindow + 1:
                        mav = moving_average(mdia, mvWindow)
                        signSwitchCount = 0
                        for idx, dat_ in enumerate(mav):
                            if idx == 0:
                                mvToRaw_a = (dat_ > mdia[idx])
                            else:
                                mvToRaw_b = (dat_ > mdia[idx])
                                if mvToRaw_b != mvToRaw_a:
                                    signSwitchCount += 1
                                    mvToRaw_a = mvToRaw_b
                        allSignSwitchCount += signSwitchCount

                    # Perform normalization and additional calculations
                    mts_start = mts[0]
                    mts_end = mts[-1]

                    mdia_ar = np.array(mdia)
                    if np.max(mdia_ar) != np.min(mdia_ar):
                        x_norm_ar = (mdia_ar - np.min(mdia_ar)) / (np.max(mdia_ar) - np.min(mdia_ar))
                    else:
                        x_norm_ar = np.zeros_like(mdia_ar)
                    x_norm_std = np.std(x_norm_ar)
                    x_norm_mean = np.mean(x_norm_ar)

                    x_mx1_std = np.std(mx1)
                    x_mx1_mean = np.mean(mx1)

                    x_mx2_std = np.std(mx2)
                    x_mx2_mean = np.mean(mx2)

                    x_my1_std = np.std(my1)
                    x_my1_mean = np.mean(my1)

                    x_my2_std = np.std(my2)
                    x_my2_mean = np.mean(my2)

                    # Append values to overall stacks
                    x_mts_start_stack.append(mts_start)
                    x_mts_end_stack.append(mts_end)

                    x_norm_std_stack.append(x_norm_std)
                    x_norm_mean_stack.append(x_norm_mean)

                    x_mx1_std_stack.append(x_mx1_std)
                    x_mx1_mean_stack.append(x_mx1_mean)

                    x_mx2_std_stack.append(x_mx2_std)
                    x_mx2_mean_stack.append(x_mx2_mean)

                    x_my1_std_stack.append(x_my1_std)
                    x_my1_mean_stack.append(x_my1_mean)

                    x_my2_std_stack.append(x_my2_std)
                    x_my2_mean_stack.append(x_my2_mean)

    # Final calculations
    mts_start_mean = np.mean(x_mts_start_stack)
    mts_start_max = np.max(x_mts_start_stack)
    mts_range_max = np.max(x_mts_end_stack)

    mdia_std = np.mean(x_norm_std_stack)
    mdia_mean = np.mean(x_norm_mean_stack)

    mx1_std = np.mean(x_mx1_std_stack)
    mx1_mean = np.mean(x_mx1_mean_stack)

    mx2_std = np.mean(x_mx2_std_stack)
    mx2_mean = np.mean(x_mx2_mean_stack)

    my1_std = np.mean(x_mx1_std_stack)
    my1_mean = np.mean(x_my1_mean_stack)

    my2_std = np.mean(x_my2_std_stack)
    my2_mean = np.mean(x_my2_mean_stack)

    # Collect the final metrics and return them as a dictionary
    features = {
        "mdia_std": mdia_std,
        "mdia_mean": mdia_mean,
        "mx1_std": mx1_std,
        "mx1_mean": mx1_mean,
        "mx2_std": mx2_std,
        "mx2_mean": mx2_mean,
        "my1_std": my1_std,
        "my1_mean": my1_mean,
        "my2_std": my2_std,
        "my2_mean": my2_mean,
        "CountAllHandOff": CountAllHandOff,
        "allSignSwitchCount": allSignSwitchCount,
        "mts_start_mean": mts_start_mean,
        "mts_range_max": mts_range_max,
        "mts_start_max": mts_start_max
    }
                
    return features

# Route for prediction
@app.route('/predict_pinchtosize', methods=['POST'])
def predict_pinchtosize():
    global successful_request_count  # Use the global counter
    try:
        # send_text("App called: predict_pinchtosize")
        # send_telegram_message("App called: predict_pinchtosize")
        # Get JSON data from request
        data = request.get_json()

        # Extract features from the JSON data
        features = process_pinch_data(data)

        # Convert dictionary values to a flat list
        features_ = list(features.values())

        # Convert to a 2D NumPy array
        X_test = np.array(features_).reshape(1, -1)

        # Predict on the test set
        y_pred = model_pinch.predict(X_test)

        # Return the prediction as a JSON response
        # response = {
        #     "prediction": int(y_pred[0])
        # }
        response = {
            "prediction": str(y_pred[0])
        }  
        # Send a Telegram message every 10 successful requests
        # if successful_request_count % 10 == 0:
        #     send_telegram_message(f"Completed {successful_request_count} successful predictions.")

        # # Reset the counter after 1,000 successful requests
        # if successful_request_count >= 1000:
        #     send_telegram_message(f"Reached {successful_request_count} successful predictions. Resetting the counter.")
        #     successful_request_count = 0

        return jsonify(response)

    except Exception as e:
        report_route_error('predict_pinchtosize', e)
        return jsonify({"error": str(e), "prediction": "2"})

# Sampling rate (10 Hz)
sampling_rate = 10.0
nyquist_freq = sampling_rate / 2.0
cutoff_freq = 0.12
normalized_cutoff = cutoff_freq / nyquist_freq
sos = signal.butter(10, normalized_cutoff, btype='highpass', output='sos')

# Function to extract features from motion data
def extract_features(signal_data):
    filtered = signal.sosfilt(sos, signal_data)
    N = len(filtered)
    fft_values = fft(filtered)
    fft_freq = fftfreq(N, 1 / sampling_rate)
    magnitude = np.abs(fft_values)
    peak_frequency = fft_freq[np.argmax(magnitude[:N // 2])]

    fab = np.abs(fft_values[:N // 2])
    F1, F2, F3, F4 = sum(np.square(fab[:25])), sum(np.square(fab[25:50])), sum(np.square(fab[50:75])), sum(np.square(fab[75:]))
    Esum = sum(np.square(fab))
    kur, ske = kurtosis(filtered, fisher=True), skew(filtered, bias=False)
    resdif, resdif2 = np.diff(filtered), np.diff(np.diff(filtered))
    Mobi = np.sqrt(np.var(resdif) / np.var(filtered))
    compx = np.sqrt(np.var(resdif2) * np.var(filtered) / (np.var(resdif) * np.var(resdif)))
    Samp, _, _ = EH.SampEn(filtered, m=2, tau=2)
    E13, E14, E15 = np.percentile(filtered, [25, 50, 75])

    return [
        np.std(filtered), np.mean(filtered), kur, ske, Mobi, compx,
        F1, F2, F3, F4, F2 / Esum, F3 / Esum, np.var(resdif2),
        Samp[0], Samp[1], Samp[2], E13, E14, E15, peak_frequency
    ]

# Function to process motion data from JSON input
def process_motion_data(data):
    tStamp, acX, acY, acZ, agX, agY, agZ = [], [], [], [], [], [], []
    for i in data['recording']['recordedData']:
        tStamp.append(i['ts'])
        acX.append(i['data'][0])
        acY.append(i['data'][1])
        acZ.append(i['data'][2])
        agX.append(i['data'][3])
        agY.append(i['data'][4])
        agZ.append(i['data'][5])

    downsample_factor = 4
    if len(acX) >= downsample_factor:
        tStamp = signal.decimate(tStamp, downsample_factor, zero_phase=True)
        acX = signal.decimate(acX, downsample_factor, zero_phase=True)
        acY = signal.decimate(acY, downsample_factor, zero_phase=True)
        acZ = signal.decimate(acZ, downsample_factor, zero_phase=True)
        agX = signal.decimate(agX, downsample_factor, zero_phase=True)
        agY = signal.decimate(agY, downsample_factor, zero_phase=True)
        agZ = signal.decimate(agZ, downsample_factor, zero_phase=True)

    features_acX = extract_features(acX)
    features_acY = extract_features(acY)
    features_acZ = extract_features(acZ)
    features_agX = extract_features(agX)
    features_agY = extract_features(agY)
    features_agZ = extract_features(agZ)

    all_features = features_acX + features_acY + features_acZ + features_agX + features_agY + features_agZ

    return all_features

# Flask endpoint to receive JSON and return prediction
@app.route('/predict_tremor_rest', methods=['POST'])
@app.route('/predict_tremor_post', methods=['POST'])
@app.route('/predict_gait_stab', methods=['POST'])
@app.route('/predict_gait_walk', methods=['POST'])
def predict_tremor():
    global successful_request_count  # Use the global counter
    try:
        # send_text("App called: predict_tremor")
        # send_telegram_message("App called: predict_tremor")
        # Get JSON data from the request
        data = request.get_json()

        # Extract features from the JSON data
        features = process_motion_data(data)

        if not features:
            return jsonify({"error": "No features extracted from data"}), 400

        # Convert to a 2D NumPy array
        X_test = np.array(features).reshape(1, -1)

        # Select the model based on the endpoint
        if request.path == '/predict_tremor_rest':
            y_pred = model_tremor_resthand.predict(X_test)
        elif request.path == '/predict_tremor_post':
            y_pred = model_tremor_posthand.predict(X_test)
        elif request.path == '/predict_gait_stab':
            y_pred = model_tremor_stabi.predict(X_test)
        elif request.path == '/predict_gait_walk':
            y_pred = model_tremor_walk.predict(X_test)            
        else:
            return jsonify({"error": "Unknown endpoint"}), 400

        # # Predict using the model
        # y_pred = model_tremor_resthand.predict(X_test)

        # Create response
        # response = {
        #     "prediction": int(y_pred[0])
        # }
        response = {
            "prediction": str(y_pred[0])
        }        
        # Send a Telegram message every 10 successful requests
        # if successful_request_count % 10 == 0:
        #     send_telegram_message(f"Completed {successful_request_count} successful predictions.")

        # # Reset the counter after 1,000 successful requests
        # if successful_request_count >= 1000:
        #     send_telegram_message(f"Reached {successful_request_count} successful predictions. Resetting the counter.")
        #     successful_request_count = 0
        return jsonify(response)

    except Exception as e:
        report_route_error(request.path.lstrip('/') or 'predict_tremor', e)
        return jsonify({"error": str(e), "prediction": "2"})


# Function to decode base64 to WAV
def decode_base64_to_wav(base64_string, output_file):
    audio_data = base64.b64decode(base64_string)
    with open(output_file, 'wb') as wav_file:
        wav_file.write(audio_data)

# Function to measure pitch using Praat
def measurePitch(wav_file, f0min, f0max, unit):
    sound = parselmouth.Sound(wav_file)
    duration = call(sound, "Get total duration")
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    meanF0 = call(pitch, "Get mean", 0, 0, unit)
    stdevF0 = call(pitch, "Get standard deviation", 0, 0, unit)
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return [
        duration, meanF0, stdevF0, hnr, localJitter, localabsoluteJitter, 
        rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, 
        apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer
    ]

# Function to measure formants using Praat
def measureFormants(wav_file, f0min, f0max):
    sound = parselmouth.Sound(wav_file)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list, f2_list, f3_list, f4_list = [], [], [], []

    for point in range(numPoints):
        t = call(pointProcess, "Get time from index", point + 1)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)

    f1_median = statistics.median([f for f in f1_list if not np.isnan(f)])
    f2_median = statistics.median([f for f in f2_list if not np.isnan(f)])
    f3_median = statistics.median([f for f in f3_list if not np.isnan(f)])
    f4_median = statistics.median([f for f in f4_list if not np.isnan(f)])

    f1_mean = statistics.mean([f for f in f1_list if not np.isnan(f)])
    f2_mean = statistics.mean([f for f in f2_list if not np.isnan(f)])
    f3_mean = statistics.mean([f for f in f3_list if not np.isnan(f)])
    f4_mean = statistics.mean([f for f in f4_list if not np.isnan(f)])

    return [f1_median, f2_median, f3_median, f4_median, f1_mean, f2_mean, f3_mean, f4_mean]

# Function to calculate additional features from formants
def calculate_additional_features(f1_median, f2_median, f3_median, f4_median):
    formants = [f1_median, f2_median, f3_median, f4_median]
    formants_zscore = zscore(formants) if None not in formants else [None] * 4

    pF = sum(formants_zscore) / 4 if None not in formants_zscore else None
    fdisp = (f4_median - f1_median) / 3 if f1_median and f4_median else None
    avgFormant = sum(formants) / 4 if None not in formants else None
    mff = (f1_median * f2_median * f3_median * f4_median) ** 0.25 if None not in formants else None

    fitch_vtl = ((1 * (35000 / (4 * f1_median))) +
                 (3 * (35000 / (4 * f2_median))) +
                 (5 * (35000 / (4 * f3_median))) +
                 (7 * (35000 / (4 * f4_median)))) / 4 if None not in formants else None

    xysum = (0.5 * f1_median) + (1.5 * f2_median) + (2.5 * f3_median) + (3.5 * f4_median) if None not in formants else None
    xsquaredsum = (0.5 ** 2) + (1.5 ** 2) + (2.5 ** 2) + (3.5 ** 2)
    delta_f = xysum / xsquaredsum if xysum else None
    vtl_delta_f = 35000 / (2 * delta_f) if delta_f else None

    return [pF, fdisp, avgFormant, mff, fitch_vtl, delta_f, vtl_delta_f, xysum]

@app.route('/predict_voice_ahh', methods=['POST'])
@app.route('/predict_voice_ypl', methods=['POST'])
def predict_voice():
    global successful_request_count  # Use the global counter
    # Generate a unique temporary file name
    temp_wav_file = f"temp_decoded_{uuid.uuid4()}.wav"

    try:
        # send_text("App called: predict_voice")
        # send_telegram_message("App called: predict_voice")
        # Get JSON data from the request
        data = request.get_json()

        # Extract base64 string from the 'data' key
        if 'data' not in data:
            return jsonify({"error": "No 'data' key found in request"}), 400

        base64_audio = data['data']

        # Decode base64 string and save as temporary WAV file
        decode_base64_to_wav(base64_audio, temp_wav_file)

        # Measure pitch and formants from the WAV file
        pitch_features = measurePitch(temp_wav_file, f0min=75, f0max=300, unit="Hertz")

        # Measure formants
        formant_medians_means = measureFormants(temp_wav_file, f0min=75, f0max=300)

        # Split formant medians and means
        formant_medians = formant_medians_means[:4]
        formant_means = formant_medians_means[4:]

        # Calculate additional features
        additional_features = calculate_additional_features(*formant_medians)

        # Merge all extracted features into a single list
        all_features = pitch_features + formant_medians + formant_means + additional_features

        # Prepare features for model prediction
        X_test = np.array(all_features[1:]).reshape(1, -1)  # Exclude "Duration" for model input

        # Select the model based on the endpoint
        if request.path == '/predict_voice_ahh':
            y_pred = model_voice_AHH.predict(X_test)
        elif request.path == '/predict_voice_ypl':
            y_pred = model_voice_YPL.predict(X_test)
        else:
            return jsonify({"error": "Unknown endpoint"}), 400

        # Create response with the prediction
        # response = {
        #     "prediction": int(y_pred[0]),
        # }
        response = {
            "prediction": str(y_pred[0]),
        }
        # Increment successful request counter
        successful_request_count += 1

        # Send a Telegram message every 10 successful requests
        # if successful_request_count % 10 == 0:
        #     send_telegram_message(f"Completed {successful_request_count} successful predictions.")

        # # Reset the counter after 1,000 successful requests
        # if successful_request_count >= 1000:
        #     send_telegram_message(f"Reached {successful_request_count} successful predictions. Resetting the counter.")
        #     successful_request_count = 0

        return jsonify(response)

    except Exception as e:
        report_route_error(request.path.lstrip('/') or 'predict_voice', e)
        return jsonify({"error": str(e), "prediction": "2"})
    finally:
        # Ensure the temporary WAV file is deleted after processing
        if os.path.exists(temp_wav_file):
            os.remove(temp_wav_file)




# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
import librosa
import soundfile as sf

def convert_mp3_to_wav(mp3_path, wav_path):
    """
    Converts an MP3 file to a WAV file using librosa and soundfile.

    Parameters:
    mp3_path (str): The path to the input MP3 file.
    wav_path (str): The path to the output WAV file.
    """
    # Load the MP3 file as a numpy array
    audio, sr = librosa.load(mp3_path, sr=None)
    
    # Save the audio as a WAV file
    sf.write(wav_path, audio, sr, format='WAV')




@app.route('/predict_voice_ahh_mp3', methods=['POST'])
@app.route('/predict_voice_ypl_mp3', methods=['POST'])
def predict_voice_mp3():
    temp_folder = None
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        temp_folder = f"temp_files_{uuid.uuid4()}"
        os.makedirs(temp_folder, exist_ok=True)

        mp3_path = os.path.join(temp_folder, "uploaded.mp3")
        file.save(mp3_path)

        temp_wav_file = os.path.join(temp_folder, f"temp_decoded_{uuid.uuid4()}.wav")

        convert_mp3_to_wav(mp3_path, temp_wav_file)

        pitch_features = measurePitch(temp_wav_file, f0min=75, f0max=300, unit="Hertz")
        formant_medians_means = measureFormants(temp_wav_file, f0min=75, f0max=300)
        formant_medians = formant_medians_means[:4]
        formant_means = formant_medians_means[4:]
        additional_features = calculate_additional_features(*formant_medians)
        all_features = pitch_features + formant_medians + formant_means + additional_features

        X_test = np.array(all_features[1:]).reshape(1, -1)

        if request.path == '/predict_voice_ahh_mp3':
            y_pred = model_voice_AHH.predict(X_test)
        elif request.path == '/predict_voice_ypl_mp3':
            y_pred = model_voice_YPL.predict(X_test)
        else:
            return jsonify({"error": "Unknown endpoint"}), 400

        # Save the uploaded MP3 as the latest payload for self-test replay
        # (only on success; skip during self-test runs to avoid recursion).
        if request.headers.get(SELFTEST_HEADER) != '1':
            try:
                with open(mp3_path, 'rb') as _f:
                    _save_test_payload(request.path.lstrip('/'), 'file', _f.read())
            except Exception:
                pass

        return jsonify({"prediction": str(y_pred[0])})

    except Exception as e:
        report_route_error(request.path.lstrip('/') or 'predict_voice_mp3', e)
        return jsonify({"error": str(e), "prediction": "2"}), 400
    finally:
        # Always clean up — on success AND on every error path. Otherwise
        # temp_files_* folders accumulate forever and eventually fill the disk.
        if temp_folder and os.path.isdir(temp_folder):
            import shutil
            try:
                shutil.rmtree(temp_folder, ignore_errors=True)
            except Exception:
                pass
    
    

@app.route('/predict_voting', methods=['POST'])
def predict_voting():
    try:
        # send_text("App called: predict_voting")
        # send_telegram_message("App called: predict_voting")
        if request.is_json:
            req = request.get_json()

            # Read 'test_result' from the request and split into a list of integers
            test_result = [int(item) for item in req['test_result'].split(',')]

            # Check if the first element is '1'
            if test_result[0] == 1:
                return jsonify({"prediction": "1"})

            # Exclude -1 from test_result
            filtered_result = [item for item in test_result if item != -1]

            # Count the number of 0s and 1s in the filtered list
            count_0 = filtered_result.count(0)
            count_1 = filtered_result.count(1)

            # Compare counts and set prediction
            if count_0 >= count_1:
                prediction = "0"
            else:
                prediction = "1"

            # Return the response with the prediction
            return jsonify({"prediction": prediction})

    except Exception as e:
        report_route_error('predict_voting', e)
        return jsonify({"error": str(e), "prediction": "2"})


# Running the app
if __name__ == '__main__':
    start_background_schedulers()
    app.run(debug=False)
