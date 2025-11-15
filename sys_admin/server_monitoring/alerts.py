import logging
import smtplib
import requests

ALERT_CPU_THRESHOLD = 90
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
EMAIL_TO = "admin@example.com"
EMAIL_FROM = "monitor@example.com"
SMTP_SERVER = "localhost"

def send_email_alert(message: str):
    with smtplib.SMTP(SMTP_SERVER) as server:
        server.sendmail(EMAIL_FROM, EMAIL_TO, f"Subject: ALERT\n\n{message}")

def send_slack_alert(message: str):
    requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def check_alerts(cpu_percent: float):
    if cpu_percent > ALERT_CPU_THRESHOLD:
        msg = f"⚠️ High CPU usage detected: {cpu_percent}%"
        logging.warning(msg)
        send_email_alert(msg)
        send_slack_alert(msg)
