"""Canvas-based keyboard drawing and key color management."""

from lib.seasonal import draw_decorations


def draw_keyboard(app):
    """Render the keyboard layout on the canvas."""
    app.canvas.delete("all")
    app.key_widgets.clear()
    app.canvas_keys.clear()

    layout = app._get_active_layout()
    U = app.UNIT
    PAD = app.KEY_PAD
    y = PAD

    for row_idx, row in enumerate(layout):
        x = PAD
        for keysym, label, width_u in row:
            w = int(U * width_u) - PAD * 2
            if keysym == "_gap":
                x += int(U * width_u)
                continue

            bg = key_bg(app, keysym)
            fg = key_fg(app, keysym)

            rid = _rounded_rect(app.canvas, x, y, x + w, y + app.KEY_H, 6,
                                fill=bg, outline=app.theme["key_border"])
            tid = app.canvas.create_text(
                x + w // 2, y + app.KEY_H // 2,
                text=label, fill=fg, font=app.FONT,
            )

            app.key_widgets[keysym] = {"rect": rid, "text": tid}
            app.canvas_keys[rid] = keysym
            app.canvas_keys[tid] = keysym

            if len(keysym) == 1 and keysym.isalpha():
                app.key_widgets[keysym.upper()] = app.key_widgets[keysym]

            x += int(U * width_u)

        y += app.KEY_H + PAD * 2
        if row_idx == 0:
            y += 10

    app.canvas.config(scrollregion=app.canvas.bbox("all"))

    # Seasonal decorations on top
    draw_decorations(app.canvas, getattr(app, 'season', None))


def key_bg(app, keysym):
    if keysym in app.stuck_keys:
        return app.theme["key_stuck"]
    if keysym in app.pressed_keys:
        return app.theme["key_tested"]
    return app.theme["key_bg"]


def key_fg(app, keysym):
    if keysym in app.stuck_keys:
        return app.theme["key_stuck_fg"]
    if keysym in app.pressed_keys:
        return app.theme["key_tested_fg"]
    return app.theme["key_fg"]


def set_key_color(app, keysym, bg, fg):
    if keysym not in app.key_widgets:
        return
    d = app.key_widgets[keysym]
    app.canvas.itemconfig(d["rect"], fill=bg)
    app.canvas.itemconfig(d["text"], fill=fg)


def set_key_tested(app, keysym):
    """Set key to tested color, or bounce color if flagged."""
    if keysym not in app.key_widgets:
        return
    t = app.theme
    is_bounce = keysym in app.bounce_keys
    bg = t["ghost"] if is_bounce else t["key_tested"]
    fg = t["ghost_fg"] if is_bounce else t["key_tested_fg"]
    d = app.key_widgets[keysym]
    app.canvas.itemconfig(d["rect"], fill=bg)
    app.canvas.itemconfig(d["text"], fill=fg)


def _rounded_rect(canvas, x1, y1, x2, y2, r=8, **kw):
    pts = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kw)
