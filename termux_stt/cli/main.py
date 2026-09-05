import argparse
import sys

from termux_stt.cli.benchmark import run_benchmark
from termux_stt.cli.demo import run_demo
from termux_stt.cli.diarize import run_diarize
from termux_stt.cli.doctor import run_doctor
from termux_stt.cli.listen import run_listen
from termux_stt.cli.models_cmd import run_models
from termux_stt.cli.transcribe import run_transcribe
from termux_stt.platform.installer import main as run_install


def _run_cli():
    parser = argparse.ArgumentParser(description="Termux STT - On-device Speech-to-Text Framework")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common parent parser for shared arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--engine", type=str, default="whisper", choices=["whisper", "vosk", "hybrid", "sherpa"], help="Engine to use")
    common_parser.add_argument("-m", "--model", type=str, help="Model name or path")
    common_parser.add_argument("--device", type=str, default="auto", choices=["auto", "gpu", "cpu", "vulkan"], help="Acceleration device backend")
    common_parser.add_argument("--lang", type=str, default="ko", help="Language code")
    common_parser.add_argument("--threads", type=int, default=None, help="Number of CPU threads to use")
    common_parser.add_argument("--vad", action="store_true", help="Enable VAD filtering")
    common_parser.add_argument("--quantization", type=str, choices=["none", "q4_0", "q5_1", "q8_0", "f16"], default="q5_1", help="Model quantization level")
    common_parser.add_argument("--prompt", type=str, default=None, help="Initial prompt / context for decoding")
    common_parser.add_argument("--temperature", type=float, default=None, help="Sampling temperature")
    common_parser.add_argument("--beam-size", type=int, default=None, help="Beam search beam size")
    common_parser.add_argument("--translate", action="store_true", help="Translate source audio to English")
    common_parser.add_argument("--extra-args", type=str, default=None, help="Raw CLI arguments passed directly to the engine")
    common_parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    # Install subcommand
    subparsers.add_parser("install", help="1-Click automatic installer for native engines and dependencies")

    # Demo subcommand
    parser_demo = subparsers.add_parser("demo", parents=[common_parser], help="Run zero-configuration STT demo with standard benchmark audio")
    parser_demo.add_argument("--format", type=str, choices=["text", "json", "srt", "vtt"], default="text", help="Output format")
    parser_demo.add_argument("--output", type=str, help="Output file path")

    # Transcribe subcommand
    parser_transcribe = subparsers.add_parser("transcribe", parents=[common_parser], help="Transcribe audio file")
    parser_transcribe.add_argument("file", type=str, nargs="?", default=None, help="Path to audio file (optional if --demo is specified)")
    parser_transcribe.add_argument("--demo", action="store_true", help="Use standard JFK benchmark audio for demonstration")
    parser_transcribe.add_argument("--format", type=str, choices=["text", "json", "srt", "vtt"], default="text", help="Output format")
    parser_transcribe.add_argument("--output", type=str, help="Output file path")

    # Listen subcommand
    parser_listen = subparsers.add_parser("listen", parents=[common_parser], help="Real-time mic transcription")
    parser_listen.add_argument("--duration", type=int, default=0, help="Listen duration in seconds (0 for infinite)")

    # Diarize subcommand
    parser_diarize = subparsers.add_parser("diarize", parents=[common_parser], help="Diarize and transcribe audio file")
    parser_diarize.add_argument("file", type=str, help="Path to audio file")
    parser_diarize.add_argument("--speakers", type=int, default=2, help="Number of expected speakers")
    parser_diarize.add_argument("--format", type=str, choices=["text", "json", "rttm"], default="text", help="Output format")
    parser_diarize.add_argument("--output", type=str, help="Output file path")

    # Models subcommand
    parser_models = subparsers.add_parser("models", help="Manage STT models")
    parser_models.add_argument("action", choices=["list", "download", "remove"], help="Action to perform")
    parser_models.add_argument("extra_args", nargs="*", help="Optional positional [engine] [model]")
    parser_models.add_argument("--model", type=str, help="Model name")
    parser_models.add_argument("--engine", type=str, default="whisper", help="Target engine")

    # Doctor subcommand
    subparsers.add_parser("doctor", help="Check system environment and dependencies")

    # Benchmark subcommand
    parser_benchmark = subparsers.add_parser("benchmark", parents=[common_parser], help="Run performance benchmarks")
    parser_benchmark.add_argument("--audio", type=str, required=True, help="Test audio file path")

    # ── AMEVA Component Protocol v1 ─────────────────────────────────────────
    _protocol_available = False
    try:
        from ameva_component.cli_support import build_protocol_subcommands
        build_protocol_subcommands(subparsers)
        _protocol_available = True
    except ImportError as _imp_err:
        import logging
        logging.getLogger(__name__).debug("ameva_component CLI support not installed: %s", _imp_err)
    # ────────────────────────────────────────────────────────────────────────

    args = parser.parse_args()
    args._explicit_lang = any(arg.startswith("--lang") for arg in sys.argv)

    if args.command == "install":
        run_install()
    elif args.command == "demo":
        run_demo(args)
    elif args.command == "transcribe":
        if getattr(args, "demo", False):
            from termux_stt.cli.demo import ensure_demo_audio
            args.file = ensure_demo_audio()
            if getattr(args, "lang", None) == "ko" and not args._explicit_lang:
                args.lang = "en"
        elif not args.file:
            parser_transcribe.error("the following arguments are required: file (or use --demo)")
        run_transcribe(args)
    elif args.command == "listen":
        run_listen(args)
    elif args.command == "diarize":
        run_diarize(args)
    elif args.command == "models":
        run_models(args)
    elif args.command == "doctor":
        run_doctor(args)
    elif args.command == "benchmark":
        run_benchmark(args)
    elif args.command in ("component", "model", "instance") and _protocol_available:
        from ameva_component.cli_support import dispatch_protocol
        from termux_stt.control import STTControl
        dispatch_protocol(args, STTControl())
    elif args.command in ("component", "model", "instance"):
        print("[ERROR] ameva-component-sdk not installed.", file=sys.stderr)
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


def main():
    try:
        _run_cli()
    except FileNotFoundError as e:
        filename = getattr(e, "filename", None) or str(e)
        print(f"\n[-] Error: Input audio file not found -> '{filename}'")
        print("    Please check the file path and ensure the audio file exists.")
        sys.exit(1)
    except PermissionError as e:
        filename = getattr(e, "filename", None) or str(e)
        print(f"\n[-] Error: Permission denied -> '{filename}'")
        print("    (Tip: On Android Termux, root '/tmp' is read-only. Please use a local path like './output.srt')")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[-] Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Operation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        else:
            print(f"\n[-] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

