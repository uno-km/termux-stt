import sys
from termux_stt import create_engine
from termux_stt.export.json_export import save_json, to_json
from termux_stt.export.srt import save_srt, to_srt
from termux_stt.export.vtt import save_vtt, to_vtt

def resolve_safe_output_path(path: str) -> str:
    if not path:
        return path
    import os
    from pathlib import Path
    p = Path(path)
    if str(p).startswith("/tmp") and not os.access("/tmp", os.W_OK):
        fallback_dir = os.environ.get("TMPDIR") or os.path.expanduser("~/tmp") or "."
        os.makedirs(fallback_dir, exist_ok=True)
        safe_path = os.path.join(fallback_dir, p.name)
        print(f"[*] Notice: Root '/tmp' is read-only on Android. Safe redirected output to: '{safe_path}'")
        return safe_path
    out_dir = os.path.dirname(os.path.abspath(path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    return path


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
        out_path = resolve_safe_output_path(args.output)
        if args.format == "srt":
            save_srt(result, out_path)
        elif args.format == "vtt":
            save_vtt(result, out_path)
        elif args.format == "json":
            save_json(result, out_path)
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(result.text)
        print(f"Output saved to {out_path}")
    else:
        if args.format == "srt":
            print(to_srt(result))
        elif args.format == "vtt":
            print(to_vtt(result))
        elif args.format == "json":
            print(to_json(result))
        else:
            print(result.text)
