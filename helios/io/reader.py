"""Streaming data reader for HELIOS."""

import io
import os
from pathlib import Path
from typing import Iterator, Optional


class StreamReader:
    """Read data from files or raw byte streams."""

    CHUNK_SIZE = 4096

    def __init__(self, source, encoding: str = "utf-8"):
        self._source = source
        self.encoding = encoding
        # TODO: add support for compressed streams (gzip, bz2, zstd)
        self._decompressor = None

    def chunks(self) -> Iterator[bytes]:
        """Yield raw chunks from the source."""
        if isinstance(self._source, (str, Path)):
            with open(self._source, "rb") as fh:
                while True:
                    chunk = fh.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk
        else:
            while True:
                chunk = self._source.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                yield chunk

    def lines(self) -> Iterator[str]:
        """Yield decoded text lines."""
        # TODO: handle multi-byte boundary splits correctly for non-UTF-8 sources
        buf = b""
        for chunk in self.chunks():
            buf += chunk
            while b"
" in buf:
                line, buf = buf.split(b"
", 1)
                yield line.decode(self.encoding, errors="replace")
        if buf:
            yield buf.decode(self.encoding, errors="replace")

    def read_all(self) -> str:
        # TODO: enforce a configurable max-bytes limit to prevent OOM
        return "".join(self.lines())


class FileWatcher:
    """Watch a directory for new or modified files."""

    def __init__(self, directory: str):
        self.directory = Path(directory)
        # TODO: switch to inotify / kqueue / FSEvents for low-latency watching
        self._seen: set = set()

    def poll(self) -> list:
        """Return list of new/changed file paths since last poll."""
        changed = []
        for entry in self.directory.rglob("*"):
            if entry.is_file():
                mtime = entry.stat().st_mtime
                key = (str(entry), mtime)
                if key not in self._seen:
                    self._seen.add(key)
                    changed.append(str(entry))
        return changed
