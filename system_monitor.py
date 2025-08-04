"""
System Monitoring
"""
import os
import psutil

def show_system_stats():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:' if os.name == 'nt' else '/')
        
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        print(f"Available Memory: {memory.available / (1024**3):.2f} GB")
        print(f"Available Disk Space: {disk.free / (1024**3):.2f} GB")
    except Exception as e:
        print(f"Error getting system stats: {e}")
