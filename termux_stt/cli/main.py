import argparse
import sys

from termux_stt.cli.benchmark import run_benchmark
from termux_stt.cli.diarize import run_diarize
from termux_stt.cli.doctor import run_doctor
from termux_stt.cli.listen import run_listen
from termux_stt.cli.models_cmd import run_models
from termux_stt.cli.transcribe import run_transcribe


def main():
    parser = argparse.ArgumentParser(description="Termux STT - On-device Speech-to-Text Framework")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Common parent parser for shared arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--engine", type=str, default="whisper", choices=["whisper", "vosk", "hybrid", "sherpa"], help="Engine to use")
    common_parser.add_argument("--model", type=str, help="Model name or path")
    common_parser.add_argument("--lang", type=str, help="Language code")
    common_parser.add_argument("--threads", type=int, default=4, help="Number of CPU threads to use")
    common_parser.add_argument("--vad", action="store_true", help="Enable VAD filtering")
    common_parser.add_argument("--quantization", type=str, choices=["none", "q4_0", "q8_0"], default="none", help="Model quantization level")
    common_parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    # Transcribe subcommand
    parser_transcribe = subparsers.add_parser("transcribe", parents=[common_parser], help="Transcribe audio file")
    parser_transcribe.add_argument("file", type=str, help="Path to audio file")
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
    parser_models.add_argument("--model", type=str, help="Model name")
    parser_models.add_argument("--engine", type=str, default="whisper", help="Target engine")

    # Doctor subcommand
    subparsers.add_parser("doctor", help="Check system environment and dependencies")

    # Benchmark subcommand
    parser_benchmark = subparsers.add_parser("benchmark", parents=[common_parser], help="Run performance benchmarks")
    parser_benchmark.add_argument("--audio", type=str, required=True, help="Test audio file path")

    args = parser.parse_args()

    if args.command == "transcribe":
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
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
