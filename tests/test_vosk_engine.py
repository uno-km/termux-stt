import sys

from termux_stt import create_engine
from termux_stt.engine.vosk_engine import VoskEngine


def test_vosk_engine_creation():
    engine = create_engine("vosk", model="small-ko-0.22", lang="ko")
    assert isinstance(engine, VoskEngine)
    assert engine.config.lang == "ko"
    assert engine.model_name == "small-ko-0.22"

    info = engine.get_info()
    assert info["name"] == "Vosk"
    assert info["model"] == "small-ko-0.22"
    assert info["language"] == "ko"
    assert "spk_model_loaded" in info


def test_vosk_platform_spoofing():
    # Calling _spoof_platform should run safely without altering desktop platforms
    current_platform = sys.platform
    VoskEngine._spoof_platform()
    # In non-termux testing environment, platform should remain stable
    assert isinstance(sys.platform, str)
    assert current_platform == sys.platform
