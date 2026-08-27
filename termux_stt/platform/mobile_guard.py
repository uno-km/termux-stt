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
    def disable_phantom_process_killer() -> bool:
        """Informational note: Phantom process killer adjustment requires manual user configuration in Android 12+ settings or adb."""
        return False

    @staticmethod
    def check_battery_optimization() -> Dict[str, Any]:
        """Check battery optimization status without privileged escalation."""
        return {"doze_active": False, "note": "Use standard Android Battery Optimization settings to exempt Termux."}

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
