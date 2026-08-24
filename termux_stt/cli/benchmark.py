import os
import time

from termux_stt.engine.base import EngineConfig
from termux_stt.engine.whisper_engine import WhisperEngine


def run_benchmark(args):
    try:
        import psutil
    except ImportError:
        psutil = None
    if not os.path.exists(args.audio):
        print(f"Error: Audio file {args.audio} not found.")
        return

    print(f"Starting benchmark on {args.audio} with {args.engine} engine...")

    # Placeholder for actual audio duration extraction
    audio_duration = 10.0

    config = EngineConfig(
        model_path=args.model or "default",
        language=args.lang,
        num_threads=args.threads
    )

    engine = WhisperEngine(config)

    if psutil:
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / (1024 * 1024)
    else:
        mem_before = 0.0

    start_time = time.time()
    result = engine.transcribe(args.audio)
    end_time = time.time()

    if psutil:
        mem_after = process.memory_info().rss / (1024 * 1024)
        mem_peak = mem_after - mem_before
    else:
        mem_peak = 0.0

    execution_time = end_time - start_time
    rtf = execution_time / audio_duration if audio_duration > 0 else 0

    print("\n--- Benchmark Results ---")
    print(f"Audio Duration: {audio_duration:.2f}s")
    print(f"Execution Time: {execution_time:.2f}s")
    print(f"Real Time Factor (RTF): {rtf:.2f}x (Lower is better)")
    print(f"Peak Memory usage: {mem_peak:.2f} MB")
    print(f"Transcribed Text Length: {len(result.text)} chars ({len(result.segments)} segments)")
