"""Export keyboard test results to a text report."""

import subprocess
from datetime import datetime
from pathlib import Path


def get_system_info():
    """Gather machine model and serial via dmidecode."""
    info = {"model": "Unknown", "serial": "Unknown"}
    try:
        r = subprocess.run(
            ["sudo", "dmidecode", "-s", "system-product-name"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0 and r.stdout.strip():
            info["model"] = r.stdout.strip()
    except Exception:
        pass
    try:
        r = subprocess.run(
            ["sudo", "dmidecode", "-s", "system-serial-number"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0 and r.stdout.strip():
            info["serial"] = r.stdout.strip()
    except Exception:
        pass
    return info


def export_report(layout_name, all_keys, tested_keys, stuck_keys, ghost_keys, latencies,
                  combos_total=0, combos_passed=0, combos_missing=None,
                  elapsed_secs=0, bounce_keys=None, press_counts=None, output_dir=None):
    """Generate a .txt QA report file. Returns the file path."""
    if output_dir is None:
        output_dir = Path.home() / "Downloads"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    sys_info = get_system_info()
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"keytest_report_{timestamp}.txt"
    filepath = output_dir / filename

    total = len(all_keys)
    tested = len(tested_keys)
    missing = [k for k in all_keys if k not in tested_keys]
    stuck_list = list(stuck_keys)
    ghost_list = list(ghost_keys)
    bounce_list = list(bounce_keys) if bounce_keys else []
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    passed = (tested == total and len(stuck_list) == 0
              and len(ghost_list) == 0 and len(bounce_list) == 0
              and combos_passed == combos_total)

    mins, secs = divmod(int(elapsed_secs), 60)

    lines = [
        "=" * 55,
        "       KEYBOARD TEST REPORT",
        "=" * 55,
        "",
        f"  Date        : {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Model       : {sys_info['model']}",
        f"  Serial      : {sys_info['serial']}",
        f"  Layout      : {layout_name}",
        f"  Duration    : {mins:02d}:{secs:02d}",
        "",
        "-" * 55,
        "  RESULTS",
        "-" * 55,
        "",
        f"  Total keys  : {total}",
        f"  Tested      : {tested}",
        f"  Missing     : {len(missing)}",
        f"  Stuck       : {len(stuck_list)}",
        f"  Ghost       : {len(ghost_list)}",
        f"  Bouncing    : {len(bounce_list)}",
        f"  Avg latency : {avg_latency:.1f} ms",
        "",
        f"  Combos      : {combos_passed}/{combos_total}",
        "",
        f"  STATUS      : {'PASS' if passed else 'FAIL'}",
        "",
    ]

    if missing:
        lines += ["-" * 55, "  MISSING KEYS", "-" * 55, ""]
        for i in range(0, len(missing), 8):
            chunk = missing[i:i + 8]
            lines.append("  " + ", ".join(chunk))
        lines.append("")

    if stuck_list:
        lines += ["-" * 55, "  STUCK KEYS", "-" * 55, ""]
        lines.append("  " + ", ".join(stuck_list))
        lines.append("")

    if ghost_list:
        lines += ["-" * 55, "  GHOST KEYS (possible short circuit)", "-" * 55, ""]
        lines.append("  " + ", ".join(ghost_list))
        lines.append("")

    if bounce_list:
        lines += ["-" * 55, "  BOUNCING KEYS (intermittent contact)", "-" * 55, ""]
        lines.append("  " + ", ".join(bounce_list))
        lines.append("")

    if press_counts:
        multi = {k: v for k, v in press_counts.items() if v > 1}
        if multi:
            lines += ["-" * 55, "  MULTI-PRESS KEYS (pressed more than once)", "-" * 55, ""]
            for k, v in sorted(multi.items(), key=lambda x: -x[1]):
                lines.append(f"  {k:<16} x{v}")
            lines.append("")

    if combos_missing:
        lines += ["-" * 55, "  MISSING COMBOS", "-" * 55, ""]
        for c in combos_missing:
            lines.append(f"  {c}")
        lines.append("")

    lines += ["=" * 55, ""]

    filepath.write_text("\n".join(lines))
    return str(filepath)
