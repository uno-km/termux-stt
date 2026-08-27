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


def run_diarize(args):
    engine = create_engine(
        engine="hybrid",
        model=getattr(args, "model", None) or "tiny",
        lang=getattr(args, "lang", "ko"),
        threads=getattr(args, "threads", None),
        vad=getattr(args, "vad", True),
        num_speakers=getattr(args, "speakers", 2),
    )

    print(f"Diarizing {args.file} with {args.speakers} speakers...")
    result = engine.diarize(args.file, num_speakers=args.speakers)

    if args.output:
        out_path = resolve_safe_output_path(args.output)
        if args.format == "rttm":
            save_rttm(result, out_path)
        elif args.format == "json":
            save_json(result, out_path)
        else:
            with open(out_path, "w", encoding="utf-8") as f:
                for seg in result.segments:
                    f.write(f"[{seg.speaker}] {seg.text}\n")
        print(f"Output saved to {out_path}")
    else:
        if args.format == "rttm":
            print(to_rttm(result))
        elif args.format == "json":
            print(to_json(result))
        else:
            for seg in result.segments:
                print(f"[{seg.speaker}] {seg.text}")
