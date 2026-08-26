import logging
import os
import subprocess
from typing import Any, Dict

try:
    import psutil
except ImportError:
    psutil = None

logger = logging.getLogger(__name__)

class MobileGuard:
    """Handles Termux-specific device APIs: WakeLock, phantom processes, memory."""

    def __init__(self):
        self._wakelock_acquired = False

    def acquire_wakelock(self) -> bool:
        """Acquire CPU wakelock to prevent sleep."""
        try:
            res = subprocess.run(["termux-wake-lock"], capture_output=True)
            if res.returncode == 0:
                self._wakelock_acquired = True
                return True
        except Exception:
            pass
        return False

    def release_wakelock(self) -> bool:
        """Release CPU wakelock."""
        try:
            res = subprocess.run(["termux-wake-unlock"], capture_output=True)
            if res.returncode == 0:
                self._wakelock_acquired = False
                return True
        except Exception:
            pass
        return False

    @staticmethod
    def set_phantom_process_limit() -> bool:
        """Disable Android 12+ phantom process killer limit."""
        try:
            res = subprocess.run([
                "su", "-c", "device_config put activity_manager max_phantom_processes 2147483647"
            ], capture_output=True)
            return res.returncode == 0
        except Exception:
            return False

    @staticmethod
    def check_battery_optimization() -> Dict[str, Any]:
        """Check if Doze mode is active (requires dumpsys/su)."""
        try:
            res = subprocess.run(["su", "-c", "dumpsys deviceidle get deep"], capture_output=True, text=True)
            state = res.stdout.strip()
            return {"doze_active": state.lower() in ("idle", "active")}
        except Exception:
            return {"doze_active": False, "error": "requires root"}

    @staticmethod
    def monitor_memory() -> Dict[str, Any]:
        """Return memory usage of current process and system."""
        if psutil is None:
            return {
                "rss_mb": 0.0,
                "available_ram_mb": 0.0,
                "percent_used": 0.0,
            }
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        sys_mem = psutil.virtual_memory()
        return {
            "rss_mb": mem_info.rss / (1024 * 1024),
            "available_ram_mb": sys_mem.available / (1024 * 1024),
            "percent_used": sys_mem.percent,
        }

    def __enter__(self):
        self.acquire_wakelock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release_wakelock()
