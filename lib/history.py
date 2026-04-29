"""Append test results to a CSV history file."""

import csv
from datetime import datetime
from pathlib import Path


HEADER = [
    "date", "model", "serial", "layout", "duration_s",
    "total_keys", "tested", "missing", "stuck", "ghost", "bounce",
    "combos_passed", "combos_total", "avg_latency_ms", "status",
]


def append_history(history_file, sys_info, layout_name, elapsed_secs,
                   all_keys, tested_keys, stuck_keys, ghost_keys, bounce_keys,
                   combos_passed, combos_total, latencies):
    """Append one row to the history CSV. Creates file + header if missing."""
    path = Path(history_file)
    write_header = not path.exists()

    total = len(all_keys)
    tested = len(tested_keys & set(all_keys))
    missing = total - tested
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    passed = (tested == total and not stuck_keys and not ghost_keys
              and not bounce_keys and combos_passed == combos_total)

    row = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model": sys_info.get("model", "Unknown"),
        "serial": sys_info.get("serial", "Unknown"),
        "layout": layout_name,
        "duration_s": int(elapsed_secs),
        "total_keys": total,
        "tested": tested,
        "missing": missing,
        "stuck": len(stuck_keys),
        "ghost": len(ghost_keys),
        "bounce": len(bounce_keys),
        "combos_passed": combos_passed,
        "combos_total": combos_total,
        "avg_latency_ms": f"{avg_lat:.1f}",
        "status": "PASS" if passed else "FAIL",
    }

    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
