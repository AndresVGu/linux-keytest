"""Seasonal decorations drawn on the keyboard canvas."""

import math
from datetime import date


def get_active_season():
    """Return the active holiday name or None based on today's date."""
    today = date.today()
    m, d = today.month, today.day

    if m == 12 and 28 <= d <= 31:
        return "newyear"
    if m == 1 and 1 <= d <= 3:
        return "newyear"
    if m == 2 and 10 <= d <= 14:
        return "valentine"
    if m == 3 and 13 <= d <= 17:
        return "stpatrick"
    if m == 10 and 27 <= d <= 31:
        return "halloween"
    if m == 10 and 7 <= d <= 13:
        return "thanksgiving"
    if m == 12 and 18 <= d <= 25:
        return "christmas"
    return None


def get_season_footer(season):
    """Return a festive footer message."""
    msgs = {
        "newyear": "Happy New Year!",
        "valentine": "Happy Valentine's Day!",
        "stpatrick": "Happy St. Patrick's Day!",
        "halloween": "Happy Halloween!",
        "thanksgiving": "Happy Thanksgiving!",
        "christmas": "Merry Christmas!",
    }
    return msgs.get(season, "")


def draw_decorations(canvas, season):
    """Draw seasonal decorations on the canvas. Call after keyboard is drawn."""
    canvas.delete("seasonal")
    if not season:
        return

    cw = canvas.winfo_width() or 900
    ch = canvas.winfo_height() or 350

    fn = {
        "newyear": _draw_newyear,
        "valentine": _draw_valentine,
        "stpatrick": _draw_stpatrick,
        "halloween": _draw_halloween,
        "thanksgiving": _draw_thanksgiving,
        "christmas": _draw_christmas,
    }.get(season)

    if fn:
        fn(canvas, cw, ch)


# ── Valentine's Day: Hearts ──

