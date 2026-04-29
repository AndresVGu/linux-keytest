"""Keyboard layouts: Canadian English, Canadian French, Spanish (Latin America)."""

import subprocess

LAYOUTS = {}


def detect_system_layout():
    """Auto-detect keyboard layout from the system using setxkbmap."""
    try:
        result = subprocess.run(
            ["setxkbmap", "-query"], capture_output=True, text=True, timeout=3,
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if line.strip().startswith("layout:"):
                    layout = line.split(":")[1].strip()
                    mapping = {
                        "us": "Canadian English",
                        "ca": "Canadian French",
                        "latam": "Spanish (Latin America)",
                        "es": "Spanish (Latin America)",
                    }
                    return mapping.get(layout, "Canadian English")
    except Exception:
        pass
    return "Canadian English"


def _ca_en():
    return [
        [
            ("Escape", "Esc", 1), ("_gap", "", 0.5),
            ("F1", "F1", 1), ("F2", "F2", 1), ("F3", "F3", 1), ("F4", "F4", 1), ("_gap", "", 0.3),
            ("F5", "F5", 1), ("F6", "F6", 1), ("F7", "F7", 1), ("F8", "F8", 1), ("_gap", "", 0.3),
            ("F9", "F9", 1), ("F10", "F10", 1), ("F11", "F11", 1), ("F12", "F12", 1), ("_gap", "", 0.3),
            ("Print", "PrtSc", 1), ("Scroll_Lock", "ScrLk", 1), ("Pause", "Pause", 1),
        ],
        [
            ("grave", "` ~", 1), ("1", "1 !", 1), ("2", "2 @", 1), ("3", "3 #", 1), ("4", "4 $", 1),
            ("5", "5 %", 1), ("6", "6 ^", 1), ("7", "7 &", 1), ("8", "8 *", 1), ("9", "9 (", 1),
            ("0", "0 )", 1), ("minus", "- _", 1), ("equal", "= +", 1), ("BackSpace", "Backspace", 2), ("_gap", "", 0.3),
            ("Insert", "Ins", 1), ("Home", "Home", 1), ("Prior", "PgUp", 1),
        ],
        [
            ("Tab", "Tab", 1.5), ("q", "Q", 1), ("w", "W", 1), ("e", "E", 1), ("r", "R", 1),
            ("t", "T", 1), ("y", "Y", 1), ("u", "U", 1), ("i", "I", 1), ("o", "O", 1),
            ("p", "P", 1), ("bracketleft", "[ {", 1), ("bracketright", "] }", 1),
            ("backslash", "\\ |", 1.5), ("_gap", "", 0.3),
            ("Delete", "Del", 1), ("End", "End", 1), ("Next", "PgDn", 1),
        ],
        [
            ("Caps_Lock", "Caps Lock", 1.75), ("a", "A", 1), ("s", "S", 1), ("d", "D", 1), ("f", "F", 1),
            ("g", "G", 1), ("h", "H", 1), ("j", "J", 1), ("k", "K", 1), ("l", "L", 1),
            ("semicolon", "; :", 1), ("apostrophe", "' \"", 1), ("Return", "Enter", 2.25),
        ],
        [
            ("Shift_L", "Shift", 2.25), ("z", "Z", 1), ("x", "X", 1), ("c", "C", 1),
            ("v", "V", 1), ("b", "B", 1), ("n", "N", 1), ("m", "M", 1), ("comma", ", <", 1),
            ("period", ". >", 1), ("slash", "/ ?", 1), ("Shift_R", "Shift", 2.75),
            ("_gap", "", 1.3), ("Up", "Up", 1),
        ],
        [
            ("Control_L", "Ctrl", 1.5), ("Super_L", "Super", 1.25), ("Alt_L", "Alt", 1.25),
            ("space", "Space", 6.25),
            ("Alt_R", "Alt", 1.25), ("Menu", "Menu", 1.25), ("Control_R", "Ctrl", 1.5),
            ("_gap", "", 0.3), ("Left", "Left", 1), ("Down", "Down", 1), ("Right", "Right", 1),
        ],
    ]


def _ca_fr():
    return [
        [
            ("Escape", "Echap", 1), ("_gap", "", 0.5),
            ("F1", "F1", 1), ("F2", "F2", 1), ("F3", "F3", 1), ("F4", "F4", 1), ("_gap", "", 0.3),
            ("F5", "F5", 1), ("F6", "F6", 1), ("F7", "F7", 1), ("F8", "F8", 1), ("_gap", "", 0.3),
            ("F9", "F9", 1), ("F10", "F10", 1), ("F11", "F11", 1), ("F12", "F12", 1), ("_gap", "", 0.3),
            ("Print", "ImpEc", 1), ("Scroll_Lock", "ArrDef", 1), ("Pause", "Arret", 1),
        ],
        [
            ("numbersign", "# |", 1), ("1", "1 !", 1), ("2", '2 "', 1), ("3", "3 /", 1), ("4", "4 $", 1),
            ("5", "5 %", 1), ("6", "6 ?", 1), ("7", "7 &", 1), ("8", "8 *", 1), ("9", "9 (", 1),
            ("0", "0 )", 1), ("minus", "- _", 1), ("equal", "= +", 1), ("BackSpace", "Retour", 2), ("_gap", "", 0.3),
            ("Insert", "Inser", 1), ("Home", "Debut", 1), ("Prior", "PgHt", 1),
        ],
        [
            ("Tab", "Tab", 1.5), ("q", "Q", 1), ("w", "W", 1), ("e", "E", 1), ("r", "R", 1),
            ("t", "T", 1), ("y", "Y", 1), ("u", "U", 1), ("i", "I", 1), ("o", "O", 1),
            ("p", "P", 1), ("dead_circumflex", "^ [", 1), ("dead_cedilla", "c ]", 1),
            ("backslash", "\\ |", 1.5), ("_gap", "", 0.3),
            ("Delete", "Suppr", 1), ("End", "Fin", 1), ("Next", "PgBs", 1),
        ],
        [
            ("Caps_Lock", "Verr Maj", 1.75), ("a", "A", 1), ("s", "S", 1), ("d", "D", 1), ("f", "F", 1),
            ("g", "G", 1), ("h", "H", 1), ("j", "J", 1), ("k", "K", 1), ("l", "L", 1),
            ("semicolon", "; :", 1), ("dead_grave", "` {", 1), ("Return", "Entree", 2.25),
        ],
        [
            ("Shift_L", "Maj", 2.25), ("z", "Z", 1), ("x", "X", 1), ("c", "C", 1),
            ("v", "V", 1), ("b", "B", 1), ("n", "N", 1), ("m", "M", 1), ("comma", ", '", 1),
            ("period", ". .", 1), ("eacute", "e <", 1), ("Shift_R", "Maj", 2.75),
            ("_gap", "", 1.3), ("Up", "Haut", 1),
        ],
        [
            ("Control_L", "Ctrl", 1.5), ("Super_L", "Super", 1.25), ("Alt_L", "Alt", 1.25),
            ("space", "Espace", 6.25),
            ("Alt_R", "AltCar", 1.25), ("Menu", "Menu", 1.25), ("Control_R", "Ctrl", 1.5),
            ("_gap", "", 0.3), ("Left", "Gche", 1), ("Down", "Bas", 1), ("Right", "Drte", 1),
        ],
    ]


def _es_latam():
    return [
        [
            ("Escape", "Esc", 1), ("_gap", "", 0.5),
            ("F1", "F1", 1), ("F2", "F2", 1), ("F3", "F3", 1), ("F4", "F4", 1), ("_gap", "", 0.3),
            ("F5", "F5", 1), ("F6", "F6", 1), ("F7", "F7", 1), ("F8", "F8", 1), ("_gap", "", 0.3),
            ("F9", "F9", 1), ("F10", "F10", 1), ("F11", "F11", 1), ("F12", "F12", 1), ("_gap", "", 0.3),
            ("Print", "ImPnt", 1), ("Scroll_Lock", "BloqD", 1), ("Pause", "Pausa", 1),
        ],
        [
            ("bar", "| o", 1), ("1", "1 !", 1), ("2", '2 "', 1), ("3", "3 #", 1), ("4", "4 $", 1),
            ("5", "5 %", 1), ("6", "6 &", 1), ("7", "7 /", 1), ("8", "8 (", 1), ("9", "9 )", 1),
            ("0", "0 =", 1), ("apostrophe", "' ?", 1), ("questiondown", "' !", 1), ("BackSpace", "Retro", 2), ("_gap", "", 0.3),
            ("Insert", "Ins", 1), ("Home", "Inicio", 1), ("Prior", "RePag", 1),
        ],
        [
            ("Tab", "Tab", 1.5), ("q", "Q", 1), ("w", "W", 1), ("e", "E", 1), ("r", "R", 1),
            ("t", "T", 1), ("y", "Y", 1), ("u", "U", 1), ("i", "I", 1), ("o", "O", 1),
            ("p", "P", 1), ("dead_acute", "' [", 1), ("plus", "+ ]", 1),
            ("backslash", "} {", 1.5), ("_gap", "", 0.3),
            ("Delete", "Supr", 1), ("End", "Fin", 1), ("Next", "AvPag", 1),
        ],
        [
            ("Caps_Lock", "BloqMay", 1.75), ("a", "A", 1), ("s", "S", 1), ("d", "D", 1), ("f", "F", 1),
            ("g", "G", 1), ("h", "H", 1), ("j", "J", 1), ("k", "K", 1), ("l", "L", 1),
            ("ntilde", "N ~", 1), ("braceleft", "{ ^", 1), ("Return", "Intro", 2.25),
        ],
        [
            ("Shift_L", "Mayus", 2.25), ("less", "< >", 1), ("z", "Z", 1), ("x", "X", 1), ("c", "C", 1),
            ("v", "V", 1), ("b", "B", 1), ("n", "N", 1), ("m", "M", 1), ("comma", ", ;", 1),
            ("period", ". :", 1), ("Shift_R", "Mayus", 2.75),
            ("_gap", "", 1.3), ("Up", "Arr", 1),
        ],
        [
            ("Control_L", "Ctrl", 1.5), ("Super_L", "Super", 1.25), ("Alt_L", "Alt", 1.25),
            ("space", "Espacio", 6.25),
            ("Alt_R", "AltGr", 1.25), ("Menu", "Menu", 1.25), ("Control_R", "Ctrl", 1.5),
            ("_gap", "", 0.3), ("Left", "Izq", 1), ("Down", "Abj", 1), ("Right", "Der", 1),
        ],
    ]


def get_all_keysyms(layout_data):
    """Extract all testable keysyms from a layout (excludes gaps)."""
    keys = []
    for row in layout_data:
        for keysym, _, _ in row:
            if keysym != "_gap":
                keys.append(keysym)
    return keys


def _numpad():
    """Standard numpad rows to append to any layout."""
    return [
        [("Num_Lock", "NumLk", 1), ("KP_Divide", "/", 1), ("KP_Multiply", "*", 1), ("KP_Subtract", "-", 1)],
        [("KP_7", "7", 1), ("KP_8", "8", 1), ("KP_9", "9", 1), ("KP_Add", "+", 1)],
        [("KP_4", "4", 1), ("KP_5", "5", 1), ("KP_6", "6", 1)],
        [("KP_1", "1", 1), ("KP_2", "2", 1), ("KP_3", "3", 1), ("KP_Enter", "Ent", 1)],
        [("KP_0", "0", 2), ("KP_Decimal", ".", 1)],
    ]


NUMPAD = _numpad()

LAYOUTS = {
    "Canadian English": _ca_en(),
    "Canadian French": _ca_fr(),
    "Spanish (Latin America)": _es_latam(),
}
