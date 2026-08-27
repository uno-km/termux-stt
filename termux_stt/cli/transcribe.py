import sys
from termux_stt import create_engine
from termux_stt.export.json_export import save_json, to_json
from termux_stt.export.srt import save_srt, to_srt
from termux_stt.export.vtt import save_vtt, to_vtt

def run_transcribe(args):
    # Collect all extra kwargs
    extra_kwargs = {}
    if getattr(args, "prompt", None):
        extra_kwargs["prompt"] = args.prompt
    if getattr(args, "temperature", None) is not None:
        extra_kwargs["temperature"] = args.temperature
    if getattr(args, "beam_size", None) is not None:
        extra_kwargs["beam_size"] = args.beam_size
    if getattr(args, "translate", False):
        extra_kwargs["translate"] = True
    if getattr(args, "extra_args", None):
        extra_kwargs["extra_args"] = args.extra_args

    engine = create_engine(
        engine=args.engine,
        model=args.model,
        lang=args.lang or "ko",
        threads=args.threads,
        vad=args.vad,
        quantization=args.quantization,
        **extra_kwargs
    )

    if getattr(args, "verbose", False):
        print(f"Transcribing {args.file} using {args.engine} with config {engine.get_info()}...")

    result = engine.transcribe(args.file, **extra_kwargs)

    if args.output:
        import os
        out_dir = os.path.dirname(os.path.abspath(args.output))
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

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
