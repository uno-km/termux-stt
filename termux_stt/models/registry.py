"""
Model registry containing known models for termux-stt engines.
"""

from typing import Any, Dict, List, Optional

__all__ = ["MODEL_REGISTRY", "get_model_info", "list_models", "get_default_model"]

MODEL_REGISTRY = {
    "whisper": {
        "tiny": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin", "sha256": "bd577a113a864445d4c299885e8aa97a4ec15870aa3722d35473bced96c437a6", "size": "75MB", "description": "Whisper Tiny (ggml)"},
        "tiny.en": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.en.bin", "sha256": "c78c4921dd286128114549337d34b2bbec4b638205f3e949131682493f96d65a", "size": "75MB", "description": "Whisper Tiny English (ggml)"},
        "base": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin", "sha256": "60ed5bc3dd14eea856493d334349b405782ddcaf00eec4ad1043704778400e77", "size": "142MB", "description": "Whisper Base (ggml)"},
        "base.en": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin", "sha256": "a34b55c23f94f083e94e8b80430a34c302258c8e77b4ffebc63c1c5259fb3568", "size": "142MB", "description": "Whisper Base English (ggml)"},
        "small": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.bin", "sha256": "55356645c2b361a969dfd0ef2c5a50d530afd4d144ff57896067204592d89e8a", "size": "466MB", "description": "Whisper Small (ggml)"},
        "small.en": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin", "sha256": "c4aa02e078a876798e29a918a994ef550f2420f1883be792e352ef16b9b66236", "size": "466MB", "description": "Whisper Small English (ggml)"},
        "small-q5_1": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small-q5_1.bin", "sha256": "", "size": "182MB", "description": "Whisper Small Q5_1 (Quantized)"},
        "medium": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin", "sha256": "fd9727b6e129260e44f2fb332c63796f2e6bc0484412f080039986deec3a5fe0", "size": "1.5GB", "description": "Whisper Medium (ggml)"},
        "medium.en": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin", "sha256": "8c30f0e44ce9560e629497ac5238042a904fb5b3e4174e2d2243ee9777615022", "size": "1.5GB", "description": "Whisper Medium English (ggml)"},
        "medium-q5_0": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium-q5_0.bin", "sha256": "", "size": "539MB", "description": "Whisper Medium Q5_0 (Quantized)"},
        "large-v3-turbo": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin", "sha256": "4b681dbbf0e8549beee9659b664d4b1a432579b4a4fae1fa4662d515a4ec7316", "size": "1.6GB", "description": "Whisper Large-v3-Turbo (Ultra-Accuracy)"},
        "large-v3-turbo-q5_0": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin", "sha256": "", "size": "560MB", "description": "Whisper Large-v3-Turbo Q5_0 (Quantized)"},
        "large-v3": {"url": "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin", "sha256": "ad82bf6a904323aa02c2e078345c2253a699c647b0a8801267493fa01f5fec42", "size": "3.1GB", "description": "Whisper Large-v3 (Full Precision)"},
    },
    "vosk": {
        "small-ko-0.22": {"url": "https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip", "sha256": "", "size": "42MB", "description": "Vosk Small Korean"},
        "model-spk-0.4": {"url": "https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip", "sha256": "", "size": "13MB", "description": "Vosk Speaker Identification"}
    },
    "sherpa": {
        "zipformer-ko": {"url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-streaming-zipformer-korean-2024-06-24.tar.bz2", "sha256": "", "size": "185MB", "description": "Sherpa ONNX Zipformer Korean"},
        "sensevoice-small": {"url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17.tar.bz2", "sha256": "", "size": "230MB", "description": "SenseVoice Small ONNX Multi-Language"},
        "3dspeaker-campplus": {"url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/3dspeaker_speech_campplus_sv_zh-cn_16k-common.onnx", "sha256": "", "size": "28MB", "description": "3D Speaker CampPlus Embedding"},
        "silero-vad": {"url": "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/silero_vad.onnx", "sha256": "", "size": "2MB", "description": "Silero VAD ONNX Model"}
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
