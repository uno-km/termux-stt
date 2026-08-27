import pytest
import os
import tempfile
from termux_stt.models.hub import ModelHub
from termux_stt.models.registry import MODEL_REGISTRY, get_model_info, list_models, get_default_model

def test_model_registry_completeness():
    assert "whisper" in MODEL_REGISTRY
    assert "tiny" in MODEL_REGISTRY["whisper"]
    assert "large-v3-turbo" in MODEL_REGISTRY["whisper"]
    assert "vosk" in MODEL_REGISTRY
    assert "small-ko-0.22" in MODEL_REGISTRY["vosk"]

def test_get_model_info():
    info = get_model_info("whisper", "tiny")
    assert "url" in info
    assert "size" in info
    assert info["size"] == "75MB"

def test_get_default_model():
    assert get_default_model("whisper") == "tiny"
    assert get_default_model("vosk") == "small-ko-0.22"

def test_model_typo_fuzzy_recommendation():
    """Verify that an unknown model typo raises ValueError with close matches and available model list."""
    with pytest.raises(ValueError) as excinfo:
        ModelHub.ensure_model("whisper", "tniyy")
    
    err_msg = str(excinfo.value)
    assert "Model 'tniyy' is not recognized for engine 'whisper'" in err_msg
    assert "Did you mean:" in err_msg
    assert "tiny" in err_msg
    assert "Available models for 'whisper':" in err_msg
    assert "large-v3-turbo" in err_msg
