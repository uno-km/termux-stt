"""
AMEVA Unified Exception Hierarchy for Termux AI Engines.
Component: [STT]
"""
from typing import Optional, Any


class AmevaTermuxError(Exception):
    """Root exception for all Termux On-Device AI Engines."""
    COMPONENT_TAG = "[STT]"
    DEFAULT_CODE = "E000_UNKNOWN"

    def __init__(self, message: str, code: Optional[Any] = None, details: Optional[Any] = None):
        self.code = code or self.DEFAULT_CODE
        self.details = details
        self.raw_message = message
        super().__init__(message if message.startswith("[ERROR:") else f"{self.COMPONENT_TAG} [{self.code}] {message}")


TermuxSTTError = AmevaTermuxError


class ErrorCode:
    PLATFORM_NOT_SUPPORTED = 1
    MODEL_NOT_FOUND = 2
    AUDIO_PROCESSING_ERROR = 3
    INFERENCE_TIMEOUT = 4
    INVALID_ARGUMENT = 5
    RUNTIME_NOT_INSTALLED = 10
    VULKAN_DEVICE = 11
    UNKNOWN_ERROR = 99


class ExitCode:
    SUCCESS = 0
    FAILURE = 1
    INVALID_USAGE = 2
    NOT_FOUND = 3
    TIMEOUT = 4


class PlatformNotSupportedError(AmevaTermuxError):
    DEFAULT_CODE = ErrorCode.PLATFORM_NOT_SUPPORTED


class ModelNotFoundError(AmevaTermuxError):
    DEFAULT_CODE = ErrorCode.MODEL_NOT_FOUND


class AudioProcessingError(AmevaTermuxError):
    DEFAULT_CODE = ErrorCode.AUDIO_PROCESSING_ERROR


class InferenceTimeoutError(AmevaTermuxError):
    DEFAULT_CODE = ErrorCode.INFERENCE_TIMEOUT


class HardwareCompatibilityError(AmevaTermuxError):
    DEFAULT_CODE = "E003_HARDWARE_INCOMPATIBLE"


class RuntimeNotFoundError(AmevaTermuxError):
    DEFAULT_CODE = "E004_RUNTIME_NOT_FOUND"


class ProvisioningError(AmevaTermuxError):
    DEFAULT_CODE = "E005_PROVISIONING_FAILED"


class InferenceExecutionError(AmevaTermuxError):
    DEFAULT_CODE = "E007_INFERENCE_FAILED"


class ModelCorruptedError(AmevaTermuxError):
    DEFAULT_CODE = "E008_MODEL_CORRUPTED"


class ModelDownloadError(ProvisioningError):
    DEFAULT_CODE = "E009_MODEL_DOWNLOAD_FAILED"
