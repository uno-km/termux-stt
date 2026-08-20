import pytest
import os
import tempfile

@pytest.fixture
def sample_audio_path():
    return "dummy_audio.mp3"

@pytest.fixture
def sample_wav_path():
    return "dummy_audio.wav"

@pytest.fixture
def tmp_output_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d
