from typing import List, Tuple

from termux_stt.export.result import Segment


class SpeakerMapper:
    """Maps speaker clusters to STT text segments."""

    def __init__(self):
        pass

    def align(self, segments: List[Segment], speaker_labels: List[Tuple[float, float, int]]) -> List[Segment]:
        """
        Align Whisper text segments with X-Vector cluster time windows.
        Assigns the speaker label that overlaps the most with the segment.
        """
        aligned_segments = []
        for seg in segments:
            best_speaker = -1
            max_overlap = 0.0

            for spk_start, spk_end, cluster_id in speaker_labels:
                overlap = self._time_overlap(seg.start, seg.end, spk_start, spk_end)
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_speaker = cluster_id

            if best_speaker != -1:
                speaker_name = self.format_speaker_label(best_speaker)
            else:
                speaker_name = "Unknown"

            aligned_segments.append(Segment(
                text=seg.text,
                start=seg.start,
                end=seg.end,
                speaker=speaker_name
            ))

        return aligned_segments

    def _time_overlap(self, seg_start: float, seg_end: float, spk_start: float, spk_end: float) -> float:
        """Calculate overlap duration between two time intervals."""
        overlap_start = max(seg_start, spk_start)
        overlap_end = min(seg_end, spk_end)
        return max(0.0, overlap_end - overlap_start)

    def format_speaker_label(self, cluster_id: int) -> str:
        """Format cluster ID into speaker label string."""
        return f"Speaker_{cluster_id}"
