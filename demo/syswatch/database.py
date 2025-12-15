from dataclasses import dataclass
from models import SystemMetrics
import sqlite3
import datetime

@dataclass
class MetricsDatabase:
    file_path: str
    def __init__(self, file_path: str = 'syswatch.db'):
        self.file_path = file_path
        self._init_schema()
        
    def _init_schema(self):
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    hostname TEXT,
                    cpu_percent REAL,
                    memory_total INTEGER,
                    memory_available INTEGER,
                    memory_percent REAL,
                    disk_usage TEXT
                )
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp_hostname
                ON system_metrics (timestamp, hostname)
            ''')
            conn.commit()
    
    def save(self, metrics: SystemMetrics):
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_metrics (
                    timestamp, hostname, cpu_percent,
                    memory_total, memory_available, memory_percent,
                    disk_usage
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.timestamp.isoformat(),
                metrics.hostname,
                metrics.cpu_percent,
                metrics.memory_total,
                metrics.memory_available,
                metrics.memory_percent,
                str(metrics.disk_usage)
            ))
            conn.commit()
    
    def get_latest(self, hostname: str) -> SystemMetrics | None:
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp, hostname, cpu_percent,
                       memory_total, memory_available, memory_percent,
                       disk_usage
                FROM system_metrics
                WHERE hostname = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (hostname,))
            row = cursor.fetchone()
            if row:
                timestamp, hostname, cpu_percent, memory_total, memory_available, memory_percent, disk_usage_str = row
                disk_usage = eval(disk_usage_str)
                return SystemMetrics(
                    timestamp=datetime.fromisoformat(timestamp),
                    hostname=hostname,
                    cpu_percent=cpu_percent,
                    memory_total=memory_total,
                    memory_available=memory_available,
                    memory_percent=memory_percent,
                    disk_usage=disk_usage
                )
            return None
        
    def get_statistics(self, hostname: str, start_time: datetime, end_time: datetime) -> dict:
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT AVG(cpu_percent), AVG(memory_percent)
                FROM system_metrics
                WHERE hostname = ? AND timestamp BETWEEN ? AND ?
            ''', (hostname, start_time.isoformat(), end_time.isoformat()))
            row = cursor.fetchone()
            if row:
                avg_cpu, avg_memory = row
                return {
                    "avg_cpu_percent": avg_cpu,
                    "avg_memory_percent": avg_memory
                }
            return {}
    
    def cleanup_old(self, days: int = 30):
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        with sqlite3.connect(self.file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM system_metrics
                WHERE timestamp < ?
            ''', (cutoff.isoformat(),))
            conn.commit()