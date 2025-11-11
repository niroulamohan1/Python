from pathlib import Path
import os
import time

# === CONFIG ===
LOG_DIR = Path(os.getenv('LOG_DIR', '/tmp'))
MAX_AGE_DAYS = int(os.getenv('MAX_LOG_AGE_DAYS', '7'))

#base_dir = Path.home()
#config_path = base_dir / 'PycharmProjects' / 'Python' / 'README.md'
base_dir = Path(__file__).resolve().parent.parent
config_path = base_dir / 'README.md'

if config_path.exists():
    print("Config found:", config_path)

def cleanup_logs():
    print(f"\nCleaning logs older than {MAX_AGE_DAYS} days in {LOG_DIR}...")
    cutoff = time.time() - (MAX_AGE_DAYS * 86400)

    if not LOG_DIR.exists():
        print("Log directory does not exist:", LOG_DIR)
        return

    deleted = 0
    for file_path in LOG_DIR.rglob('*'):
        if file_path.is_file() and file_path.suffix == '.log':
            if file_path.stat().st_mtime < cutoff:
                try:
                    file_path.unlink()
                    print("🗑️ Deleted:", file_path)
                    deleted += 1
                except Exception as e:
                    print("Error deleting", file_path, ":", e)
    print(f"Cleanup complete. {deleted} files deleted.")

if __name__ == "__main__":
    cleanup_logs()