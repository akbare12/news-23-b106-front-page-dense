#!/usr/bin/env python3
"""news-23 b106 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("main.py: error:", msg, file=sys.stderr)
    sys.exit(1)


def validate_png(data):
    """Validate the PNG strictly (header + chunk walk) before copying it."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 33:
        fail("file too short for an IHDR chunk")
    # first chunk: length at bytes 8..12, type at 12..16, IHDR data at 16..29, CRC at 29..33.
    # NOTE: offsets start after the 8-byte PNG signature (data[0:8]), not at 0.
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    ihdr = data[16:29]
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (1024, 1024):
        fail("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        fail("expected 8-bit RGB/RGBA, got depth %d colour type %d" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        fail("unexpected compression/filter/interlace flags")
    expect = zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF
    (crc,) = struct.unpack(">I", data[29:33])
    if crc != expect:
        fail("IHDR CRC mismatch")
    # chunk walk from offset 33
    off = 33
    idat_total = 0
    seen_iend = False
    while off < len(data):
        if off + 8 > len(data):
            fail("truncated chunk header at offset %d" % off)
        (clen,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + clen > len(data):
            fail("truncated %s chunk" % ctype.decode("latin1"))
        body = data[off + 8:off + 8 + clen]
        (ccrc,) = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != ccrc:
            fail("%s CRC mismatch" % ctype.decode("latin1"))
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be empty")
            if off + 12 + clen != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        off += 12 + clen
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small (%d bytes)" % idat_total)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if os.path.isfile(outdir_abs):
        fail("MAKEFUN_OUTPUT_DIR is a file: %s" % outdir)
    if outdir_abs == here or outdir_abs.startswith(here + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: %s" % outdir)
    if not os.path.exists(src):
        fail("source image missing: %s" % src)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        fail("source too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        fail("source over 1 MiB: %d bytes" % len(data))
    validate_png(data)
    out = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(out) == os.path.abspath(src):
        fail("output would overwrite the source image")
    os.makedirs(outdir_abs, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    with open(out, "rb") as f:
        back = f.read()
    if back != data:
        fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)" % (out, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
