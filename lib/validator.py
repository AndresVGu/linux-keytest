"""Validation gate, progress tracking, export, and reset."""

import time

from lib.combos import COMBOS
from lib.export import export_report, get_system_info
from lib.history import append_history
from lib.timer import stop_timer


def update_progress(app):
    """Update progress bar, counters, missing/ghost labels, and validate button."""
    t = app.theme
    all_keys = app._get_active_keysyms()
    total = len(all_keys)
    tested = len(app.pressed_keys & set(all_keys))
    missing = [k for k in all_keys if k not in app.pressed_keys]
    pct = (tested / total * 100) if total else 0

    # Counter
    ghost_count = len(app.ghost_keys)
    stuck_count = len(app.stuck_keys)
    status = "PASS" if tested == total and not app.stuck_keys and not app.ghost_keys else f"{tested}/{total}"
    extra = ""
    if stuck_count:
        extra += f"  Stuck:{stuck_count}"
    if ghost_count:
        extra += f"  Ghost:{ghost_count}"
    app.total_label.config(text=f"Keys: {status}  ({pct:.0f}%){extra}")

    # Bar
    app.progress_canvas.delete("all")
    cw = app.progress_canvas.winfo_width() or 600
    bar_h, y = 14, 2
    app.progress_canvas.create_rectangle(0, y, cw, y + bar_h, fill=t["progress_bg"], outline="")
    fill_w = int(cw * pct / 100)
    fill_color = t["progress_full"] if pct >= 100 else t["progress_fill"]
    if fill_w > 0:
        app.progress_canvas.create_rectangle(0, y, fill_w, y + bar_h, fill=fill_color, outline="")

    # Missing keys
    if missing:
        app.missing_label.config(text=", ".join(missing[:30]) + ("..." if len(missing) > 30 else ""))
    else:
        app.missing_label.config(text="None — All keys tested!")

    # Ghost keys
    if app.ghost_keys:
        app.ghost_label.config(text=", ".join(sorted(app.ghost_keys)))
    else:
        app.ghost_label.config(text="None")

    update_validate_btn(app)


def is_test_complete(app):
    all_keys = set(app._get_active_keysyms())
    keys_done = all_keys.issubset(app.pressed_keys)
    no_issues = not app.stuck_keys and not app.ghost_keys and not app.bounce_keys
    combos_done = len(app.tested_combos) == len(COMBOS)
    return keys_done and no_issues and combos_done


def update_validate_btn(app):
    t = app.theme
    if app.validated:
        app.validate_btn.config(bg=t["progress_full"], fg="#ffffff", text="  PASSED  ")
    elif is_test_complete(app):
        app.validate_btn.config(bg=t["progress_fill"], fg="#ffffff", text="  Validate  ")
    else:
        app.validate_btn.config(bg=t["key_border"], fg=t["text_dim"], text="  Validate  ")


def validate(app):
    if app.validated:
        return

    if not is_test_complete(app):
        missing_keys = [k for k in app._get_active_keysyms() if k not in app.pressed_keys]
        missing_combos = [c[2] for c in COMBOS if (c[0], c[1]) not in app.tested_combos]
        msg = []
        if missing_keys:
            msg.append(f"Keys: {len(missing_keys)} missing")
        if missing_combos:
            msg.append(f"Combos: {len(missing_combos)} missing")
        if app.stuck_keys:
            msg.append(f"Stuck: {len(app.stuck_keys)}")
        if app.ghost_keys:
            msg.append(f"Ghost: {len(app.ghost_keys)}")
        app.latency_list.insert(0, f" [!] {', '.join(msg)}")
        app.latency_list.itemconfig(0, fg=app.theme["key_stuck"])
        return

    app.validated = True
    stop_timer(app)
    app.timer_label.config(fg=app.theme["progress_full"])
    do_export(app)
    update_validate_btn(app)
    app.latency_list.insert(0, " [PASS] Test validated!")
    app.latency_list.itemconfig(0, fg=app.theme["progress_full"])


def do_export(app):
    all_keys = app._get_active_keysyms()
    elapsed = int(time.monotonic() - app.timer_start) if app.timer_start else 0
    path = export_report(
        layout_name=app.current_layout,
        all_keys=all_keys,
        tested_keys=app.pressed_keys,
        stuck_keys=app.stuck_keys,
        ghost_keys=app.ghost_keys,
        latencies=app.latencies,
        combos_total=len(COMBOS),
        combos_passed=len(app.tested_combos),
        combos_missing=[c[2] for c in COMBOS if (c[0], c[1]) not in app.tested_combos],
        elapsed_secs=elapsed,
        bounce_keys=app.bounce_keys,
        press_counts=app.key_press_count,
        output_dir=app.cfg["export_dir"],
    )
    app.latency_list.insert(0, f" Report: {path}")

    sys_info = get_system_info()
    append_history(
        history_file=app.cfg["history_file"],
        sys_info=sys_info,
        layout_name=app.current_layout,
        elapsed_secs=elapsed,
        all_keys=all_keys,
        tested_keys=app.pressed_keys,
        stuck_keys=app.stuck_keys,
        ghost_keys=app.ghost_keys,
        bounce_keys=app.bounce_keys,
        combos_passed=len(app.tested_combos),
        combos_total=len(COMBOS),
        latencies=app.latencies,
    )


def reset(app):
    app.pressed_keys.clear()
    app.stuck_keys.clear()
    app.ghost_keys.clear()
    app.key_press_times.clear()
    app.flash_jobs.clear()
    app.stuck_jobs.clear()
    app.latencies.clear()
    app.held_keys.clear()
    app.tested_combos.clear()
    app.key_press_count.clear()
    app.repeat_events.clear()
    app.bounce_keys.clear()
    app.validated = False
    app.highlight_keysym = None
    app.latency_list.delete(0, "end")
    stop_timer(app)
