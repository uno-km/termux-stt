from termux_stt import create_engine
from termux_stt.export.json_export import save_json, to_json
from termux_stt.export.rttm import save_rttm, to_rttm


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
        if args.format == "rttm":
            save_rttm(result, args.output)
        elif args.format == "json":
            save_json(result, args.output)
        else:
            with open(args.output, "w", encoding="utf-8") as f:
                for seg in result.segments:
                    f.write(f"[{seg.speaker}] {seg.text}\n")
        print(f"Output saved to {args.output}")
    else:
        if args.format == "rttm":
            print(to_rttm(result))
        elif args.format == "json":
            print(to_json(result))
        else:
            for seg in result.segments:
                print(f"[{seg.speaker}] {seg.text}")
