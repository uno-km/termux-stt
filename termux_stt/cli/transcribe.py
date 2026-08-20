import sys

from termux_stt.engine.base import EngineConfig
from termux_stt.engine.hybrid_engine import HybridEngine
from termux_stt.engine.vosk_engine import VoskEngine
from termux_stt.engine.whisper_engine import WhisperEngine
from termux_stt.export.json_export import save_json, to_json
from termux_stt.export.srt import save_srt, to_srt
from termux_stt.export.vtt import save_vtt, to_vtt


def run_transcribe(args):
    config = EngineConfig(
        model_path=args.model or "default",
        language=args.lang,
        num_threads=args.threads,
        use_vad=args.vad
    )

    if args.engine == "whisper":
        engine = WhisperEngine(config)
    elif args.engine == "vosk":
        engine = VoskEngine(config)
    elif args.engine == "hybrid":
        engine = HybridEngine(config)
    else:
        print(f"Engine {args.engine} not supported for transcription yet.")
        sys.exit(1)

    print(f"Transcribing {args.file} using {args.engine}...")
    result = engine.transcribe(args.file)

    if args.output:
        if args.format == "srt":
            save_srt(result, args.output)
        elif args.format == "vtt":
            save_vtt(result, args.output)
        elif args.format == "json":
            save_json(result, args.output)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result.text)
        print(f"Output saved to {args.output}")
    else:
        if args.format == "srt":
            print(to_srt(result))
        elif args.format == "vtt":
            print(to_vtt(result))
        elif args.format == "json":
            print(to_json(result))
        else:
            print(result.text)
