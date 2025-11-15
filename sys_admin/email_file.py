#!/usr/bin/env python3
"""
Send email with attachment via authenticated SMTP relay
Python 3.9 compatible
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# --- Configuration ---
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your_username"
SMTP_PASS = "your_password"

EMAIL_FROM = "sender@example.com"
EMAIL_TO = "recipient@example.com"
EMAIL_SUBJECT = "Server Report with Attachment"
EMAIL_BODY = "Hello,\n\nPlease find the attached report.\n\nRegards,\nPython Script"

ATTACHMENT_PATH = "/path/to/report.csv"  # file to attach

def send_email():
    # Create MIME message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = EMAIL_SUBJECT
    msg.attach(MIMEText(EMAIL_BODY, "plain"))

    # Add attachment
    if os.path.exists(ATTACHMENT_PATH):
        with open(ATTACHMENT_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(ATTACHMENT_PATH)}",
        )
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
            print("Email with attachment sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()

'''
from pathlib import Path

file_path = Path("/path/to/file.txt")

if file_path.exists():
    print("File exists!")
else:
    print("File does not exist.")

p = Path("/var/log/syslog")

if p.exists():
    if p.is_file():
        print("It's a file")
    elif p.is_dir():
        print("It's a directory")
'''