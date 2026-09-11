"""Exceptions and centralized ErrorCodes for the termux-stt framework.

Strictly aligned with termux-diffusion and termux-llamacpp standards.
"""
from __future__ import annotations


class ErrorCode:
    CLI_EXCLUSIVE = "E_CLI_EXCLUSIVE_MUTEX"
    PLATFORM_UNSUPPORTED = "E_PLATFORM_UNSUPPORTED"
    AUDIO_NOT_FOUND = "E_AUDIO_NOT_FOUND"
    AUDIO_FORMAT_UNSUPPORTED = "E_AUDIO_FORMAT_UNSUPPORTED"
    AUDIO_CORRUPT = "E_AUDIO_CORRUPT"
    MODEL_NOT_FOUND = "E_MODEL_NOT_FOUND"
    MODEL_DOWNLOAD = "E_MODEL_DOWNLOAD"
    VULKAN_LOADER = "E_VULKAN_LOADER"
    VULKAN_DEVICE = "E_VULKAN_DEVICE"
    RUNTIME_NOT_INSTALLED = "E_RUNTIME_NOT_INSTALLED"
    PROCESS_TIMEOUT = "E_PROCESS_TIMEOUT"
    DIARIZATION_FAILED = "E_DIARIZATION_FAILED"


class ExitCode:
    SUCCESS = 0
    CLI_ERROR = 2
    PLATFORM_ERROR = 10
    INTEGRITY_ERROR = 20
    EXECUTION_ERROR = 30
    SELFTEST_ERROR = 40
    BUILD_ERROR = 50


class TermuxSTTError(Exception):
    """Base exception for all termux-stt errors."""

    def __init__(self, message: str, code: str = "E_UNKNOWN") -> None:
        super().__init__(message)
        self.code = code


class PlatformNotSupportedError(TermuxSTTError):
    """Raised when running on an unsupported platform or when hardware requirements are unmet."""

    def __init__(self, message: str, code: str = ErrorCode.PLATFORM_UNSUPPORTED) -> None:
        super().__init__(message, code=code)


class ModelNotFoundError(TermuxSTTError):
    """Raised when the specified STT model cannot be found locally or on Hub."""

    def __init__(self, message: str, code: str = ErrorCode.MODEL_NOT_FOUND) -> None:
        super().__init__(message, code=code)


class AudioProcessingError(TermuxSTTError):
    """Raised when audio conversion, loading, or preprocessing fails."""

    def __init__(self, message: str, code: str = ErrorCode.AUDIO_CORRUPT) -> None:
        super().__init__(message, code=code)


class InferenceTimeoutError(TermuxSTTError):
    """Raised when STT inference exceeds the maximum execution timeout."""

    def __init__(self, message: str, code: str = ErrorCode.PROCESS_TIMEOUT) -> None:
        super().__init__(message, code=code)
