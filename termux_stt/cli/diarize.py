import sys
from termux_stt.engine.base import EngineConfig
from termux_stt.engine.hybrid_engine import HybridEngine
from termux_stt.export.rttm import save_rttm, to_rttm
from termux_stt.export.json_export import save_json, to_json

def run_diarize(args):
    config = EngineConfig(
        model_path=args.model or "default",
        language=args.lang,
        num_threads=args.threads,
        use_vad=args.vad
    )
    
    engine = HybridEngine(config)
        
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
