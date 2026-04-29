"""Load configuration from config.json with defaults fallback."""

import json
from pathlib import Path

DEFAULTS = {
    "default_layout": "auto",
    "sound_enabled": True,
    "stuck_timeout_ms": 3000,
    "bounce_threshold": 15,
    "flash_duration_ms": 150,
    "export_dir": "~/Downloads",
    "history_file": "~/.keytest_history.csv",
}


def load_config():
    """Load config.json from the script directory, falling back to defaults."""
    config_path = Path(__file__).parent.parent / "config.json"
    cfg = dict(DEFAULTS)
    try:
        if config_path.exists():
            with open(config_path) as f:
                user_cfg = json.load(f)
            cfg.update(user_cfg)
    except Exception:
        pass

    # Expand ~ in paths
    cfg["export_dir"] = str(Path(cfg["export_dir"]).expanduser())
    cfg["history_file"] = str(Path(cfg["history_file"]).expanduser())
    return cfg
