"""Session timer, lock polling, sound feedback, and next-key highlight."""

import subprocess
import time

from lib.layouts import get_all_keysyms
from lib.renderer import set_key_color


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


# ── Next Key Highlight ──

def start_highlight_blink(app):
    _blink(app)


def _blink(app):
    active_keys = app._get_active_keysyms()
    next_ks = None
    for ks in active_keys:
        if ks not in app.pressed_keys:
            next_ks = ks
            break

    # Restore previous
    prev = app.highlight_keysym
    if prev and prev != next_ks:
        if prev in app.key_widgets and prev not in app.pressed_keys:
            set_key_color(app, prev, app.theme["key_bg"], app.theme["key_fg"])

    app.highlight_keysym = next_ks

    if next_ks and next_ks in app.key_widgets and next_ks not in app.pressed_keys:
        app.highlight_visible = not app.highlight_visible
        t = app.theme
        if app.highlight_visible:
            set_key_color(app, next_ks, t["accent"], t["btn_fg"])
        else:
            set_key_color(app, next_ks, t["key_bg"], t["key_fg"])

    app.highlight_job = app.master.after(app.BLINK_MS, lambda: _blink(app))


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
