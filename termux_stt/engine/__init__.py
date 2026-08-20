"""
Engine module for termux-stt.

Provides the EngineRegistry that maps engine names to their concrete
implementations and the shared base classes.
"""

from typing import Dict, Type, Any, Optional

from .base import Engine, EngineConfig

__all__ = ['EngineRegistry', 'Engine', 'EngineConfig']


class EngineRegistry:
    """Registry that maps engine names to their concrete Engine subclasses.

    Supported engine names:
        - ``"whisper"`` — whisper.cpp subprocess wrapper
        - ``"vosk"``    — Vosk CFFI/ctypes wrapper
        - ``"sherpa"``  — Sherpa-ONNX subprocess wrapper
        - ``"hybrid"``  — Vosk X-Vector + Whisper STT hybrid pipeline
    """

    _engines: Dict[str, Type[Engine]] = {}

    @classmethod
    def register(cls, name: str, engine_class: Type[Engine]) -> None:
        """Register an engine class under *name*."""
        cls._engines[name] = engine_class

    @classmethod
    def get_engine(cls, engine_name: str, **kwargs: Any) -> Engine:
        """Instantiate and return the engine identified by *engine_name*.

        Parameters
        ----------
        engine_name : str
            One of ``"whisper"``, ``"vosk"``, ``"sherpa"``, ``"hybrid"``.
        **kwargs
            Forwarded to the engine constructor via :class:`EngineConfig`.

        Returns
        -------
        Engine
            A ready-to-use engine instance.

        Raises
        ------
        ValueError
            If *engine_name* is not registered.
        """
        # Lazy-import concrete engines to avoid circular imports
        cls._ensure_builtin_engines()

        name_lower = engine_name.lower()
        if name_lower not in cls._engines:
            available = ', '.join(sorted(cls._engines.keys())) or '(none)'
            raise ValueError(
                f"Unknown engine '{engine_name}'. "
                f"Available engines: {available}"
            )

        engine_cls = cls._engines[name_lower]

        # Build EngineConfig from kwargs
        config = EngineConfig(
            engine=name_lower,
            model=kwargs.pop('model', None),
            lang=kwargs.pop('lang', 'ko'),
            threads=kwargs.pop('threads', None),
            vad=kwargs.pop('vad', True),
            vad_threshold=kwargs.pop('vad_threshold', 0.5),
            quantization=kwargs.pop('quantization', 'q5_1'),
            num_speakers=kwargs.pop('num_speakers', 0),
            custom_model_path=kwargs.pop('custom_model_path', None),
            extra=kwargs,
        )

        return engine_cls(config)

    @classmethod
    def list_engines(cls) -> list:
        """Return a list of registered engine names."""
        cls._ensure_builtin_engines()
        return sorted(cls._engines.keys())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    _builtins_loaded: bool = False

    @classmethod
    def _ensure_builtin_engines(cls) -> None:
        """Lazily register the four built-in engines."""
        if cls._builtins_loaded:
            return
        cls._builtins_loaded = True

        try:
            from .whisper_engine import WhisperEngine
            cls.register('whisper', WhisperEngine)
        except Exception:
            pass

        try:
            from .vosk_engine import VoskEngine
            cls.register('vosk', VoskEngine)
        except Exception:
            pass

        try:
            from .sherpa_engine import SherpaEngine
            cls.register('sherpa', SherpaEngine)
        except Exception:
            pass

        try:
            from .hybrid_engine import HybridEngine
            cls.register('hybrid', HybridEngine)
        except Exception:
            pass
