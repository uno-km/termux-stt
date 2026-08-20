from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SpeakerEmbedding:
    start: float
    end: float
    vector: List[float]
    dimension: int = 128

class XVectorExtractor:
    """Vosk X-Vector Extraction Interface."""

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        # Model loading is deferred to extraction time or handled by VoskEngine

    def extract(self, audio_path: str, chunk_sec: float = 2.0) -> List[SpeakerEmbedding]:
        """
        Extract X-Vectors from audio file.
        In a full implementation, this would delegate to VoskEngine.
        """
        # Placeholder for integration with VoskEngine's extract_xvectors
        # e.g. return self.vosk_engine.extract_xvectors(audio_path, chunk_sec)
        return []
