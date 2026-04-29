#!/usr/bin/env python3
"""
Keyboard Tester — Modern UI for QA keyboard validation.
Supports Canadian English, Canadian French, and Spanish (Latin America).
Author: Andres V. a.k.a. @4vs3c
"""

import tkinter as tk
from datetime import datetime
import atexit

from lib.themes import LIGHT, DARK
from lib.layouts import LAYOUTS, NUMPAD, get_all_keysyms, detect_system_layout
from lib.grabber import GnomeKeyGrabber
from lib.combos import COMBOS
from lib.config import load_config
from lib import ui, renderer, timer, validator
from lib.easter_eggs import KonamiTracker, konami_wave, rainbow_wave
from lib.seasonal import get_active_season, get_season_footer, draw_decorations


class KeyboardTester:

    UNIT = 48
    KEY_PAD = 3
    KEY_H = 42
    FONT = ("Segoe UI", 9, "bold")
    FONT_SM = ("Segoe UI", 7)
    FONT_TITLE = ("Segoe UI", 18, "bold")
    FONT_SUB = ("Segoe UI", 9)
    FONT_MONO = ("Consolas", 10)

    def __init__(self, master):
        self.master = master
        master.title("Keyboard Tester")
        master.minsize(1280, 720)

        self.cfg = load_config()
        self.theme = LIGHT
        self.is_dark = False

        # Key state
        self.key_press_times = {}
        self.pressed_keys = set()
        self.stuck_keys = set()
        self.ghost_keys = set()
        self.key_widgets = {}
        self.canvas_keys = {}
        self.flash_jobs = {}
        self.stuck_jobs = {}
        self.latencies = []
        self.held_keys = set()

        # Defect tracking
        self.key_press_count = {}
        self.repeat_events = {}
        self.bounce_keys = set()
        self.BOUNCE_THRESHOLD = self.cfg["bounce_threshold"]
        self.FLASH_MS = self.cfg["flash_duration_ms"]
        self.STUCK_MS = self.cfg["stuck_timeout_ms"]

        # Modes
        self.combo_mode = False
        self.tested_combos = set()
        self.numpad_enabled = False
        self.sound_enabled = self.cfg["sound_enabled"]
        self.validated = False

        # Timer
        self.timer_start = None
        self.timer_running = False
        self.timer_job = None

        # Easter eggs
        self.konami = KonamiTracker()
        self._celebration_done = False

        # Seasonal
        self.season = get_active_season()

        # Layout
        self.layouts = LAYOUTS
        detected = detect_system_layout()
        self.current_layout = detected if self.cfg["default_layout"] == "auto" else self.cfg.get("default_layout", detected)

        # System key grab
        self.grabber = GnomeKeyGrabber()
        self.grabber.grab()

        # Build and start
        ui.build_ui(self)
        ui.apply_theme(self)
        renderer.draw_keyboard(self)
        validator.update_progress(self)
        timer.start_lock_poll(self)

        master.bind("<KeyPress>", self._on_key_press)
        master.bind("<KeyRelease>", self._on_key_release)
        master.bind("<FocusIn>", lambda e: master.focus_set())
        master.protocol("WM_DELETE_WINDOW", self._on_close)
        atexit.register(self.grabber.release)

    # ── Layout helpers ──

    def _get_active_layout(self):
        rows = list(self.layouts[self.current_layout])
        if self.numpad_enabled:
            rows = rows + NUMPAD
        return rows

    def _get_active_keysyms(self):
        return get_all_keysyms(self._get_active_layout())

    # ── Key events ──

    def _on_key_press(self, event):
        ks = event.keysym
        now = datetime.now()
        self.held_keys.add(ks)

        # Konami Code check
        if self.konami.feed(ks):
            konami_wave(self)
            self.konami.reset()

        self.key_press_count[ks] = self.key_press_count.get(ks, 0) + 1

        if ks in self.key_press_times:
            if ks not in self.repeat_events:
                self.repeat_events[ks] = []
            self.repeat_events[ks].append(now)
        else:
            self.key_press_times[ks] = now
            self.repeat_events.pop(ks, None)

        if not self.timer_running:
            timer.start_timer(self)

        if self.sound_enabled:
            timer.beep()

        if self.combo_mode:
            self._check_combos()

        if ks not in self.key_widgets:
            self.ghost_keys.add(ks)
            self.latency_list.insert(0, f" [GHOST] {ks}")
            self.latency_list.itemconfig(0, fg=self.theme["ghost"])
            validator.update_progress(self)
            return

        renderer.set_key_color(self, ks, self.theme["key_active"], self.theme["key_active_fg"])

        if ks in self.stuck_jobs:
            self.master.after_cancel(self.stuck_jobs[ks])
        self.stuck_jobs[ks] = self.master.after(self.STUCK_MS, lambda k=ks: self._mark_stuck(k))

    def _on_key_release(self, event):
        ks = event.keysym
        self.held_keys.discard(ks)

        if ks in self.stuck_jobs:
            self.master.after_cancel(self.stuck_jobs.pop(ks))

        if ks in self.key_press_times:
            dt = (datetime.now() - self.key_press_times.pop(ks)).total_seconds() * 1000
            self.latencies.append(dt)
            count = self.key_press_count.get(ks, 1)
            tag = f" x{count}" if count > 1 else ""
            self.latency_list.insert(0, f" {ks:<14} {dt:7.1f} ms{tag}")

        if ks in self.repeat_events and len(self.repeat_events[ks]) >= 3:
            events = self.repeat_events[ks]
            duration = (events[-1] - events[0]).total_seconds()
            if duration > 0:
                rate = len(events) / duration
                if rate > self.BOUNCE_THRESHOLD and ks not in self.bounce_keys:
                    self.bounce_keys.add(ks)
                    self.latency_list.insert(0, f" [BOUNCE] {ks} {rate:.0f}r/s")
                    self.latency_list.itemconfig(0, fg=self.theme["ghost"])
        self.repeat_events.pop(ks, None)

        if ks in self.key_widgets:
            if ks in self.stuck_keys:
                self.stuck_keys.discard(ks)
            self.pressed_keys.add(ks)
            if ks in self.flash_jobs:
                self.master.after_cancel(self.flash_jobs[ks])
            self.flash_jobs[ks] = self.master.after(
                self.FLASH_MS, lambda k=ks: renderer.set_key_tested(self, k),
            )
            validator.update_progress(self)

            # 100% celebration (once)
            if not self._celebration_done:
                all_keys = set(self._get_active_keysyms())
                if all_keys.issubset(self.pressed_keys):
                    self._celebration_done = True
                    self.latency_list.insert(0, " [🎉] 100% — All keys tested!")
                    self.latency_list.itemconfig(0, fg="#2ecc71")
                    rainbow_wave(self)

    def _mark_stuck(self, keysym):
        if keysym in self.key_press_times:
            self.stuck_keys.add(keysym)
            renderer.set_key_color(self, keysym, self.theme["key_stuck"], self.theme["key_stuck_fg"])

    # ── Actions (called by UI buttons) ──

    def _on_layout_change(self, event):
        new = self.layout_var.get()
        if new != self.current_layout:
            self.current_layout = new
            renderer.draw_keyboard(self)
            validator.update_progress(self)

    def _reset(self):
        validator.reset(self)
        self.konami.reset()
        self._celebration_done = False
        renderer.draw_keyboard(self)
        validator.update_progress(self)
        validator.update_validate_btn(self)
        if self.combo_mode:
            self._draw_combo_list()

    def _export(self):
        validator.do_export(self)

    def _validate(self):
        validator.validate(self)

    def _toggle_theme(self):
        self.is_dark = not self.is_dark
        self.theme = DARK if self.is_dark else LIGHT
        ui.apply_theme(self)
        renderer.draw_keyboard(self)
        validator.update_progress(self)

    def _toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self._update_sound_btn()

    def _update_sound_btn(self):
        t = self.theme
        if self.sound_enabled:
            self.sound_btn.config(text="  Sound: ON  ", bg=t["accent"], fg=t["btn_fg"])
        else:
            self.sound_btn.config(text="  Sound: OFF  ", bg=t["key_border"], fg=t["text_dim"])

    def _toggle_numpad(self):
        self.numpad_enabled = not self.numpad_enabled
        self._update_numpad_btn()
        renderer.draw_keyboard(self)
        validator.update_progress(self)

    def _update_numpad_btn(self):
        t = self.theme
        if self.numpad_enabled:
            self.numpad_btn.config(text="  Numpad: ON  ", bg=t["accent"], fg=t["btn_fg"])
        else:
            self.numpad_btn.config(text="  Numpad: OFF  ", bg=t["key_border"], fg=t["text_dim"])

    def _update_validate_btn(self):
        validator.update_validate_btn(self)

    def _on_close(self):
        self.grabber.release()
        self.master.destroy()

    # ── Combo Test ──

    def _toggle_combo_mode(self):
        self.combo_mode = not self.combo_mode
        if self.combo_mode:
            self.combo_btn.config(text="  Keys Mode  ")
            self.combo_frame.pack(padx=8, pady=(0, 8), fill="x")
            self._draw_combo_list()
        else:
            self.combo_btn.config(text="  Combo Test  ")
            self.combo_frame.pack_forget()

    def _draw_combo_list(self):
        for w in self.combo_items:
            w.destroy()
        self.combo_items.clear()

        import tkinter as _tk
        t = self.theme
        for mod, key, label in COMBOS:
            passed = (mod, key) in self.tested_combos
            fg = t["combo_pass"] if passed else t["combo_pending_fg"]
            prefix = "[+]" if passed else "[ ]"
            lbl = _tk.Label(
                self.combo_frame, text=f"{prefix} {label}",
                font=self.FONT_SM, fg=fg, bg=t["bg_secondary"], anchor="w",
            )
            lbl.pack(fill="x", padx=4, pady=1)
            self.combo_items.append(lbl)

    def _check_combos(self):
        changed = False
        for mod, key, label in COMBOS:
            if (mod, key) in self.tested_combos:
                continue
            if mod in self.held_keys and key in self.held_keys:
                self.tested_combos.add((mod, key))
                self.latency_list.insert(0, f" [COMBO] {label}")
                self.latency_list.itemconfig(0, fg=self.theme["combo_pass"])
                changed = True
        if changed:
            self._draw_combo_list()


if __name__ == "__main__":
    root = tk.Tk()
    KeyboardTester(root)
    root.mainloop()
