import os
import sys
from termux_stt import create_engine
from termux_stt.export.json_export import save_json, to_json
from termux_stt.export.rttm import save_rttm, to_rttm
from termux_stt.platform.installer import EngineInstaller


def resolve_safe_output_path(path: str) -> str:
    if not path:
        return path
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


def ensure_diarization_installed_interactive() -> bool:
    """Check if diarization models are installed; prompt user interactively if in TTY."""
    if EngineInstaller.check_diarization_installed():
        return True

    print("\n" + "=" * 65)
    print("[!] Neural Speaker Diarization runtimes / models are not installed.")
    print("    Required models: PyAnnote 3.0 (~15MB) + 3D-Speaker CAM++ (~28MB)")
    print("=" * 65)

    if sys.stdin.isatty():
        try:
            choice = input("Would you like to download and install them now? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            sys.exit(1)

        if choice in ("y", "yes"):
            print("\n[*] Starting full diarization runtime provisioning...")
            ok = EngineInstaller.install_diarization()
            if ok:
                print("[+] Diarization runtimes successfully installed! Resuming operation...\n")
                return True
            else:
                print("[-] Failed to provision diarization runtimes.")
                sys.exit(1)

    print("\n[-] Error: Diarization models are missing.")
    print("    To install them manually, run:")
    print("        termux-stt install --engine diarization")
    print("    or full install:")
    print("        termux-stt install --all\n")
    sys.exit(1)


def run_diarize(args):
    # Interactive check for diarization models
    ensure_diarization_installed_interactive()

    target_engine = getattr(args, "engine", None)
    if not target_engine or target_engine in ("whisper", "vosk"):
        target_engine = "sherpa"

    engine = create_engine(
        engine=target_engine,
        model=getattr(args, "model", None) or ("sensevoice-small-int8" if target_engine == "sherpa" else "tiny"),
        lang=getattr(args, "lang", "ko"),
        threads=getattr(args, "threads", None),
        vad=getattr(args, "vad", True),
        num_speakers=getattr(args, "speakers", 2),
        device=getattr(args, "device", "auto"),
    )

    print(f"[*] Diarizing '{args.file}' using engine='{target_engine}' with {args.speakers} speakers...")
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
