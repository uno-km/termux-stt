import pytest

from termux_stt.diarization.clustering import KMeans, cosine_similarity, euclidean_distance
from termux_stt.diarization.mapper import SpeakerMapper
from termux_stt.export.result import Segment


def test_distance_and_similarity():
    vec_a = [1.0, 0.0, 0.0]
    vec_b = [0.0, 1.0, 0.0]
    vec_c = [2.0, 0.0, 0.0]

    # Orthogonal
    assert abs(cosine_similarity(vec_a, vec_b) - 0.0) < 1e-6
    # Parallel
    assert abs(cosine_similarity(vec_a, vec_c) - 1.0) < 1e-6

    # Euclidean
    assert abs(euclidean_distance([0.0, 0.0], [3.0, 4.0]) - 5.0) < 1e-6

    # Dimension mismatch
    with pytest.raises(ValueError):
        euclidean_distance([1.0], [1.0, 2.0])


def test_kmeans_2clusters_separation():
    # Cluster A around (1, 1), Cluster B around (10, 10)
    data = [
        [0.9, 1.1], [1.0, 1.0], [1.2, 0.8],
        [9.9, 10.1], [10.0, 10.0], [10.2, 9.8]
    ]
    kmeans = KMeans(n_clusters=2, seed=42)
    kmeans.fit(data)

    labels = kmeans.labels_
    # First 3 should share one label, last 3 should share another
    assert labels[0] == labels[1] == labels[2]
    assert labels[3] == labels[4] == labels[5]
    assert labels[0] != labels[3]


def test_kmeans_adaptive_sample_count():
    # Only 1 sample with 2 requested clusters -> must not crash, should adapt
    data = [[1.0, 2.0]]
    kmeans = KMeans(n_clusters=2, seed=42)
    kmeans.fit(data)
    assert len(kmeans.labels_) == 1
    assert kmeans.labels_[0] == 0


def test_speaker_mapper_overlap_alignment():
    segments = [
        Segment(start=0.0, end=2.0, text="Hello"),
        Segment(start=2.5, end=4.5, text="World"),
    ]
    # Speaker 0 active [0.0 - 2.2], Speaker 1 active [2.2 - 5.0]
    speaker_labels = [
        (0.0, 2.2, 0),
        (2.2, 5.0, 1),
    ]

    mapper = SpeakerMapper()
    aligned = mapper.align(segments, speaker_labels)

    assert len(aligned) == 2
    assert aligned[0].speaker == "Speaker_0"
    assert aligned[0].text == "Hello"
    assert aligned[1].speaker == "Speaker_1"
    assert aligned[1].text == "World"


def test_speaker_mapper_empty_labels_fallback_unknown():
    # No speaker_labels provided -> all segments honestly marked as Speaker_Unknown
    segments = [
        Segment(start=0.0, end=1.0, text="Speaker one speaking"),
        Segment(start=1.2, end=2.0, text="Still speaker one"),
        Segment(start=3.5, end=4.5, text="Speaker two speaking after long pause"),
    ]
    mapper = SpeakerMapper()
    aligned = mapper.align(segments, [], num_speakers=2)

    assert aligned[0].speaker == "Speaker_Unknown"
    assert aligned[1].speaker == "Speaker_Unknown"
    assert aligned[2].speaker == "Speaker_Unknown"
