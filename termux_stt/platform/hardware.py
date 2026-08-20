"""
Hardware detection for Termux Android devices.
"""

import os
import multiprocessing
from dataclasses import dataclass
from typing import Tuple

__all__ = [
    "HardwareInfo", "detect_hardware", "get_optimal_threads", 
    "check_neon_support", "check_fp16_support", "get_ram_info", "is_termux"
]

@dataclass
class HardwareInfo:
    cpu_model: str
    cpu_cores: int
    big_cores: int
    little_cores: int
    neon_support: bool
    fp16_support: bool
    ram_total_mb: int
    ram_available_mb: int
    soc_name: str
    is_termux: bool
    is_android: bool

def is_termux() -> bool:
    """Check if running inside Termux."""
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix

def get_ram_info() -> Tuple[int, int]:
    """Get total and available RAM in MB using /proc/meminfo."""
    total, available = 0, 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total = int(line.split()[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    available = int(line.split()[1]) // 1024
    except Exception:
        pass
    return total, available

def check_neon_support() -> bool:
    """Check for ARM NEON support."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()
            return "neon" in content.lower() or "asimd" in content.lower()
    except Exception:
        return False

def check_fp16_support() -> bool:
    """Check for FP16 support (asimdhp/fphp)."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()
            return "fphp" in content.lower() or "asimdhp" in content.lower()
    except Exception:
        return False

def get_optimal_threads() -> int:
    """Get optimal thread count (typically based on big cores)."""
    cores = multiprocessing.cpu_count()
    # Simple heuristic: assume half are big cores on modern big.LITTLE ARM
    big_cores = max(1, cores // 2)
    return big_cores

def detect_hardware() -> HardwareInfo:
    """Detect comprehensive hardware info."""
    cores = multiprocessing.cpu_count()
    big_cores = get_optimal_threads()
    little_cores = cores - big_cores
    
    total_ram, avail_ram = get_ram_info()
    termux_env = is_termux()
    android_env = hasattr(os, "uname") and "android" in os.uname().release.lower()
    if termux_env:
        android_env = True
        
    return HardwareInfo(
        cpu_model="Unknown ARM",
        cpu_cores=cores,
        big_cores=big_cores,
        little_cores=little_cores,
        neon_support=check_neon_support(),
        fp16_support=check_fp16_support(),
        ram_total_mb=total_ram,
        ram_available_mb=avail_ram,
        soc_name="Unknown SoC",
        is_termux=termux_env,
        is_android=android_env
    )
