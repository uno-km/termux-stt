"""
Hardware detection for Termux Android devices.
"""

import multiprocessing
import os
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

# [B방안] Platform SSOT: ameva-runtime.platform 에서 공유 구현을 가져옵니다.
try:
    from ameva_runtime.vulkan.platform import is_termux as _ameva_is_termux
    _AMEVA_PLATFORM_AVAILABLE = True
except ImportError:
    _AMEVA_PLATFORM_AVAILABLE = False


def is_termux() -> bool:
    """Check if running inside Termux.

    [B방안] ameva-runtime.platform.is_termux() 를 SSOT 로 사용하며,
    미설치 환경에서는 인라인 구현으로 안전하게 폴백합니다.
    """
    if _AMEVA_PLATFORM_AVAILABLE:
        return _ameva_is_termux()
    prefix = os.environ.get("PREFIX", "")
    return "com.termux" in prefix or "TERMUX_VERSION" in os.environ or os.path.exists("/data/data/com.termux")

def get_ram_info() -> Tuple[int, int]:
    """Get total and available RAM in MB using /proc/meminfo."""
    import logging
    total, available = 0, 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total = int(line.split()[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    available = int(line.split()[1]) // 1024
    except Exception as e:
        logging.getLogger("termux_stt.platform.hardware").debug(
            "[termux-stt] /proc/meminfo 읽기 실패 (비 Linux 환경에서 정상): %s", e
        )
    return total, available

def check_neon_support() -> bool:
    """Check for ARM NEON support."""
    import logging
    try:
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()
            return "neon" in content.lower() or "asimd" in content.lower()
    except Exception as e:
        logging.getLogger("termux_stt.platform.hardware").debug(
            "[termux-stt] NEON 지원 확인 실패 (/proc/cpuinfo 접근 불가): %s", e
        )
        return False

def check_fp16_support() -> bool:
    """Check for FP16 support (asimdhp/fphp)."""
    import logging
    try:
        with open("/proc/cpuinfo", "r") as f:
            content = f.read()
            return "fphp" in content.lower() or "asimdhp" in content.lower()
    except Exception as e:
        logging.getLogger("termux_stt.platform.hardware").debug(
            "[termux-stt] FP16 지원 확인 실패 (/proc/cpuinfo 접근 불가): %s", e
        )
        return False

def get_optimal_threads() -> int:
    """Get optimal thread count (typically based on big cores)."""
    cores = multiprocessing.cpu_count()
    # Simple heuristic: assume half are big cores on modern big.LITTLE ARM
    big_cores = max(1, cores // 2)
    return big_cores

def detect_hardware() -> HardwareInfo:
    """Detect comprehensive hardware info.

    반환 값의 타입·구조는 변경 없습니다. cpu_model 필드가 'Unknown ARM' 고정값에서
    /proc/cpuinfo 기반 실제 SoC 명칭으로 개선됩니다.
    """
    import logging as _log
    _logger = _log.getLogger("termux_stt.platform.hardware")

    cores = multiprocessing.cpu_count()
    big_cores = get_optimal_threads()
    little_cores = cores - big_cores

    total_ram, avail_ram = get_ram_info()
    termux_env = is_termux()
    android_env = hasattr(os, "uname") and "android" in os.uname().release.lower()
    if termux_env:
        android_env = True

    # SoC 명칭 탐지 — /proc/cpuinfo 에서 Hardware 또는 model name 필드를 읽습니다.
    cpu_model = "Unknown ARM"
    soc_name = "Unknown SoC"
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line_l = line.lower()
                    if line.startswith("Hardware") or line.startswith("hardware"):
                        # Hardware	: Qualcomm Technologies, Inc SM8650
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            cpu_model = parts[1].strip()
                    if "exynos" in line_l or "s5e" in line_l:
                        soc_name = "Samsung Exynos"
                    elif "qualcomm" in line_l or "qcom" in line_l or "snapdragon" in line_l:
                        soc_name = "Qualcomm Snapdragon"
                    elif "mediatek" in line_l or "dimensity" in line_l:
                        soc_name = "MediaTek Dimensity"
                    elif "tensor" in line_l:
                        soc_name = "Google Tensor"
        except Exception as e:
            _logger.debug(
                "[termux-stt] /proc/cpuinfo SoC 탐지 실패 (비 Linux 환경에서 정상): %s", e
            )

    return HardwareInfo(
        cpu_model=cpu_model,
        cpu_cores=cores,
        big_cores=big_cores,
        little_cores=little_cores,
        neon_support=check_neon_support(),
        fp16_support=check_fp16_support(),
        ram_total_mb=total_ram,
        ram_available_mb=avail_ram,
        soc_name=soc_name,
        is_termux=termux_env,
        is_android=android_env
    )
