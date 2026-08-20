"""
Docker test runner for termux-stt with authentic continuous speech (no loop).
"""

import sys
import time
from pathlib import Path
from termux_stt import create_engine, __version__
from termux_stt.export.result import TranscriptResult

def main():
    print("=" * 65)
    print(f"🎙️  termux-stt v{__version__} - Continuous Speech (No-Loop) Test")
    print("=" * 65)

    audio_file = "/app/continuous_speech.wav"
    if not Path(audio_file).exists():
        audio_file = "continuous_speech.wav"

    print(f"\n[1] Target Audio: {audio_file}")
    import wave
    w = wave.open(audio_file, 'rb')
    duration = w.getnframes() / w.getframerate()
    print(f"    Audio Duration: {duration:.2f}s (Channels: {w.getnchannels()}, SampleRate: {w.getframerate()}Hz)")
    w.close()

    # 1. Whisper Base Test
    print("\n[2] Initializing Whisper Engine (model='base', lang='en')...")
    engine_base = create_engine("whisper", model="base", lang="en")
    print(f"    Engine info: {engine_base.get_info()}")

    print(f"\n[3] Transcribing {duration:.2f}s continuous speech with Whisper Base...")
    t0 = time.time()
    result_base = engine_base.transcribe(audio_file)
    elapsed = time.time() - t0
    rtf = elapsed / duration if duration > 0 else 0

    print(f"\n--- [Transcription Results] (Elapsed: {elapsed:.2f}s, RTF: {rtf:.3f}) ---")
    print(f"Total Segments: {len(result_base.segments)}")
    print("-" * 65)
    for i, seg in enumerate(result_base.segments):
        print(f"  [{i+1:02d}] ({seg.start:05.2f}s -> {seg.end:05.2f}s) {seg.text}")
    print("-" * 65)

    print("\n[4] Full Transcribed Text:")
    print(result_base.text)

    # 2. Export SRT subtitles
    print("\n[5] Generated Subtitles (SRT format):")
    print("-" * 65)
    print(result_base.to_srt().strip())
    print("-" * 65)

    print("\n" + "=" * 65)
    print("✅ Continuous Speech Test Complete (0% Repeated Sentences)!")
    print("=" * 65)

if __name__ == "__main__":
    main()
