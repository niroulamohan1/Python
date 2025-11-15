from prometheus_client import Gauge, start_http_server

cpu_gauge = Gauge("server_cpu_usage_percent", "CPU usage percentage")
mem_gauge = Gauge("server_memory_usage_mb", "Memory usage in MB")
disk_gauge = Gauge("server_disk_usage_gb", "Disk usage in GB")
net_sent_gauge = Gauge("server_network_sent_mb", "Network sent in MB")
net_recv_gauge = Gauge("server_network_recv_mb", "Network received in MB")

def start_exporter(port=8000):
    start_http_server(port)

def export_metrics(cpu_percent, mem_used, disk_used, bytes_sent, bytes_recv):
    cpu_gauge.set(cpu_percent)
    mem_gauge.set(mem_used)
    disk_gauge.set(disk_used)
    net_sent_gauge.set(bytes_sent)
    net_recv_gauge.set(bytes_recv)
