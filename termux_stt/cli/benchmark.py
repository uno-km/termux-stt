import os
import time

from termux_stt import create_engine
from termux_stt.audio.loader import get_audio_info


def run_benchmark(args):
    try:
        import psutil
    except ImportError:
        psutil = None
    if not os.path.exists(args.audio):
        print(f"Error: Audio file {args.audio} not found.")
        return

    engine_name = getattr(args, "engine", "whisper")
    print(f"Starting benchmark on {args.audio} with {engine_name} engine...")

    # Extract actual audio duration via multi-stage inspection (Zero Fake Duration)
    audio_duration = None
    try:
        info = get_audio_info(args.audio)
        dur_str = info.get("format", {}).get("duration")
        if dur_str is not None:
            audio_duration = float(dur_str)
    except Exception:
        pass

    # Secondary fallback: standard wave header inspection
    if audio_duration is None:
        try:
            import wave
            with wave.open(args.audio, "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                if rate > 0:
                    audio_duration = float(frames) / float(rate)
        except Exception:
            pass

    engine = create_engine(
        engine=engine_name,
        model=getattr(args, "model", None) or "tiny",
        lang=getattr(args, "lang", "ko"),
        threads=getattr(args, "threads", None),
        vad=getattr(args, "vad", True),
    )

    max_rss_mb = 0.0
    stop_monitor = False

    def _monitor_memory():
        nonlocal max_rss_mb
        if not psutil:
            return
        main_proc = psutil.Process(os.getpid())
        while not stop_monitor:
            try:
                current_rss = main_proc.memory_info().rss
                for child in main_proc.children(recursive=True):
                    try:
                        current_rss += child.memory_info().rss
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                rss_mb = current_rss / (1024 * 1024)
                if rss_mb > max_rss_mb:
                    max_rss_mb = rss_mb
            except Exception:
                pass
            time.sleep(0.05)

    import threading
    monitor_thread = threading.Thread(target=_monitor_memory, daemon=True)
    monitor_thread.start()

    start_time = time.time()
    result = engine.transcribe(args.audio)
    end_time = time.time()

    stop_monitor = True
    monitor_thread.join(timeout=0.2)

    execution_time = end_time - start_time
    rtf = (execution_time / audio_duration) if (audio_duration and audio_duration > 0) else None

    print("\n--- Benchmark Results ---")
    if audio_duration is not None:
        print(f"Audio Duration: {audio_duration:.2f}s")
    else:
        print("Audio Duration: Unknown (Failed to inspect exact duration)")
    print(f"Execution Time: {execution_time:.2f}s")
    if rtf is not None:
        print(f"Real Time Factor (RTF): {rtf:.2f}x (Lower is better)")
    else:
        print("Real Time Factor (RTF): N/A (Audio duration undetermined)")
    print(f"Peak Total Memory usage: {max_rss_mb:.2f} MB")
    print(f"Transcribed Text Length: {len(result.text)} chars ({len(result.segments)} segments)")
