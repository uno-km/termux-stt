"""
Abstract base classes for STT engines.

Every concrete engine (Whisper, Vosk, Sherpa, Hybrid) inherits from
:class:`Engine` and implements its abstract methods.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, Optional

from ..export.result import DiarizedResult, Segment, TranscriptResult

__all__ = ['Engine', 'EngineConfig']


@dataclass
class EngineConfig:
    """Configuration object passed to every engine constructor.

    Parameters
    ----------
    engine : str
        Engine identifier (``"whisper"``, ``"vosk"``, ``"sherpa"``, ``"hybrid"``).
    model : str, optional
        Model name (``"tiny"``, ``"base"``, ``"small"``, ``"medium"``, ``"custom"``).
        Defaults to the engine's own default model.
    lang : str
        ISO 639-1 language code. Default ``"ko"`` (Korean).
    threads : int, optional
        CPU threads to use. ``None`` means auto-detect (big-core count).
    vad : bool
        Enable Silero-VAD silence filtering. Default ``True``.
    vad_threshold : float
        VAD sensitivity threshold (0.0–1.0). Default ``0.5``.
    quantization : str
        GGML quantization level: ``"f16"``, ``"q8_0"``, ``"q5_1"``, ``"q4_0"``.
        Default ``"q5_1"``.
    num_speakers : int
        Number of speakers for diarization. ``0`` disables speaker
        diarization; ``2+`` activates it.
    custom_model_path : str, optional
        Absolute path to a custom / fine-tuned model file.
    extra : dict
        Catch-all for additional keyword arguments.
    """

    engine: str = 'whisper'
    model: Optional[str] = None
    lang: str = 'ko'
    threads: Optional[int] = None
    vad: bool = True
    vad_threshold: float = 0.5
    quantization: str = 'q5_1'
    num_speakers: int = 0
    custom_model_path: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    # Convenience helpers ---------------------------------------------------

    @property
    def model_name(self) -> str:
        """Return the model name, falling back to engine-specific defaults."""
        if self.model:
            return self.model
        defaults = {
            'whisper': 'base',
            'vosk': 'small-ko-0.22',
            'sherpa': 'zipformer-ko',
            'hybrid': 'base',
        }
        return defaults.get(self.engine, 'base')

    @property
    def language(self) -> str:
        """Alias for ``lang``."""
        return self.lang


class Engine(ABC):
    """Abstract Base Class for all STT engines.

    Every engine must implement the five core methods below.  The
    ``create_engine()`` factory (in ``termux_stt.__init__``) constructs the
    appropriate subclass, so callers never need to instantiate engines
    directly.

    Example
    -------
    >>> from termux_stt import create_engine
    >>> engine = create_engine("whisper", model="base", lang="ko")
    >>> result = engine.transcribe("meeting.wav")
    >>> print(result.text)
    """

    @abstractmethod
    def transcribe(self, audio_path: str, **kwargs: Any) -> TranscriptResult:
        """Transcribe an audio file and return the full result.

        Parameters
        ----------
        audio_path : str
            Path to an audio file (any format supported by ffmpeg).
        **kwargs
            Engine-specific options.

        Returns
        -------
        TranscriptResult
            Object containing *text*, *segments*, *language*, and *duration*.
        """

    @abstractmethod
    def stream_mic(
        self, duration: Optional[float] = None
    ) -> Iterator[Segment]:
        """Stream transcription from the device microphone.

        Yields :class:`Segment` objects as speech is detected.
        """

    @abstractmethod
    def stream_file(
        self, audio_path: str, chunk_sec: float = 5.0
    ) -> Iterator[Segment]:
        """Stream transcription from a file in chunks.

        Useful for very long recordings where holding the entire result
        in memory is undesirable.
        """

    @abstractmethod
    def diarize(
        self, audio_path: str, num_speakers: int = 2
    ) -> DiarizedResult:
        """Run STT **and** speaker diarization.

        Parameters
        ----------
        audio_path : str
            Path to the audio file.
        num_speakers : int
            Expected number of distinct speakers.

        Returns
        -------
        DiarizedResult
            Extends :class:`TranscriptResult` with per-segment speaker
            labels.
        """

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:
        """Return a dictionary of engine / model / hardware status info."""
