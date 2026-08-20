from termux_stt.export.result import TranscriptResult

def _format_timestamp(seconds: float) -> str:
    """Format seconds into HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def to_srt(result: TranscriptResult) -> str:
    """Generate SRT format from TranscriptResult."""
    lines = []
    for i, seg in enumerate(result.segments, 1):
        start = _format_timestamp(seg.start)
        end = _format_timestamp(seg.end)
        lines.append(str(i))
        lines.append(f"{start} --> {end}")
        text = seg.text.strip()
        if hasattr(seg, 'speaker') and seg.speaker:
            text = f"[{seg.speaker}] {text}"
        lines.append(text)
        lines.append("")
    return "\n".join(lines)

def save_srt(result: TranscriptResult, output_path: str) -> None:
    """Save TranscriptResult as SRT file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(to_srt(result))
