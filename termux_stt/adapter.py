"""
termux_stt.adapter
===================
AMEVA Component Protocol v1 — Orchestrator Adapter (v0.8.1 호환)
"""
from __future__ import annotations

from typing import Any, AsyncIterator

from ameva_component.adapter_base import BaseOrchestratorAdapter
from termux_stt.control.component import STTControl


class STTOrchestratorAdapter(BaseOrchestratorAdapter):
    """STT (Speech-to-Text) Orchestrator Adapter.

    음성 파일 변환은 Whisper.cpp를 통해 파일 기반으로 수행됩니다.
    infer() 지원: 오디오 파일 경로를 받아 transcript를 반환합니다.
    partial / silence / decode 실패를 구분하여 반환합니다.
    """

    COMPONENT_ID = "termux-stt"

    def __init__(self, control: STTControl | None = None) -> None:
        self._control = control or STTControl()

    async def infer(self, request: dict[str, Any]) -> AsyncIterator[dict[str, Any]]:
        """STT inference: audio_path 또는 audio_bytes 기반 transcription.

        request 키:
            audio_path (str): 음성 파일 경로 (필수 또는 audio_bytes 중 하나)
            model_id (str): 사용할 모델 ID (선택, 기본값: 활성 모델)
            language (str): 언어 코드 (선택)

        반환 프레임:
            {"type": "transcript", "text": str, "final": bool, "language": str | None}
            {"type": "error", "code": str, "message": str}
        """
        audio_path = request.get("audio_path")
        if not audio_path:
            yield {
                "type": "error",
                "ok": False,
                "error": {
                    "code": "AUDIO_EMPTY",
                    "message": "audio_path is required for STT infer",
                    "operation": "infer",
                    "component_id": self.COMPONENT_ID,
                    "retryable": False,
                },
            }
            return

        if hasattr(self._control, "transcribe"):
            try:
                result = await self._control.transcribe(request)
                yield {
                    "type": "transcript",
                    "text": result.get("text", ""),
                    "final": True,
                    "language": result.get("language"),
                    "fallback_used": result.get("fallback_used", False),
                    "ok": True,
                }
            except Exception as exc:
                yield {
                    "type": "error",
                    "ok": False,
                    "error": {
                        "code": "TRANSCRIPTION_FAILED",
                        "message": str(exc),
                        "operation": "infer",
                        "component_id": self.COMPONENT_ID,
                        "retryable": True,
                    },
                }
        else:
            # transcribe()가 없는 경우 — 아직 구현되지 않음을 명시적 실패로 표시
            yield self._not_supported("infer.transcribe")


def create_adapter() -> STTOrchestratorAdapter:
    """Entry Point Factory."""
    return STTOrchestratorAdapter()
