<h1 align="center">
  ⌨️ Linux Keytest
</h1>

<p align="center">
  <b>Professional keyboard testing tool for QA hardware validation on Linux</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-blue" alt="Tkinter">
  <img src="https://img.shields.io/badge/Platform-Ubuntu%20Linux-E95420?logo=ubuntu&logoColor=white" alt="Ubuntu">
  <img src="https://img.shields.io/badge/Theme-Light%20%2F%20Dark-333" alt="Themes">
</p>

---

## Table of Contents

- [What is This?](#what-is-this)
- [Who is This For?](#who-is-this-for)
- [Goals](#goals)
- [Features](#features)
  - [Key Testing](#key-testing)
  - [Defect Detection](#defect-detection)
  - [Modifier Combo Test](#modifier-combo-test)
  - [Validation Gate](#validation-gate)
  - [Reporting](#reporting)
  - [User Experience](#user-experience)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Standalone](#standalone)
  - [Via Toughbook AutoInstall](#via-toughbook-autoinstall)
- [User Manual](#user-manual)
  - [Main Interface](#main-interface)
  - [Testing a Keyboard](#testing-a-keyboard)
  - [Combo Test Mode](#combo-test-mode)
  - [Validating and Exporting](#validating-and-exporting)
  - [Understanding the Report](#understanding-the-report)
  - [History Log](#history-log)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Keyboard Layouts](#keyboard-layouts)
- [Author](#author)

---

## What is This?

Linux Keytest is a Python/Tkinter desktop application that provides a visual, interactive way to test every key on a physical keyboard. It renders a realistic on-screen keyboard layout, highlights keys as they are pressed, detects hardware defects (stuck keys, ghost keys, bouncing contacts), measures latency, and generates QA reports.

It was built to be used in a **refurbishment production line** where technicians need to verify that every key on a laptop keyboard works correctly before the unit is shipped to a customer.

---

## Who is This For?

- **QA technicians** testing refurbished laptops (Panasonic Toughbooks, Dell, etc.)
- **IT departments** validating hardware before deployment
- **Anyone** who needs to verify that a keyboard is fully functional

---

## Goals

- **Ensure 100% key coverage** — Every key must be tested before a unit passes QA
- **Detect physical defects** — Stuck keys, ghost keys (short circuits), and bouncing contacts
- **Standardize the QA process** — Every technician follows the same test procedure
- **Generate audit trail** — Exportable reports and CSV history for supervisors
- **Minimize test time** — Visual guides, sound feedback, and progress tracking keep the technician moving fast
- **Support multiple languages** — Canadian English, Canadian French, and Spanish (Latin America) keyboard layouts with localized key labels

---

## Features

### Key Testing

- **Visual keyboard** — Canvas-based rendering with rounded keys, realistic spacing, and grouped key clusters (F-keys, nav, arrows)
- **Real-time feedback** — Keys flash red on press, then fade to a subtle tested color
- **Progress bar** — Shows percentage of keys tested with a color-coded bar
- **Missing keys list** — Panel showing exactly which keys haven't been tested yet
- **Next key highlight** — The next untested key blinks to guide the technician
- **Multi-press counter** — Tracks how many times each key was pressed (detects weak contacts that need multiple attempts)
- **Latency measurement** — Records press-to-release time in milliseconds for every key
- **Numpad support** — Toggle button to add numpad keys for models that have one (CF-54, CF-53)

### Defect Detection

- **Stuck key detection** — If a key is held for more than 3 seconds (configurable), it is flagged as stuck and highlighted in red
- **Ghost key detection** — If a key event is received for a key that doesn't exist in the current layout, it is flagged as a ghost key (possible short circuit in the keyboard membrane)
- **Bounce detection** — Measures the auto-repeat rate when a key is held. If the rate exceeds the threshold (default: 15 repeats/sec), the key is flagged as bouncing (intermittent contact)

### Modifier Combo Test

- **Dedicated combo mode** — Toggle button activates a checklist of modifier key combinations
- **Simultaneous detection** — Detects when both keys of a combo are held at the same time
- **12 standard combos** — Shift+A, Shift+Z, Ctrl+C/V/X/A/Z/S, Alt+F4, Alt+Tab, Ctrl+Alt, Shift+Ctrl
- **Visual checklist** — Each combo shows as pending or passed in the right panel

### Validation Gate

- **Validate button** — Only activates (turns green) when ALL conditions are met:
  - All keys tested
  - All combos passed
  - Zero stuck keys
  - Zero ghost keys
  - Zero bouncing keys
- **Incomplete test feedback** — If clicked before completion, shows exactly what's missing
- **Auto-export on validation** — Generates the report and logs to history automatically
- **PASS indicator** — Button turns green with "PASSED" text, timer stops and turns green

### Reporting

- **Text report** — Generates a `.txt` file in `~/Downloads` with full test results:
  - Machine model and serial number (via `dmidecode`)
  - Layout used, test duration
  - Keys: total, tested, missing, stuck, ghost, bouncing
  - Combos: passed/total
  - Average latency
  - PASS/FAIL status
  - Detailed lists of missing keys, stuck keys, ghost keys, bouncing keys, multi-press keys, and missing combos
- **CSV history** — Every export appends a row to `~/.keytest_history.csv` with summary data. Supervisors can open this in LibreOffice to track how many units were tested and which ones failed

### User Experience

- **Light and dark mode** — Light mode by default, toggle with a button
- **Sound feedback** — Click sound on every keypress (uses `paplay` with freedesktop sounds). Toggle on/off
- **Session timer** — Starts on first keypress, shows elapsed time in MM:SS format
- **Caps Lock / Num Lock indicator** — Shows current state in the toolbar, updated every 500ms
- **System key grabbing** — Temporarily disables GNOME shortcuts for Super and Print Screen so they can be tested without triggering OS functions. All shortcuts are restored when the app closes
- **Auto-detect layout** — Detects the system keyboard layout via `setxkbmap` and selects the matching layout automatically
- **Configurable** — All timings, thresholds, and paths can be customized via `config.json`

---

## Requirements

- Python 3.x
- `python3-tk` (Tkinter)
- `dbus-x11` (required when running from a root terminal)
- `pulseaudio-utils` (for sound feedback via `paplay`, optional)

---

## Installation

```bash
sudo apt install -y python3-tk dbus-x11
git clone https://github.com/AndresVGu/linux-keytest
cd linux-keytest
```

---

## Usage

### Standalone

```bash
python3 keytest.py
```

### Via Toughbook AutoInstall

The [toughbook-autoinstall](https://github.com/AndresVGu/toughbook-autoinstall) script (option 4 in the menu) clones this repo automatically into `~/Downloads/linux-keytest/` and launches it in a new terminal window.

---

## User Manual

### Main Interface

The interface is divided into:

- **Top bar** — Title, layout selector, action buttons (Reset, Export, Combo Test, Dark Mode, Validate, Sound, Numpad), session timer, key counter, and Caps/Num Lock indicator
- **Progress bar** — Green bar showing percentage of keys tested
- **Keyboard panel** (left) — Visual keyboard with realistic layout and spacing
- **Info panel** (right) — Latency log, missing keys list, ghost keys list, and combo checklist (when active)

### Testing a Keyboard

1. Launch the application
2. Select the correct layout from the dropdown (or let it auto-detect)
3. If the unit has a numpad, click **Numpad: OFF** to toggle it on
4. Start pressing keys — the timer starts automatically on the first keypress
5. Each key flashes red when pressed, then fades to a subtle color once tested
6. The next untested key blinks to guide you
7. Watch the progress bar and missing keys list to track what's left
8. If a key doesn't register, press it again — the multi-press counter will flag it in the report

### Combo Test Mode

1. Click **Combo Test** to activate the mode
2. A checklist appears in the right panel showing all combos to test
3. Press both keys of each combo simultaneously (e.g., hold Ctrl then press C)
4. Each combo turns green with `[+]` when detected
5. Click **Keys Mode** to return to normal testing

### Validating and Exporting

- The **Validate** button is gray when the test is incomplete
- When all keys + combos are tested and no defects are found, it turns green
- Click it to:
  - Stop the timer
  - Auto-generate the report
  - Log the result to history
  - Show "PASSED" in green
- You can also click **Export Report** at any time to generate a report without validating

### Understanding the Report

The generated `.txt` report includes:

| Section | Description |
|:--------|:------------|
| Header | Date, model, serial, layout, duration |
| Results | Total/tested/missing/stuck/ghost/bounce counts, avg latency, combos, PASS/FAIL |
| Missing Keys | List of keys that were not pressed |
| Stuck Keys | Keys that were held for more than the stuck timeout |
| Ghost Keys | Keys that fired events without being in the layout (possible short circuit) |
| Bouncing Keys | Keys with abnormally high repeat rate (intermittent contact) |
| Multi-Press Keys | Keys that were pressed more than once, sorted by count |
| Missing Combos | Modifier combinations that were not tested |

### History Log

Every time a report is exported, a row is appended to `~/.keytest_history.csv` with:

```
date, model, serial, layout, duration_s, total_keys, tested, missing, stuck, ghost, bounce, combos_passed, combos_total, avg_latency_ms, status
```

Open this file in LibreOffice Calc to review test history across multiple units.

---

## Configuration

All settings are in `config.json` at the project root:

```json
{
    "default_layout": "auto",
    "sound_enabled": true,
    "stuck_timeout_ms": 3000,
    "bounce_threshold": 15,
    "flash_duration_ms": 150,
    "highlight_blink_ms": 600,
    "export_dir": "~/Downloads",
    "history_file": "~/.keytest_history.csv"
}
```

| Setting | Description | Default |
|:--------|:------------|:--------|
| `default_layout` | `"auto"` to detect via `setxkbmap`, or a layout name | `"auto"` |
| `sound_enabled` | Enable click sound on keypress | `true` |
| `stuck_timeout_ms` | Milliseconds before a held key is flagged as stuck | `3000` |
| `bounce_threshold` | Max repeats/second before flagging as bounce | `15` |
| `flash_duration_ms` | How long the red flash stays after key release | `150` |
| `highlight_blink_ms` | Blink interval for the next untested key | `600` |
| `export_dir` | Directory where reports are saved | `~/Downloads` |
| `history_file` | Path to the CSV history file | `~/.keytest_history.csv` |

If `config.json` is missing or a field is absent, defaults are used.

---

## Project Structure

```
linux-keytest/
├── keytest.py              # Entry point — orchestrator (state, events, delegation)
├── config.json             # User-configurable settings
├── lib/
│   ├── __init__.py         # Package marker
│   ├── ui.py               # UI construction and theme application
│   ├── renderer.py         # Canvas keyboard drawing and key color management
│   ├── validator.py        # Progress tracking, validation gate, export, reset
│   ├── timer.py            # Session timer, sound feedback, key highlight, lock polling
│   ├── themes.py           # LIGHT and DARK color palettes
│   ├── layouts.py          # Keyboard layouts (CA-EN, CA-FR, ES-LATAM) + numpad + auto-detect
│   ├── combos.py           # Modifier key combinations for combo testing
│   ├── config.py           # Config loader with defaults fallback
│   ├── grabber.py          # GNOME shortcut grabber/releaser (Super, PrtSc)
│   ├── export.py           # Text report generator + system info via dmidecode
│   └── history.py          # CSV history logger
└── README.md               # This file
```

| Module | Lines | Responsibility |
|:-------|------:|:---------------|
| `keytest.py` | 325 | Orchestrator: application state, key event handling, and delegation to components |
| `lib/ui.py` | 198 | Builds all Tkinter widgets (header, toolbar, panels, buttons) and applies theme colors |
| `lib/renderer.py` | 97 | Draws the keyboard on a Canvas with rounded keys, manages key color states |
| `lib/validator.py` | 156 | Progress bar updates, missing/ghost key tracking, validation gate logic, export + history triggers, reset |
| `lib/timer.py` | 97 | Session timer (MM:SS), sound feedback via `paplay`, next-key blink highlight, Caps/Num Lock polling |
| `lib/layouts.py` | 183 | Three keyboard layout definitions with localized labels, numpad rows, keysym extraction, system layout auto-detection |
| `lib/export.py` | 128 | Generates formatted `.txt` QA reports with machine info from `dmidecode` |
| `lib/themes.py` | 63 | Color dictionaries for light and dark mode (key states, UI elements, progress bar, defect indicators) |
| `lib/grabber.py` | 56 | Uses `gsettings` to temporarily disable GNOME shortcuts and restore them on exit |
| `lib/history.py` | 51 | Appends one-line CSV summaries to a persistent history file |
| `lib/config.py` | 33 | Loads `config.json` with safe defaults for every field |
| `lib/combos.py` | 17 | Defines the 12 modifier+key combinations to test |

---

## Keyboard Layouts

| Layout | Key Labels | Notes |
|:-------|:-----------|:------|
| Canadian English | English labels (Backspace, Enter, Shift, Space, Delete, etc.) | Standard QWERTY |
| Canadian French | French labels (Retour, Entree, Maj, Espace, Suppr, Echap, etc.) | QWERTY with French Canadian key names and AltCar |
| Spanish (Latin America) | Spanish labels (Retro, Intro, Mayus, Espacio, Supr, etc.) | QWERTY with Ñ key and AltGr |

All layouts include: Esc, F1–F12, PrtSc, ScrLk, Pause, full alphanumeric rows, navigation cluster (Ins, Home, PgUp, Del, End, PgDn), and arrow keys. Numpad is available as an optional toggle for models that have one.

---

## Author

**Andres Villarreal** ([@4vs3c](https://github.com/AndresVGu))

---

<p align="center">
  <sub>Built for the refurb & QA team</sub>
</p>
