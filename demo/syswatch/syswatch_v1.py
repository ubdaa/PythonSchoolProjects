import platform
import psutil
import sys

def get_system_info():
    print("\n=== Système ===")
    print("OS:", platform.system())
    print("Version:", platform.version())
    print("Architecture:", platform.machine())
    print("Hostname:", platform.node())
    print("Python:", sys.version)
    
def get_cpu_info():
    print("\n=== CPU ===")
    print("Coeurs physiques:", psutil.cpu_count(False))
    print("Coeurs logique:", psutil.cpu_count())
    print("Utilisation:", psutil.cpu_percent())
    
def get_memory_info():
    total = round(psutil.virtual_memory().total / 1024 ** 3, 2)
    available = round(psutil.virtual_memory().available / 1024 ** 3, 2)
    used = round(psutil.virtual_memory().used / 1024 ** 3, 2)
    percent = round(used/total*100, 2)
    print("\n=== Mémoire ===")
    print("Total:", total, "GB")
    print("Disponible:", available, "GB")
    print("Utilisation:", percent, "%")
    
def get_disk_info():
    print("\n=== Disques ===")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        percent = usage.percent
        print(f"{partition.mountpoint} : {percent}%")
    
def main():
    print("=== SysWatch v1.0 ===")
    get_system_info()
    get_cpu_info()
    get_memory_info()
    get_disk_info()