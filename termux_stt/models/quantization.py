"""
Quantization logic for Whisper.cpp models.
"""

from dataclasses import dataclass
from typing import List

__all__ = ["QUANTIZATION_LEVELS", "QuantizationInfo", "get_quantized_url", "recommend_quantization"]

QUANTIZATION_LEVELS = ["f16", "q8_0", "q5_1", "q4_0"]

@dataclass
class QuantizationInfo:
    level: str
    size_ratio: float
    accuracy_delta: float
    description: str

def get_quantized_url(model_name: str, quant_level: str) -> str:
    """Construct URL for specific quantization level for whisper.cpp models."""
    if quant_level not in QUANTIZATION_LEVELS:
        raise ValueError(f"Unknown quantization level {quant_level}")
        
    base_url = "https://huggingface.co/ggerganov/whisper.cpp/resolve/main"
    
    if quant_level == "f16":
        return f"{base_url}/ggml-{model_name}.bin"
        
    return f"{base_url}/ggml-{model_name}-{quant_level}.bin"

def recommend_quantization(available_ram_mb: int) -> str:
    """Recommend quantization level based on available RAM."""
    if available_ram_mb > 4000:
        return "f16"
    elif available_ram_mb > 2000:
        return "q8_0"
    elif available_ram_mb > 1000:
        return "q5_1"
    else:
        return "q4_0"
