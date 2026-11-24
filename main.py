#!/usr/bin/env python3
"""One Line, One Chill — make.fun entry.

Writes a single line of horror (one sentence, under 200 characters)
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output), then re-reads the
file to verify the bytes written are exactly the line.
"""

import os
import sys
import tempfile

LINE = "My daughter's drawing of our family has four people in it, and she keeps pointing at the one standing behind me."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    # Atomic write: a crash mid-write can never leave a truncated entry.txt.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp_path, path)
    except OSError:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("verification failed: entry.txt bytes differ", file=sys.stderr)
        return 1
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
