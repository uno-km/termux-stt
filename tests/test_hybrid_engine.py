from termux_stt import create_engine
from termux_stt.engine.hybrid_engine import HybridEngine


def test_hybrid_engine_creation():
    engine = create_engine("hybrid", model="base", lang="ko", num_speakers=2)
    assert isinstance(engine, HybridEngine)
    assert engine.config.lang == "ko"
    assert engine.config.num_speakers == 2

    info = engine.get_info()
    assert "Hybrid" in info["name"]
    assert "whisper" in info
    assert "vosk" in info
    assert info["num_speakers"] == 2


def test_hybrid_diarize_mocked_components(monkeypatch):
    engine = create_engine("hybrid", model="base", lang="ko", num_speakers=2)
    from termux_stt.export.result import Segment, TranscriptResult

    # Mock whisper transcribe
    monkeypatch.setattr(
        engine._whisper,
        "transcribe",
        lambda wav_path, **kw: TranscriptResult(
            text="Hello world test speech",
            segments=[
                Segment(start=0.0, end=2.0, text="Hello world"),
                Segment(start=2.5, end=4.0, text="test speech"),
            ],
            language="ko",
            duration=4.0,
        ),
    )

    # Mock vosk xvector extraction
    monkeypatch.setattr(
        engine._vosk,
        "extract_xvectors",
        lambda wav_path, chunk_sec=2.0: [
            (0.0, 2.0, [1.0] * 128),
            (2.0, 4.0, [-1.0] * 128),
        ],
    )

    # Create dummy wav file
    import tempfile
    import wave
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00" * 32000)
        tmp_wav = tmp.name

    try:
        res = engine.diarize(tmp_wav, num_speakers=2)
        assert len(res.segments) == 2
        assert res.segments[0].speaker == "Speaker_0"
        assert res.segments[1].speaker == "Speaker_1"
        assert "Hello world" in res.text
    finally:
        import os
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)


def test_hybrid_diarize_xvector_failure_raises_when_fallback_disabled(monkeypatch):
    import tempfile
    import wave

    import pytest

    engine = create_engine("hybrid", model="base", lang="ko", num_speakers=2)

    monkeypatch.setattr(
        engine._vosk,
        "extract_xvectors",
        lambda wav_path, chunk_sec=2.0: (_ for _ in ()).throw(RuntimeError("vosk model missing")),
    )

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00" * 32000)
        tmp_wav = tmp.name

    try:
        with pytest.raises(RuntimeError) as excinfo:
            engine.diarize(tmp_wav, num_speakers=2, allow_fallback=False)
        assert "X-Vector speaker embedding extraction failed" in str(excinfo.value)
    finally:
        import os
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)


def test_hybrid_diarize_xvector_failure_fallback_unknown(monkeypatch):
    import tempfile
    import wave

    from termux_stt.export.result import Segment, TranscriptResult

    engine = create_engine("hybrid", model="base", lang="ko", num_speakers=2)

    monkeypatch.setattr(
        engine._vosk,
        "extract_xvectors",
        lambda wav_path, chunk_sec=2.0: (_ for _ in ()).throw(RuntimeError("vosk model missing")),
    )
    monkeypatch.setattr(
        engine._whisper,
        "transcribe",
        lambda wav_path, **kw: TranscriptResult(
            text="Fallback test speech",
            segments=[Segment(start=0.0, end=2.0, text="Fallback test speech")],
            language="ko",
            duration=2.0,
        ),
    )

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        with wave.open(tmp.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(b"\x00" * 32000)
        tmp_wav = tmp.name

    try:
        res = engine.diarize(tmp_wav, num_speakers=2, allow_fallback=True)
        assert len(res.segments) == 1
        assert res.segments[0].speaker == "Speaker_Unknown"
    finally:
        import os
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)
