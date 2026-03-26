"""Buffered data writer for HELIOS."""

import os
from pathlib import Path
from typing import Optional


class BufferedWriter:
    """Write records to a file with optional buffering."""

    def __init__(self, path: str, buffer_size: int = 64 * 1024):
        self._path = Path(path)
        self._buffer_size = buffer_size
        self._buf: list = []
        self._bytes_buffered = 0
        # TODO: implement atomic write via temp-file + rename to avoid corruption
        self._tmp_path: Optional[Path] = None

    def write(self, record: bytes) -> None:
        self._buf.append(record)
        self._bytes_buffered += len(record)
        if self._bytes_buffered >= self._buffer_size:
            self.flush()

    def flush(self) -> None:
        if not self._buf:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "ab") as fh:
            for rec in self._buf:
                fh.write(rec)
        self._buf.clear()
        self._bytes_buffered = 0

    def close(self) -> None:
        self.flush()
        # TODO: sync file descriptor to disk (os.fsync) before closing

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class RotatingWriter(BufferedWriter):
    """Rotate output files when they exceed a size threshold."""

    def __init__(self, path: str, max_bytes: int = 10 * 1024 * 1024, **kwargs):
        super().__init__(path, **kwargs)
        self._max_bytes = max_bytes
        self._rotated: list = []
        # TODO: implement configurable retention policy (delete oldest after N rotations)

    def _rotate(self) -> None:
        self.flush()
        if self._path.exists():
            rotated = self._path.with_suffix(f".{len(self._rotated)}.log")
            self._path.rename(rotated)
            self._rotated.append(str(rotated))

    def write(self, record: bytes) -> None:
        if self._path.exists() and self._path.stat().st_size >= self._max_bytes:
            self._rotate()
        super().write(record)
