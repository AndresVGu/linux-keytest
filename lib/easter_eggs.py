"""Easter eggs: Konami Code and 100% rainbow celebration."""

from lib.renderer import set_key_color

# Konami: Up Up Down Down Left Right Left Right b a
KONAMI_SEQ = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "b", "a"]

RAINBOW = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#e91e63"]


class KonamiTracker:
    """Tracks key sequence and triggers on Konami Code match."""

    def __init__(self):
        self._buffer = []

    def feed(self, keysym):
        self._buffer.append(keysym)
        if len(self._buffer) > len(KONAMI_SEQ):
            self._buffer.pop(0)
        return self._buffer == KONAMI_SEQ

    def reset(self):
        self._buffer.clear()


def rainbow_wave(app, on_done=None):
    """Animate a rainbow color wave across all keys, then restore."""
    keysyms = [ks for ks in app.key_widgets if not (len(ks) == 1 and ks.isupper())]
    total = len(keysyms)
    if total == 0:
        if on_done:
            on_done()
        return

    step_ms = max(15, 1500 // total)
    _wave_step(app, keysyms, 0, step_ms, on_done)


def _wave_step(app, keysyms, idx, step_ms, on_done):
    if idx >= len(keysyms):
        # Restore all keys after a short pause
        app.master.after(400, lambda: _restore_all(app, on_done))
        return

    ks = keysyms[idx]
    color = RAINBOW[idx % len(RAINBOW)]
    set_key_color(app, ks, color, "#ffffff")

    app.master.after(step_ms, lambda: _wave_step(app, keysyms, idx + 1, step_ms, on_done))


def _restore_all(app, on_done):
    from lib.renderer import key_bg, key_fg
    for ks in app.key_widgets:
        if len(ks) == 1 and ks.isupper():
            continue
        set_key_color(app, ks, key_bg(app, ks), key_fg(app, ks))
    if on_done:
        on_done()


def konami_wave(app):
    """Trigger the Konami Code celebration."""
    app.latency_list.insert(0, " [🎮] Nice!")
    app.latency_list.itemconfig(0, fg=RAINBOW[4])
    rainbow_wave(app)
