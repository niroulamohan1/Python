import os
import shutil
import subprocess
from pathlib import Path
import logging
import configparser
from datetime import datetime
import psutil   # pip install psutil

# ----------------------------
# Setup logging
# ----------------------------
logging.basicConfig(
    filename="sysadmin_extended.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Load configuration
# ----------------------------
config = configparser.ConfigParser()
config.read("sysadmin_config.ini")

SOURCE_DIR = Path(config.get("Paths", "source_dir", fallback="project_folder"))
BACKUP_DIR = Path(config.get("Paths", "backup_dir", fallback="backup_folder"))
ARCHIVE_NAME = config.get("Paths", "archive_name", fallback="project_backup")

# ----------------------------
# Utility functions
# ----------------------------

def backup_files():
    """Copy files from source to backup directory."""
    logging.info("Starting backup...")
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.copytree(SOURCE_DIR, BACKUP_DIR / SOURCE_DIR.name, dirs_exist_ok=True)
    logging.info("Backup completed successfully.")

def create_archive():
    """Create a timestamped archive of the backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = f"{ARCHIVE_NAME}_{timestamp}.zip"
    shutil.make_archive(f"{ARCHIVE_NAME}_{timestamp}", "zip", BACKUP_DIR)
    logging.info(f"Archive created: {archive_file}")
    return archive_file

def list_directory(path="."):
    """Cross-platform directory listing using pathlib."""
    folder = Path(path)
    print(f"\nContents of {folder.resolve()}:")
    for item in folder.iterdir():
        type_ = "DIR" if item.is_dir() else "FILE"
        size = item.stat().st_size if item.is_file() else "-"
        print(f"{type_:4} {item.name:30} {size}")
    logging.info(f"Listed contents of {folder}")

def run_system_command(command):
    """Run a system command safely with subprocess."""
    logging.info(f"Running system command: {command}")
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(result.stdout)
    if result.stderr:
        logging.error(f"Error: {result.stderr}")
    return result

def report_system_status():
    """Report CPU, memory, and disk usage using psutil."""
    print("\n--- System Status Report ---")
    print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
    print(f"Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"Disk Usage (/): {psutil.disk_usage('/').percent}%")
    logging.info("System status reported.")

def show_environment_info():
    """Show environment variables and current working directory."""
    print("\n--- Environment Info ---")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"User: {os.getenv('USERNAME') or os.getenv('USER')}")
    print("PATH:", os.getenv("PATH"))
    logging.info("Environment info displayed.")

# ----------------------------
# Main workflow
# ----------------------------
if __name__ == "__main__":
    print("Extended Sysadmin Utility Script Running...")
    backup_files()
    archive_file = create_archive()
    list_directory(BACKUP_DIR)

    # Optional external command
    run_system_command("echo Backup complete")

    # System monitoring
    report_system_status()

    # Environment info
    show_environment_info()

    print("All tasks completed. Check sysadmin_extended.log for details.")
