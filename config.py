from __future__ import annotations

from models import BufferPreset

EQ_PROFILE = False
EQ_PROFILE_LOG_EVERY = 50
EQ_PROFILE_LOW_WATERMARK_SEC = 0.25

BLOCKSIZE_FRAMES = 512
LATENCY = "low"
DEFAULT_BUFFER_PRESET = "Stable"
AUTO_BUFFER_PRESET = "Ultra Stable"
AUTO_BUFFER_WINDOW_SEC = 6.0
AUTO_BUFFER_THRESHOLD = 3

BUFFER_PRESETS = {
    "Stable": BufferPreset(
        blocksize_frames=BLOCKSIZE_FRAMES,
        latency=LATENCY,
        target_sec=0.7,
        high_sec=0.9,
        low_sec=0.5,
        ring_max_seconds=1.25,
    ),
    "Low Latency": BufferPreset(
        blocksize_frames=256,
        latency=LATENCY,
        target_sec=0.5,
        high_sec=0.7,
        low_sec=0.35,
        ring_max_seconds=0.9,
    ),
    "Ultra Stable": BufferPreset(
        blocksize_frames=2048,
        latency="high",
        target_sec=1.5,
        high_sec=2.0,
        low_sec=1.1,
        ring_max_seconds=2.5,
    ),
}
