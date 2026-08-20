"""
Model registry containing known models for termux-stt engines.
"""

from typing import Any, Dict, List, Optional

__all__ = ["MODEL_REGISTRY", "get_model_info", "list_models", "get_default_model"]

MODEL_REGISTRY = {
    "whisper": {
        "tiny": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin", "sha256": "", "size": "75MB", "description": "Whisper Tiny (ggml)"},
        "base": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin", "sha256": "", "size": "142MB", "description": "Whisper Base (ggml)"},
        "small": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin", "sha256": "", "size": "466MB", "description": "Whisper Small (ggml)"},
        "medium": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin", "sha256": "", "size": "1.5GB", "description": "Whisper Medium (ggml)"}
    },
    "vosk": {
        "small-ko-0.22": {"url": "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip", "sha256": "", "size": "42MB", "description": "Vosk Small Korean"},
        "model-spk-0.4": {"url": "https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip", "sha256": "", "size": "13MB", "description": "Vosk Speaker Identification"}
    },
    "sherpa": {
        "zipformer-ko": {"url": "", "sha256": "", "size": "", "description": "Sherpa ONNX Zipformer Korean"},
        "sensevoice-small": {"url": "", "sha256": "", "size": "", "description": "SenseVoice Small ONNX"},
        "3dspeaker-campplus": {"url": "", "sha256": "", "size": "", "description": "3D Speaker CampPlus"},
        "silero-vad": {"url": "", "sha256": "", "size": "", "description": "Silero VAD ONNX"}
    }
}

def get_model_info(engine: str, model_name: str) -> Dict[str, Any]:
    """Get metadata for a specific model."""
    engine_models = MODEL_REGISTRY.get(engine, {})
    if model_name not in engine_models:
        raise ValueError(f"Model {model_name} for engine {engine} not found in registry.")
    return engine_models[model_name]

def list_models(engine: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all models in registry, optionally filtered by engine."""
    results = []
    for eng, models in MODEL_REGISTRY.items():
        if engine and eng != engine:
            continue
        for m_name, info in models.items():
            entry = {"engine": eng, "model_name": m_name}
            entry.update(info)
            results.append(entry)
    return results

def get_default_model(engine: str) -> str:
    """Get a default model name for a given engine."""
    defaults = {
        "whisper": "tiny",
        "vosk": "small-ko-0.22",
        "sherpa": "zipformer-ko"
    }
    return defaults.get(engine, "")
