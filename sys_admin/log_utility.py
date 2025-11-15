#!/usr/bin/env python3
"""
Log Utility with Size + Time Rotation
Python 3.9+
"""

import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
import smtplib

# --- Configuration ---
LOG_FILE = Path("/var/log/myapp/app.log")
LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB
LOG_BACKUP_COUNT = 3
LOG_DAILY_BACKUP_COUNT = 7

# Alert settings (email)
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your_username"
SMTP_PASS = "your_password"
EMAIL_FROM = "monitor@example.com"
EMAIL_TO = "admin@example.com"


def send_email_alert(subject: str, message: str):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, f"Subject: {subject}\n\n{message}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")


def setup_logger(log_file: Path):
    try:
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger("myapp")
        logger.setLevel(logging.INFO)

        # Size-based rotation
        size_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT
        )

        # Daily rotation
        time_handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=LOG_DAILY_BACKUP_COUNT
        )

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        size_handler.setFormatter(formatter)
        time_handler.setFormatter(formatter)

        logger.addHandler(size_handler)
        logger.addHandler(time_handler)

        return logger
    except Exception as e:
        send_email_alert("Logging Setup Failed", f"Failed to configure logging: {e}")
        raise


def main():
    logger = setup_logger(LOG_FILE)
    for i in range(1000):
        logger.info(f"Log entry {i}")


if __name__ == "__main__":
    main()
