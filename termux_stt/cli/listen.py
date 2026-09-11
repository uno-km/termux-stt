import time

from termux_stt import create_engine


def run_listen(args):
    engine_name = getattr(args, "engine", "whisper")
    engine = create_engine(
        engine=engine_name,
        model=getattr(args, "model", None),
        lang=getattr(args, "lang", "ko"),
        threads=getattr(args, "threads", None),
        vad=getattr(args, "vad", True),
    )

    if engine_name != "whisper":
        print("Warning: Real-time listening is currently best supported with whisper engine.")

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
