from __future__ import annotations

import threading
from collections import deque
from typing import Optional

import numpy as np
from PySide6 import QtGui


class AudioRingBuffer:
    """
    Thread-safe audio buffer as deque of numpy arrays.

    push(frames): frames (n, ch) float32
    pop(n): returns exactly (n, ch) float32, zero-padded on underrun
    pop_into(out): fills provided buffer, zero-padded on underrun
    """

    def __init__(self, channels: int, max_seconds: float, sample_rate: int):
        self.channels = channels
        self.sample_rate = sample_rate
        self.max_frames = int(max_seconds * sample_rate)
        self._dq: deque[np.ndarray] = deque()
        self._frames = 0
        self._underruns = 0
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)

    def clear(self) -> None:
        with self._not_full:
            self._dq.clear()
            self._frames = 0
            self._not_full.notify_all()

    def frames_available(self) -> int:
        with self._lock:
            return self._frames

    def push(self, frames: np.ndarray) -> None:
        self.push_blocking(frames, stop_event=None)

    def push_blocking(self, frames: np.ndarray, stop_event: Optional[threading.Event]) -> None:
        if frames.size == 0:
            return
        if frames.dtype != np.float32:
            frames = frames.astype(np.float32, copy=False)
        if frames.ndim != 2 or frames.shape[1] != self.channels:
            raise ValueError(f"frames must be (n,{self.channels}) float32, got {frames.shape} {frames.dtype}")

        if frames.shape[0] > self.max_frames:
            frames = frames[:self.max_frames, :]

        offset = 0
        total = frames.shape[0]
        with self._not_full:
            while offset < total:
                if stop_event is not None and stop_event.is_set():
                    return
                space = self.max_frames - self._frames
                if space <= 0:
                    self._not_full.wait(timeout=0.05)
                    continue
                take = min(space, total - offset)
                self._dq.append(frames[offset : offset + take])
                self._frames += take
                offset += take

    def pop(self, n: int) -> np.ndarray:
        if n <= 0:
            return np.zeros((0, self.channels), dtype=np.float32)

        out = np.zeros((n, self.channels), dtype=np.float32)
        self.pop_into(out)
        return out

    def pop_into(self, out: np.ndarray) -> int:
        if out.ndim != 2 or out.shape[1] != self.channels:
            raise ValueError(f"out must be (n,{self.channels}) float32, got {out.shape} {out.dtype}")
        if out.dtype != np.float32:
            raise ValueError(f"out must be float32, got {out.dtype}")

        n = out.shape[0]
        if n <= 0:
            return 0

        idx = 0
        with self._not_full:
            while idx < n and self._dq:
                chunk = self._dq[0]
                take = min(n - idx, chunk.shape[0])
                out[idx : idx + take] = chunk[:take]
                idx += take
                if take == chunk.shape[0]:
                    self._dq.popleft()
                else:
                    self._dq[0] = chunk[take:, :]
                self._frames -= take
                self._not_full.notify_all()
            if idx < n:
                self._underruns += 1

        if idx < n:
            out[idx:n, :].fill(0)
        return idx

    def consume_underruns(self) -> int:
        with self._lock:
            underruns = self._underruns
            self._underruns = 0
            return underruns


