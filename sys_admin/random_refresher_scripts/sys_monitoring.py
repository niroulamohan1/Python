import os
import shutil
import subprocess
from pathlib import Path
import logging
from datetime import datetime

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(
    filename="system_report.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

REPORT_FILE = Path("system_report.txt")

# ----------------------------
# Utility functions
# ----------------------------

def get_disk_usage(path="/"):
    """Return disk usage statistics for a given path."""
    usage = shutil.disk_usage(path)
    return {
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
        "percent_used": round((usage.used / usage.total) * 100, 2)
    }

def list_large_files(directory, size_limit=50*1024*1024):
    """List files larger than size_limit (default 50 MB)."""
    folder = Path(directory)
    large_files = []
    for item in folder.rglob("*"):
        if item.is_file() and item.stat().st_size > size_limit:
            large_files.append((item, item.stat().st_size))
    return large_files

def run_system_command(command):
    """Run a system command and return its output."""
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def generate_report():
    """Generate a system monitoring report."""
    logging.info("Generating system report...")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Disk usage
    disk = get_disk_usage("/")
    disk_report = (
        f"Disk Usage:\n"
        f"  Total: {disk['total'] // (1024**3)} GB\n"
        f"  Used: {disk['used'] // (1024**3)} GB\n"
        f"  Free: {disk['free'] // (1024**3)} GB\n"
        f"  Percent Used: {disk['percent_used']}%\n"
    )

    # Environment info
    env_report = (
        f"Environment Info:\n"
        f"  Current Directory: {os.getcwd()}\n"
        f"  User: {os.getenv('USERNAME') or os.getenv('USER')}\n"
    )

    # Large files
    large_files = list_large_files(".")
    files_report = "Large Files (>50MB):\n"
    if large_files:
        for file, size in large_files:
            files_report += f"  {file} - {size // (1024**2)} MB\n"
    else:
        files_report += "  None found\n"

    # Example system command
    uptime = run_system_command("uptime" if os.name != "nt" else "systeminfo | findstr /C:\"System Boot Time\"")

    # Build full report
    report = (
        f"System Report - {now}\n"
        f"{'-'*40}\n"
        f"{disk_report}\n"
        f"{env_report}\n"
        f"{files_report}\n"
        f"System Uptime:\n  {uptime}\n"
    )

    # Save to file
    REPORT_FILE.write_text(report)
    logging.info("System report generated successfully.")
    print(report)

# ----------------------------
# Main workflow
# ----------------------------
if __name__ == "__main__":
    print("System Monitoring Script Running...")
    generate_report()
    print(f"Report saved to {REPORT_FILE.resolve()}")
