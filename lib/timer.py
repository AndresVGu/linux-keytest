"""Session timer, lock polling, and sound feedback."""

import subprocess
import time


# ── Session Timer ──

def start_timer(app):
    app.timer_start = time.monotonic()
    app.timer_running = True
    _tick(app)


def stop_timer(app):
    app.timer_running = False
    app.timer_start = None
    if app.timer_job:
        app.master.after_cancel(app.timer_job)
        app.timer_job = None
    app.timer_label.config(text="00:00", fg=app.theme["text"])


def _tick(app):
    if not app.timer_running:
        return
    elapsed = int(time.monotonic() - app.timer_start)
    mins, secs = divmod(elapsed, 60)
    app.timer_label.config(text=f"{mins:02d}:{secs:02d}")
    app.timer_job = app.master.after(1000, lambda: _tick(app))


# ── Sound Feedback ──

def beep():
    try:
        subprocess.Popen(
            ["paplay", "/usr/share/sounds/freedesktop/stereo/key-press-click.oga"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


# ── Caps Lock / Num Lock Indicator ──

def start_lock_poll(app):
    _poll(app)


def _poll(app):
    try:
        result = subprocess.run(
            ["xset", "q"], capture_output=True, text=True, timeout=2,
        )
        caps = "ON" if "Caps Lock:   on" in result.stdout else "OFF"
        num = "ON" if "Num Lock:    on" in result.stdout else "OFF"
        app.lock_label.config(text=f"Caps:{caps}  Num:{num}")
    except Exception:
        app.lock_label.config(text="")
    app.master.after(500, lambda: _poll(app))
