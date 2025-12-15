import platform
import psutil
import sys
import datetime

def collect_info_system():
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Python": sys.version
    }
    
def collect_info_cpu():
    return {
        "Coeurs physiques": psutil.cpu_count(False),
        "Coeurs logiques": psutil.cpu_count(),
        "Pourcentage d'utilisation": psutil.cpu_percent()
    }
    
def collect_info_memory():
    total = round(psutil.virtual_memory().total / 1024 ** 3, 2)
    used = round(psutil.virtual_memory().used / 1024 ** 3, 2)
    percent = round(used/total*100, 2)
    return {
        "Total": psutil.virtual_memory().total,
        "Disponible": psutil.virtual_memory().available,
        "Pourcentage d'utilisation": percent
    }
    
def collect_info_disk():
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_info[partition.mountpoint] = usage.percent
    return disk_info

def collect_all_info():
    return {
        "system": collect_info_system(),
        "cpu": collect_info_cpu(),
        "memory": collect_info_memory(),
        "disk": collect_info_disk(),
        "timestamp": datetime.datetime.now().isoformat()
    }