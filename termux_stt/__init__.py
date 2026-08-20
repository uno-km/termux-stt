"""
termux-stt — Android on-device STT framework for Termux.

Unified interface for whisper.cpp, vosk, and sherpa-onnx with built-in
speaker diarization, real-time microphone streaming, and hybrid pipelines.

Quick Start
-----------
>>> from termux_stt import create_engine
>>> engine = create_engine("whisper", model="base", lang="ko")
>>> result = engine.transcribe("meeting.wav")
>>> print(result.text)
"""

__version__ = '1.0.0'
__author__ = 'Eunho Kim (@uno-km)'


def create_engine(
    engine: str = "whisper",
    *,
    model: str = None,
    lang: str = "ko",
    num_speakers: int = 0,
    threads: int = None,
    vad: bool = True,
    vad_threshold: float = 0.5,
    quantization: str = "q5_1",
    custom_model_path: str = None,
    **kwargs,
):
    """Create an STT engine instance.

    Parameters
    ----------
    engine : str
        ``"whisper"`` | ``"vosk"`` | ``"sherpa"`` | ``"hybrid"``
    model : str, optional
        ``"tiny"`` | ``"base"`` | ``"small"`` | ``"medium"`` | ``"custom"``
    lang : str
        ISO 639-1 language code. Default ``"ko"``.
    num_speakers : int
        ``0`` = no diarization, ``2+`` = enable speaker diarization.
    threads : int, optional
        CPU thread count. ``None`` = auto-detect big-cores.
    vad : bool
        Enable Silero-VAD silence filtering. Default ``True``.
    vad_threshold : float
        VAD sensitivity (0.0–1.0). Default ``0.5``.
    quantization : str
        GGML quantization: ``"f16"`` | ``"q8_0"`` | ``"q5_1"`` | ``"q4_0"``.
    custom_model_path : str, optional
        Path to a custom fine-tuned model.
    **kwargs
        Additional engine-specific options.

    Returns
    -------
    Engine
        A ready-to-use engine instance with ``transcribe()``,
        ``stream_mic()``, ``diarize()``, and more.

    Examples
    --------
    >>> engine = create_engine("whisper", model="base", lang="ko")
    >>> result = engine.transcribe("meeting.wav")

    >>> engine = create_engine("hybrid", lang="ko", num_speakers=2)
    >>> result = engine.diarize("interview.wav")
    """
    from .engine import EngineRegistry

    return EngineRegistry.get_engine(
        engine,
        model=model,
        lang=lang,
        num_speakers=num_speakers,
        threads=threads,
        vad=vad,
        vad_threshold=vad_threshold,
        quantization=quantization,
        custom_model_path=custom_model_path,
        **kwargs,
    )


__all__ = [
    'create_engine',
    '__version__',
    '__author__',
]
