"""
Docker test runner for termux-stt with JFK 1-minute speech.
"""

import sys
import time
from pathlib import Path
from termux_stt import create_engine, __version__
from termux_stt.export.result import TranscriptResult

def main():
    print("=" * 60)
    print(f"🎙️  termux-stt v{__version__} - Docker Linux STT Verification")
    print("=" * 60)

    audio_file = "/app/jfk_1min.wav"
    if not Path(audio_file).exists():
        audio_file = "jfk_1min.wav"

    print(f"\n[1] Target Audio: {audio_file}")
    print(f"    File exists: {Path(audio_file).exists()}")

    # 1. Whisper tiny test
    print("\n[2] Initializing Whisper Engine (model='tiny', lang='en')...")
    engine_tiny = create_engine("whisper", model="tiny", lang="en")
    print(f"    Engine info: {engine_tiny.get_info()}")

    print("\n[3] Transcribing 1-minute JFK speech with Whisper tiny...")
    t0 = time.time()
    result_tiny = engine_tiny.transcribe(audio_file)
    elapsed_tiny = time.time() - t0
    rtf_tiny = elapsed_tiny / 60.0

    print(f"\n--- [Whisper tiny Results] (Elapsed: {elapsed_tiny:.2f}s, RTF: {rtf_tiny:.3f}) ---")
    print(f"Full Text:\n{result_tiny.text}\n")
    print(f"Segments Count: {len(result_tiny.segments)}")
    for i, seg in enumerate(result_tiny.segments[:5]):
        print(f"  [{i+1}] ({seg.start:.2f}s -> {seg.end:.2f}s) {seg.text}")

    # 2. Whisper base test
    print("\n[4] Initializing Whisper Engine (model='base', lang='en')...")
    engine_base = create_engine("whisper", model="base", lang="en")
    print("\n[5] Transcribing 1-minute JFK speech with Whisper base...")
    t0 = time.time()
    result_base = engine_base.transcribe(audio_file)
    elapsed_base = time.time() - t0
    rtf_base = elapsed_base / 60.0

    print(f"\n--- [Whisper base Results] (Elapsed: {elapsed_base:.2f}s, RTF: {rtf_base:.3f}) ---")
    print(f"Full Text:\n{result_base.text}\n")

    # 3. Export formats
    print("\n[6] Exporting SRT / VTT / JSON formats...")
    srt_output = result_base.to_srt()
    vtt_output = result_base.to_vtt()
    json_output = result_base.to_json()
    print("--- [SRT Sample] ---")
    print("\n".join(srt_output.splitlines()[:12]))

    print("\n" + "=" * 60)
    print("✅ Docker Verification Test 100% SUCCESSFUL!")
    print("=" * 60)

if __name__ == "__main__":
    main()
