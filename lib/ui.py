"""UI construction and theme application."""

import tkinter as tk
from tkinter import ttk
from lib.seasonal import get_season_footer


def build_ui(app):
    """Build all UI widgets and store references on the app instance."""
    m = app.master

    # Header
    app.header = tk.Frame(m)
    app.header.pack(fill="x", padx=30, pady=(18, 4))

    app.title_label = tk.Label(app.header, text="Keyboard Tester", font=app.FONT_TITLE)
    app.title_label.pack(side="left")

    app.subtitle_label = tk.Label(app.header, text="QA Hardware Validation", font=app.FONT_SUB)
    app.subtitle_label.pack(side="left", padx=(12, 0), pady=(8, 0))

    # Controls
    app.ctrl = tk.Frame(m)
    app.ctrl.pack(fill="x", padx=30, pady=(4, 4))

    app.layout_lbl = tk.Label(app.ctrl, text="Layout:", font=app.FONT_SM)
    app.layout_lbl.pack(side="left")

    app.layout_var = tk.StringVar(value=app.current_layout)
    app.layout_combo = ttk.Combobox(
        app.ctrl, textvariable=app.layout_var,
        values=list(app.layouts.keys()), state="readonly", width=25,
    )
    app.layout_combo.pack(side="left", padx=(6, 15))
    app.layout_combo.bind("<<ComboboxSelected>>", app._on_layout_change)

    for text, cmd in [("Reset", app._reset), ("Export Report", app._export)]:
        btn = tk.Label(app.ctrl, text=f"  {text}  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
        btn.pack(side="left", padx=4)
        btn.bind("<Button-1>", lambda e, c=cmd: c())
        btn._is_btn = True

    app.combo_btn = tk.Label(app.ctrl, text="  Combo Test  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
    app.combo_btn.pack(side="left", padx=4)
    app.combo_btn.bind("<Button-1>", lambda e: app._toggle_combo_mode())
    app.combo_btn._is_btn = True

    app.theme_btn = tk.Label(app.ctrl, text="  Dark Mode  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
    app.theme_btn.pack(side="left", padx=4)
    app.theme_btn.bind("<Button-1>", lambda e: app._toggle_theme())
    app.theme_btn._is_btn = True

    app.validate_btn = tk.Label(app.ctrl, text="  Validate  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
    app.validate_btn.pack(side="left", padx=4)
    app.validate_btn.bind("<Button-1>", lambda e: app._validate())
    app.validate_btn._is_btn = True

    app.sound_btn = tk.Label(app.ctrl, text="  Sound: ON  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
    app.sound_btn.pack(side="left", padx=4)
    app.sound_btn.bind("<Button-1>", lambda e: app._toggle_sound())
    app.sound_btn._is_btn = True

    app.numpad_btn = tk.Label(app.ctrl, text="  Numpad: OFF  ", font=app.FONT, cursor="hand2", padx=12, pady=4)
    app.numpad_btn.pack(side="left", padx=4)
    app.numpad_btn.bind("<Button-1>", lambda e: app._toggle_numpad())
    app.numpad_btn._is_btn = True

    app.lock_label = tk.Label(app.ctrl, text="", font=app.FONT_SM)
    app.lock_label.pack(side="right", padx=(0, 6))

    app.timer_label = tk.Label(app.ctrl, text="00:00", font=("Consolas", 12, "bold"))
    app.timer_label.pack(side="right", padx=(10, 20))

    app.total_label = tk.Label(app.ctrl, text="", font=app.FONT_SM)
    app.total_label.pack(side="right", padx=10)

    # Progress bar
    app.progress_frame = tk.Frame(m)
    app.progress_frame.pack(fill="x", padx=30, pady=(0, 8))

    app.progress_canvas = tk.Canvas(app.progress_frame, height=18, highlightthickness=0)
    app.progress_canvas.pack(fill="x")

    # Content
    app.content = tk.Frame(m)
    app.content.pack(fill="both", expand=True, padx=30, pady=(0, 8))

    # Keyboard
    app.kb_outer = tk.Frame(app.content, highlightthickness=1)
    app.kb_outer.pack(side="left", fill="both", expand=True, padx=(0, 10))

    app.canvas = tk.Canvas(app.kb_outer, highlightthickness=0, borderwidth=0)
    app.canvas.pack(fill="both", expand=True, padx=8, pady=8)

    # Right panel
    app.right_panel = tk.Frame(app.content, highlightthickness=1, width=260)
    app.right_panel.pack(side="right", fill="y")
    app.right_panel.pack_propagate(False)

    # Latency log
    app.lat_title = tk.Label(app.right_panel, text="Latency Log", font=app.FONT)
    app.lat_title.pack(pady=(10, 5))

    list_container = tk.Frame(app.right_panel)
    list_container.pack(fill="both", expand=True, padx=8, pady=(0, 4))

    app.latency_list = tk.Listbox(
        list_container, font=app.FONT_MONO, width=28,
        borderwidth=0, highlightthickness=0, relief="flat",
    )
    app.latency_list.pack(side="left", fill="both", expand=True)

    app.scrollbar = tk.Scrollbar(list_container, orient="vertical", command=app.latency_list.yview)
    app.scrollbar.pack(side="right", fill="y")
    app.latency_list.config(yscrollcommand=app.scrollbar.set)

    # Missing keys
    app.missing_title = tk.Label(app.right_panel, text="Missing Keys", font=app.FONT)
    app.missing_title.pack(pady=(6, 2))

    app.missing_label = tk.Label(app.right_panel, text="", font=app.FONT_SM, wraplength=240, justify="left")
    app.missing_label.pack(padx=8, pady=(0, 4), anchor="w")

    # Ghost keys
    app.ghost_title = tk.Label(app.right_panel, text="Ghost Keys", font=app.FONT)
    app.ghost_title.pack(pady=(4, 2))

    app.ghost_label = tk.Label(app.right_panel, text="None", font=app.FONT_SM, wraplength=240, justify="left")
    app.ghost_label.pack(padx=8, pady=(0, 4), anchor="w")

    # Combo panel (hidden)
    app.combo_frame = tk.Frame(app.right_panel)
    app.combo_title = tk.Label(app.combo_frame, text="Combo Test", font=app.FONT)
    app.combo_title.pack(pady=(4, 2))
    app.combo_items = []

    # Footer
    season_msg = get_season_footer(getattr(app, 'season', None))
    footer_text = f"By Andres V. (@4vs3c)  {season_msg}" if season_msg else "By Andres V. (@4vs3c)"
    app.footer_label = tk.Label(m, text=footer_text, font=app.FONT_SM)
    app.footer_label.pack(side="bottom", pady=(0, 8))


def apply_theme(app):
    """Apply the current theme colors to all widgets."""
    t = app.theme

    for w in (app.master, app.header, app.ctrl, app.content, app.progress_frame):
        w.configure(bg=t["bg"])

    app.title_label.config(fg=t["accent"], bg=t["bg"])
    app.subtitle_label.config(fg=t["text_dim"], bg=t["bg"])
    app.layout_lbl.config(fg=t["text"], bg=t["bg"])
    app.total_label.config(fg=t["text_dim"], bg=t["bg"])
    app.footer_label.config(fg=t["text_dim"], bg=t["bg"])
    app.progress_canvas.config(bg=t["bg"])
    app.timer_label.config(bg=t["bg"], fg=t["text"])
    app.lock_label.config(bg=t["bg"], fg=t["text_dim"])

    for w in app.ctrl.winfo_children():
        if hasattr(w, "_is_btn"):
            w.config(fg=t["btn_fg"], bg=t["accent"])
            w.bind("<Enter>", lambda e, b=w: b.config(bg=t["accent_hover"]))
            w.bind("<Leave>", lambda e, b=w: b.config(bg=t["accent"]))

    app.theme_btn.config(text="  Light Mode  " if app.is_dark else "  Dark Mode  ")

    app.kb_outer.config(bg=t["bg_secondary"], highlightbackground=t["key_border"])
    app.canvas.config(bg=t["bg_secondary"])
    app.right_panel.config(bg=t["bg_secondary"], highlightbackground=t["key_border"])
    app.lat_title.config(fg=t["accent"], bg=t["bg_secondary"])
    app.missing_title.config(fg=t["accent"], bg=t["bg_secondary"])
    app.missing_label.config(fg=t["text_dim"], bg=t["bg_secondary"])
    app.ghost_title.config(fg=t["ghost"], bg=t["bg_secondary"])
    app.ghost_label.config(fg=t["ghost"], bg=t["bg_secondary"])
    app.combo_frame.config(bg=t["bg_secondary"])
    app.combo_title.config(fg=t["accent"], bg=t["bg_secondary"])

    for frame in app.right_panel.winfo_children():
        if isinstance(frame, tk.Frame):
            frame.config(bg=t["bg_secondary"])

    app.latency_list.config(
        bg=t["listbox_bg"], fg=t["listbox_fg"],
        selectbackground=t["accent"], selectforeground="white",
    )
    app.scrollbar.config(bg=t["scrollbar"], troughcolor=t["bg_secondary"], highlightthickness=0, borderwidth=0)

    style = ttk.Style(app.master)
    style.theme_use("clam")
    style.configure(".", background=t["bg"], foreground=t["text"], fieldbackground=t["bg_secondary"])
    style.configure("TCombobox", fieldbackground=t["bg_secondary"], background=t["key_border"],
                     foreground=t["text"], selectbackground=t["accent"], selectforeground="white")
    style.map("TCombobox", fieldbackground=[("readonly", t["bg_secondary"])])

    app._update_validate_btn()
    app._update_sound_btn()
    app._update_numpad_btn()
