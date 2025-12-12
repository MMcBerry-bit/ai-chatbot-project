"""
Watchdog Timer for AI Chatbot
Monitors app health and prevents/recovers from hangs
"""

import threading
import time
import logging
from datetime import datetime, timedelta

class AppWatchdog:
    def __init__(self, timeout_seconds=30, check_interval=5):
        """
        Initialize watchdog timer
        
        Args:
            timeout_seconds: How long without heartbeat before considering app hung
            check_interval: How often to check for heartbeat (seconds)
        """
        self.timeout_seconds = timeout_seconds
        self.check_interval = check_interval
        self.last_heartbeat = datetime.now()
        self.running = False
        self.thread = None
        self.on_timeout_callback = None
        self.enabled = True
        
        # Setup logging
        logging.basicConfig(
            filename='ai_chatbot_watchdog.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def start(self, on_timeout=None):
        """
        Start the watchdog timer
        
        Args:
            on_timeout: Callback function to execute if timeout detected
        """
        if self.running:
            return
            
        self.on_timeout_callback = on_timeout
        self.running = True
        self.last_heartbeat = datetime.now()
        
        self.thread = threading.Thread(target=self._monitor, daemon=True)
        self.thread.start()
        
        self.logger.info(f"Watchdog started (timeout: {self.timeout_seconds}s)")
        
    def stop(self):
        """Stop the watchdog timer"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        self.logger.info("Watchdog stopped")
        
    def heartbeat(self):
        """
        Send heartbeat signal to indicate app is alive
        Call this regularly from your main application loop
        """
        if self.enabled:
            self.last_heartbeat = datetime.now()
        
    def disable_temporarily(self, duration_seconds=60):
        """
        Disable watchdog temporarily for long operations
        
        Args:
            duration_seconds: How long to disable watchdog
        """
        self.enabled = False
        self.logger.info(f"Watchdog disabled for {duration_seconds}s")
        
        def re_enable():
            time.sleep(duration_seconds)
            self.enabled = True
            self.last_heartbeat = datetime.now()
            self.logger.info("Watchdog re-enabled")
            
        threading.Thread(target=re_enable, daemon=True).start()
        
    def _monitor(self):
        """Internal monitoring loop"""
        consecutive_timeouts = 0
        
        while self.running:
            time.sleep(self.check_interval)
            
            if not self.enabled:
                continue
                
            # Check if heartbeat is recent
            time_since_heartbeat = datetime.now() - self.last_heartbeat
            
            if time_since_heartbeat.total_seconds() > self.timeout_seconds:
                consecutive_timeouts += 1
                self.logger.warning(
                    f"Watchdog timeout detected! No heartbeat for "
                    f"{time_since_heartbeat.total_seconds():.1f}s "
                    f"(timeout #{consecutive_timeouts})"
                )
                
                # Execute callback if provided
                if self.on_timeout_callback:
                    try:
                        self.on_timeout_callback(consecutive_timeouts)
                    except Exception as e:
                        self.logger.error(f"Timeout callback error: {e}")
                        
                # Reset heartbeat to avoid repeated callbacks
                self.last_heartbeat = datetime.now()
            else:
                # Reset timeout counter on successful heartbeat
                if consecutive_timeouts > 0:
                    self.logger.info("App recovered, resetting timeout counter")
                consecutive_timeouts = 0


class OperationMonitor:
    """Monitor individual operations for timeouts"""
    
    def __init__(self, name, timeout_seconds=30):
        self.name = name
        self.timeout_seconds = timeout_seconds
        self.start_time = None
        self.logger = logging.getLogger(__name__)
        
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Operation started: {self.name}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return False
            
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if duration > self.timeout_seconds:
            self.logger.warning(
                f"Operation '{self.name}' took {duration:.1f}s "
                f"(timeout threshold: {self.timeout_seconds}s)"
            )
        else:
            self.logger.info(f"Operation completed: {self.name} ({duration:.1f}s)")
            
        return False  # Don't suppress exceptions


# Singleton instance
_watchdog = None

def get_watchdog():
    """Get global watchdog instance"""
    global _watchdog
    if _watchdog is None:
        _watchdog = AppWatchdog()
    return _watchdog
