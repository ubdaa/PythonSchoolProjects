from dataclasses import dataclass
from datetime import datetime
import psutil

@dataclass
class SystemMetrics():
    timestamp: datetime
    hostname: str
    cpu_percent: float
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_usage: dict
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "hostname": self.hostname,
            "cpu_percent": self.cpu_percent,
            "memory_total": self.memory_total,
            "memory_available": self.memory_available,
            "memory_percent": self.memory_percent,
            "disk_usage": self.disk_usage
        }
        
    def __str__(self):
        return (f"Timestamp: {self.timestamp}, Hostname: {self.hostname}, "
                f"CPU Usage: {self.cpu_percent}%, "
                f"Memory: {self.memory_available}/{self.memory_total} ({self.memory_percent}%), "
                f"Disk Usage: {self.disk_usage}")
        
@dataclass
class SystemCollector():
    hostname: str
    
    def __init__(self, hostname: str):
        self.hostname = hostname
        
    def collect(self) -> SystemMetrics:
        cpu_percent = psutil.cpu_percent()
        virtual_mem = psutil.virtual_memory()
        memory_total = virtual_mem.total
        memory_available = virtual_mem.available
        memory_percent = virtual_mem.percent
        
        disk_usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = usage.percent
            except PermissionError:
                continue
            
        return SystemMetrics(
            timestamp=datetime.now(),
            hostname=self.hostname,
            cpu_percent=cpu_percent,
            memory_total=memory_total,
            memory_available=memory_available,
            memory_percent=memory_percent,
            disk_usage=disk_usage
        )