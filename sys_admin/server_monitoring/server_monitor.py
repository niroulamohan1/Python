#!/usr/bin/env python3
import psutil
import logging
import time
from alerts import check_alerts
from exporters import start_exporter, export_metrics

logging.basicConfig(
    filename="server_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    mem_used = mem.used / (1024 ** 2)
    disk_used = disk.used / (1024 ** 3)
    bytes_sent = net.bytes_sent / (1024 ** 2)
    bytes_recv = net.bytes_recv / (1024 ** 2)

    logging.info(
        f"CPU: {cpu_percent}% | "
        f"Memory: {mem_used:.2f} MB | "
        f"Disk: {disk_used:.2f} GB | "
        f"Network: Sent {bytes_sent:.2f} MB, Recv {bytes_recv:.2f} MB"
    )

    # Alerts
    check_alerts(cpu_percent)

    # Prometheus Export
    export_metrics(cpu_percent, mem_used, disk_used, bytes_sent, bytes_recv)

def monitor(interval=60):
    logging.info("Starting Linux server monitoring...")
    try:
        while True:
            log_system_metrics()
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")

if __name__ == "__main__":
    start_exporter(port=8000)  # Prometheus endpoint
    monitor(interval=60)