class VisualizerBuffer:
    """
    Thread-safe ring buffer for recent audio snapshots.

    push(frames): frames (n, ch) float32
    get_recent(n, mono): returns most recent frames, optional mono downmix
    """

    def __init__(self, channels: int, max_seconds: float, sample_rate: int):
        self.channels = channels
        self.sample_rate = sample_rate
        self.max_frames = max(1, int(max_seconds * sample_rate))
        self._buffer = np.zeros((self.max_frames, channels), dtype=np.float32)
        self._write_index = 0
        self._filled = 0
        self._lock = threading.Lock()

    def clear(self) -> None:
        with self._lock:
            self._write_index = 0
            self._filled = 0

    def push(self, frames: np.ndarray) -> None:
        if frames.size == 0:
            return
        if frames.dtype != np.float32:
            frames = frames.astype(np.float32, copy=False)
        if frames.ndim != 2 or frames.shape[1] != self.channels:
            raise ValueError(f"frames must be (n,{self.channels}) float32, got {frames.shape} {frames.dtype}")

        if frames.shape[0] > self.max_frames:
            frames = frames[-self.max_frames :, :]

        n = frames.shape[0]
        with self._lock:
            end = self._write_index + n
            if end <= self.max_frames:
                self._buffer[self._write_index : end, :] = frames
            else:
                first = self.max_frames - self._write_index
                self._buffer[self._write_index :, :] = frames[:first, :]
                remaining = end - self.max_frames
                self._buffer[:remaining, :] = frames[first:, :]
            self._write_index = end % self.max_frames
            self._filled = min(self.max_frames, self._filled + n)

    def get_recent(
        self,
        frames: Optional[int] = None,
        mono: bool = False,
        delay_frames: int = 0,
    ) -> np.ndarray:
        delay = max(0, int(delay_frames))
        with self._lock:
            filled = self._filled
            if filled == 0 or delay >= filled:
                data = np.zeros((0, self.channels), dtype=np.float32)
            else:
                available = filled - delay
                if frames is not None and frames > 0:
                    take = min(frames, available)
                else:
                    take = available

                if take <= 0:
                    data = np.zeros((0, self.channels), dtype=np.float32)
                elif filled < self.max_frames:
                    end = filled - delay
                    start = end - take
                    data = np.empty((take, self.channels), dtype=np.float32)
                    data[:, :] = self._buffer[start:end, :]
                else:
                    end = (self._write_index - delay) % self.max_frames
                    start = (end - take) % self.max_frames
                    data = np.empty((take, self.channels), dtype=np.float32)
                    if start < end:
                        data[:, :] = self._buffer[start:end, :]
                    else:
                        first = self.max_frames - start
                        data[:first, :] = self._buffer[start:, :]
                        data[first:, :] = self._buffer[:end, :]

        if mono and data.size:
            mono_data = data.mean(axis=1, dtype=np.float32)
            return mono_data.reshape(-1, 1)
        return data


class VideoFrameBuffer:
    """
    Thread-safe buffer for the most recent video frame.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._image: Optional[QtGui.QImage] = None
        self._timestamp: Optional[float] = None

    def clear(self) -> None:
        with self._lock:
            self._image = None
            self._timestamp = None

    def update(self, image: QtGui.QImage, timestamp: float) -> None:
        with self._lock:
            self._image = image
            self._timestamp = float(timestamp)

    def get_latest(self) -> tuple[Optional[QtGui.QImage], Optional[float]]:
        with self._lock:
            return self._image, self._timestamp


class VideoRingBuffer:
    """
    Thread-safe ring buffer for decoded video frames with timestamps.
    Frames are stored in timestamp order. Supports fetching the frame
    closest to (but not after) a given target timestamp.
    """

    def __init__(self, max_frames: int = 30):
        self._max_frames = max(1, int(max_frames))
        self._frames: deque[tuple[float, QtGui.QImage]] = deque()
        self._lock = threading.Lock()

    def clear(self) -> None:
        with self._lock:
            self._frames.clear()

    def push(self, timestamp: float, image: QtGui.QImage) -> None:
        """Add a frame. Frames should be pushed in timestamp order."""
        with self._lock:
            self._frames.append((float(timestamp), image))
            while len(self._frames) > self._max_frames:
                self._frames.popleft()

    def get_frame_for_time(self, target_time: float) -> tuple[Optional[QtGui.QImage], Optional[float]]:
        """
        Return the frame with the largest timestamp <= target_time.
        Also discards frames that are too old (before the returned frame).
        """
        with self._lock:
            if not self._frames:
                return None, None

            best_idx = -1
            for i, (ts, _) in enumerate(self._frames):
                if ts <= target_time:
                    best_idx = i
                else:
                    break  # frames are in order, stop searching

            if best_idx < 0:
                # All frames are in the future; return None
                return None, None

            # Discard frames older than best_idx (already shown)
            for _ in range(best_idx):
                self._frames.popleft()

            ts, img = self._frames[0]
            return img, ts

    def frames_buffered(self) -> int:
        with self._lock:
            return len(self._frames)
