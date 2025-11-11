import os
from os import path
import time

# === CONFIG ===
LOG_DIR = os.getenv('LOG_DIR', '/tmp')
MAX_AGE_DAYS = int(os.getenv('MAX_LOG_AGE_DAYS', '7'))

def cleanup_logs():
    print(f"\nCleaning logs older than {MAX_AGE_DAYS} days in {LOG_DIR}...")
    now = time.time()
    cutoff = now - (MAX_AGE_DAYS * 86400)

    if not path.exists(LOG_DIR):
        print("Log directory does not exist:", LOG_DIR)
        return

    deleted = 0
    for root, _, files in os.walk(LOG_DIR):
        for file in files:
            file_path = path.join(root, file)
            if path.isfile(file_path) and path.getmtime(file_path) < cutoff:
                try:
                    os.remove(file_path)
                    print("Deleted:", file_path)
                    deleted += 1
                except Exception as e:
                    print("Error deleting", file_path, ":", e)
    print(f"Cleanup complete. {deleted} files deleted.")

if __name__ == "__main__":
    cleanup_logs()