def _draw_heart(canvas, cx, cy, size, color):
    pts = []
    for i in range(100):
        t = math.pi * 2 * i / 100
        x = size * 16 * math.sin(t) ** 3
        y = -size * (13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        pts.extend([cx + x * 0.06, cy + y * 0.06])
    canvas.create_polygon(pts, fill=color, outline="", smooth=True, tags="seasonal")


def _draw_valentine(canvas, cw, ch):
    _draw_heart(canvas, 30, 30, 12, "#e74c3c")
    _draw_heart(canvas, cw - 30, 30, 10, "#ff6b81")
    _draw_heart(canvas, 25, ch - 25, 8, "#ff6b81")
    _draw_heart(canvas, cw - 25, ch - 25, 11, "#e74c3c")
    _draw_heart(canvas, cw // 2, 20, 7, "#e74c3c55")


# ── St. Patrick's Day: Shamrocks ──

def _draw_shamrock_leaf(canvas, cx, cy, r, angle, color):
    pts = []
    for i in range(50):
        t = math.pi * 2 * i / 50
        x = cx + r * math.cos(t) * math.cos(math.radians(angle)) - r * 0.6 * math.sin(t) * math.sin(math.radians(angle))
        y = cy + r * math.cos(t) * math.sin(math.radians(angle)) + r * 0.6 * math.sin(t) * math.cos(math.radians(angle))
        pts.extend([x, y])
    canvas.create_polygon(pts, fill=color, outline="", smooth=True, tags="seasonal")


def _draw_shamrock(canvas, cx, cy, size, color):
    offset = size * 0.7
    for angle in [90, 210, 330]:
        lx = cx + offset * math.cos(math.radians(angle))
        ly = cy - offset * math.sin(math.radians(angle))
        _draw_shamrock_leaf(canvas, lx, ly, size, angle, color)
    # Stem
    canvas.create_line(cx, cy + size * 0.3, cx + size * 0.2, cy + size * 1.8,
                       fill=color, width=2, tags="seasonal")


def _draw_stpatrick(canvas, cw, ch):
    _draw_shamrock(canvas, 30, 30, 10, "#27ae60")
    _draw_shamrock(canvas, cw - 30, 28, 8, "#2ecc71")
    _draw_shamrock(canvas, 25, ch - 25, 7, "#2ecc71")
    _draw_shamrock(canvas, cw - 28, ch - 22, 9, "#27ae60")


# ── Halloween: Pumpkins and Bats ──

def _draw_pumpkin(canvas, cx, cy, size, color):
    s = size
    # Body
    canvas.create_oval(cx - s, cy - s * 0.8, cx + s, cy + s * 0.8,
                       fill=color, outline="#c0392b", width=1, tags="seasonal")
    # Vertical lines
    canvas.create_arc(cx - s * 0.3, cy - s * 0.8, cx + s * 0.3, cy + s * 0.8,
                      start=0, extent=180, style="arc", outline="#c0392b", tags="seasonal")
    # Stem
    canvas.create_rectangle(cx - 2, cy - s * 0.8, cx + 2, cy - s * 1.1,
                            fill="#27ae60", outline="", tags="seasonal")
    # Eyes
    es = s * 0.2
    canvas.create_polygon(cx - s * 0.3, cy - es, cx - s * 0.3 + es, cy - es * 2,
                          cx - s * 0.3 + es * 2, cy - es,
                          fill="#1a1a2e", outline="", tags="seasonal")
    canvas.create_polygon(cx + s * 0.3, cy - es, cx + s * 0.3 - es, cy - es * 2,
                          cx + s * 0.3 - es * 2, cy - es,
                          fill="#1a1a2e", outline="", tags="seasonal")
    # Mouth
    canvas.create_arc(cx - s * 0.4, cy - s * 0.1, cx + s * 0.4, cy + s * 0.5,
                      start=200, extent=140, style="arc", outline="#1a1a2e", width=2, tags="seasonal")


def _draw_bat(canvas, cx, cy, size, color):
    s = size
    # Body
    canvas.create_oval(cx - s * 0.15, cy - s * 0.2, cx + s * 0.15, cy + s * 0.2,
                       fill=color, outline="", tags="seasonal")
    # Left wing
    pts_l = [cx - s * 0.1, cy, cx - s * 0.5, cy - s * 0.5, cx - s * 0.8, cy - s * 0.2,
             cx - s * 0.6, cy + s * 0.1, cx - s * 0.3, cy - s * 0.1]
    canvas.create_polygon(pts_l, fill=color, outline="", smooth=True, tags="seasonal")
    # Right wing
    pts_r = [cx + s * 0.1, cy, cx + s * 0.5, cy - s * 0.5, cx + s * 0.8, cy - s * 0.2,
             cx + s * 0.6, cy + s * 0.1, cx + s * 0.3, cy - s * 0.1]
    canvas.create_polygon(pts_r, fill=color, outline="", smooth=True, tags="seasonal")
    # Eyes
    canvas.create_oval(cx - s * 0.08, cy - s * 0.1, cx - s * 0.02, cy - s * 0.04,
                       fill="#e74c3c", outline="", tags="seasonal")
    canvas.create_oval(cx + s * 0.02, cy - s * 0.1, cx + s * 0.08, cy - s * 0.04,
                       fill="#e74c3c", outline="", tags="seasonal")


def _draw_halloween(canvas, cw, ch):
    _draw_pumpkin(canvas, 30, 30, 16, "#e67e22")
    _draw_pumpkin(canvas, cw - 30, ch - 25, 14, "#f39c12")
    _draw_bat(canvas, cw - 60, 25, 20, "#2c3e50")
    _draw_bat(canvas, 60, ch - 20, 16, "#2c3e50")


# ── Thanksgiving: Autumn Leaves ──

def _draw_leaf(canvas, cx, cy, size, color):
    s = size
    pts = [
        cx, cy - s,
        cx + s * 0.3, cy - s * 0.6,
        cx + s * 0.7, cy - s * 0.5,
        cx + s * 0.4, cy - s * 0.2,
        cx + s * 0.6, cy + s * 0.1,
        cx + s * 0.2, cy + s * 0.1,
        cx, cy + s * 0.5,
        cx - s * 0.2, cy + s * 0.1,
        cx - s * 0.6, cy + s * 0.1,
        cx - s * 0.4, cy - s * 0.2,
        cx - s * 0.7, cy - s * 0.5,
        cx - s * 0.3, cy - s * 0.6,
    ]
    canvas.create_polygon(pts, fill=color, outline="", smooth=True, tags="seasonal")
    # Stem
    canvas.create_line(cx, cy + s * 0.3, cx, cy + s * 0.8,
                       fill="#8B4513", width=1, tags="seasonal")


def _draw_thanksgiving(canvas, cw, ch):
    colors = ["#e67e22", "#c0392b", "#f39c12", "#d35400"]
    _draw_leaf(canvas, 25, 25, 14, colors[0])
    _draw_leaf(canvas, cw - 25, 22, 12, colors[1])
    _draw_leaf(canvas, 20, ch - 20, 10, colors[2])
    _draw_leaf(canvas, cw - 20, ch - 18, 13, colors[3])
    _draw_leaf(canvas, cw // 2 - 40, 18, 8, colors[1])
    _draw_leaf(canvas, cw // 2 + 40, 18, 9, colors[2])


# ── Christmas: Tree, Snowflakes, Stars ──

def _draw_tree(canvas, cx, cy, size, color):
    s = size
    # Three triangle layers
    for i, (w, h) in enumerate([(0.5, 0.4), (0.7, 0.35), (0.9, 0.3)]):
        top_y = cy - s * (0.8 - i * 0.3)
        bot_y = top_y + s * h
        half_w = s * w * 0.5
        canvas.create_polygon(
            cx, top_y, cx - half_w, bot_y, cx + half_w, bot_y,
            fill=color, outline="", tags="seasonal",
        )
    # Trunk
    canvas.create_rectangle(cx - s * 0.08, cy + s * 0.1, cx + s * 0.08, cy + s * 0.3,
                            fill="#8B4513", outline="", tags="seasonal")
    # Star on top
    _draw_star(canvas, cx, cy - s * 0.85, s * 0.12, "#f1c40f")


def _draw_star(canvas, cx, cy, size, color):
    pts = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = size if i % 2 == 0 else size * 0.4
        pts.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
    canvas.create_polygon(pts, fill=color, outline="", tags="seasonal")


def _draw_snowflake(canvas, cx, cy, size, color):
    for angle in [0, 60, 120]:
        rad = math.radians(angle)
        x1 = cx + size * math.cos(rad)
        y1 = cy + size * math.sin(rad)
        x2 = cx - size * math.cos(rad)
        y2 = cy - size * math.sin(rad)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=1, tags="seasonal")
        # Small branches
        for sign in [1, -1]:
            bx = cx + size * 0.5 * math.cos(rad) + sign * size * 0.25 * math.cos(rad + math.pi / 3)
            by = cy + size * 0.5 * math.sin(rad) + sign * size * 0.25 * math.sin(rad + math.pi / 3)
            canvas.create_line(cx + size * 0.5 * math.cos(rad), cy + size * 0.5 * math.sin(rad),
                               bx, by, fill=color, width=1, tags="seasonal")


def _draw_christmas(canvas, cw, ch):
    _draw_tree(canvas, 35, 40, 28, "#27ae60")
    _draw_tree(canvas, cw - 35, ch - 30, 24, "#2ecc71")
    _draw_snowflake(canvas, cw - 50, 25, 10, "#bdc3c7")
    _draw_snowflake(canvas, 50, ch - 20, 8, "#ecf0f1")
    _draw_snowflake(canvas, cw // 2, 15, 9, "#bdc3c7")
    _draw_star(canvas, cw // 2 + 60, 18, 6, "#f1c40f")
    _draw_star(canvas, cw // 2 - 60, ch - 15, 5, "#f1c40f")


# ── New Year: Fireworks and Stars ──

def _draw_firework(canvas, cx, cy, size, color):
    for i in range(12):
        angle = math.radians(i * 30)
        x1 = cx + size * 0.3 * math.cos(angle)
        y1 = cy + size * 0.3 * math.sin(angle)
        x2 = cx + size * math.cos(angle)
        y2 = cy + size * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=1, tags="seasonal")
        # Dot at tip
        canvas.create_oval(x2 - 1.5, y2 - 1.5, x2 + 1.5, y2 + 1.5,
                           fill=color, outline="", tags="seasonal")


def _draw_newyear(canvas, cw, ch):
    _draw_firework(canvas, 40, 35, 22, "#f1c40f")
    _draw_firework(canvas, cw - 40, 30, 18, "#e74c3c")
    _draw_firework(canvas, cw // 2, 20, 15, "#3498db")
    _draw_firework(canvas, 35, ch - 25, 16, "#9b59b6")
    _draw_firework(canvas, cw - 35, ch - 20, 20, "#2ecc71")
    _draw_star(canvas, cw // 2 - 80, 15, 5, "#f1c40f")
    _draw_star(canvas, cw // 2 + 80, ch - 12, 4, "#e74c3c")
    _draw_star(canvas, 70, 15, 4, "#3498db")
    _draw_star(canvas, cw - 70, ch - 12, 3, "#f39c12")
