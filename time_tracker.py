"""
Time Tracking Utilities
"""
import time

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.start_time = time.time()
        print("Timer started.")
    
    def stop(self):
        if self.start_time is None:
            print("Timer was not started.")
            return 0
        
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        print(f"Elapsed time: {elapsed:.2f} seconds.")
        return elapsed
