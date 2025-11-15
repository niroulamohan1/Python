#!/usr/bin/env python3
"""
Env + Config Validator and Runner
Python 3.9+
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import smtplib

# --- Configuration ---
REQUIRED_ENV_VARS = {
    "APP_ENV": "production",
    "APP_CONFIG": "/etc/myapp/config.yaml"
}
CONFIG_FILES = [
    Path("/etc/myapp/config.yaml"),
    Path("/etc/myapp/secret.key")
]
SCRIPT_TO_RUN = "/usr/local/bin/myapp_start.sh"

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


def check_and_set_env_vars(required_vars: dict):
    load_dotenv()  # load from .env file
    missing = []
    for key, default in required_vars.items():
        if not os.getenv(key):
            os.environ[key] = default
            missing.append(key)
            send_email_alert("Missing Env Var", f"{key} was missing, set to default {default}")
    return missing


def validate_config_files(files):
    missing = []
    for f in files:
        if not f.exists() or not f.is_file():
            missing.append(str(f))
            send_email_alert("Missing Config File", f"Config file missing: {f}")
    return missing


def run_script(script_path: str):
    try:
        subprocess.run([script_path], check=True)
        print(f"Successfully ran {script_path}")
    except subprocess.CalledProcessError as e:
        send_email_alert("Script Execution Failed", f"Failed to run {script_path}: {e}")
        sys.exit(1)


def main():
    missing_env = check_and_set_env_vars(REQUIRED_ENV_VARS)
    missing_files = validate_config_files(CONFIG_FILES)

    if missing_env or missing_files:
        print("Validation failed, not running script.")
        sys.exit(1)

    run_script(SCRIPT_TO_RUN)


if __name__ == "__main__":
    main()
