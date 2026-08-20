import time

from termux_stt.engine.base import EngineConfig
from termux_stt.engine.whisper_engine import WhisperEngine


def run_listen(args):
    config = EngineConfig(
        model_path=args.model or "default",
        language=args.lang,
        num_threads=args.threads,
        use_vad=args.vad
    )

    if args.engine != "whisper":
        print("Warning: Real-time listening is currently best supported with whisper engine.")

    engine = WhisperEngine(config)

    print(f"Listening with {args.engine}... (Press Ctrl+C to stop)")
    start_time = time.time()

    try:
        for segment in engine.stream_mic():
            print(f"[{segment.start:.2f} - {segment.end:.2f}] {segment.text}")
            if args.duration > 0 and (time.time() - start_time) >= args.duration:
                print(f"Reached duration limit of {args.duration} seconds.")
                break
    except KeyboardInterrupt:
        print("\nStopped listening.")
