#!/usr/bin/env python3
"""THE WORLD IN ONE IMAGE - the world's news of Sunday 22 November 2026 in one PNG.

Entry for make.fun's "news-image-20261122" bounty. Pure Python 3 standard
library: the front page is drawn pixel by pixel into an RGB framebuffer with a
built-in 5x7 bitmap font and written out with a hand-rolled PNG encoder
(zlib + struct). No network, no external assets, fully deterministic: every
run writes exactly the same bytes to the output entry.png.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 234)
INK = (20, 22, 26)
RED = (178, 32, 42)
DARK = (58, 58, 58)
HAIR = (178, 171, 152)

# ---------------------------------------------------------------------------
# 5x7 bitmap font. Each glyph is 7 rows of 5 pixels, '#' = ink.
# ---------------------------------------------------------------------------
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "a": (".....", ".....", ".####", "....#", ".####", "#...#", ".####"),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".####", "#....", "#....", "#....", ".####"),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".####"),
    "f": ("..##.", ".#...", "#####", ".#...", ".#...", ".#...", ".#..."),
    "g": (".....", ".....", ".####", "#...#", ".####", "....#", ".###."),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    "j": ("...#.", ".....", "..##.", "...#.", "...#.", "#..#.", ".##.."),
    "k": ("#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "####.", "#....", "#...."),
    "q": (".....", ".....", ".####", "#...#", ".####", "....#", "....#"),
    "r": (".....", ".....", "#.##.", "##..#", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "#####", ".#...", ".#...", ".#..#", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ";": (".....", ".....", ".##..", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".....", ".##..", ".....", ".....", ".##..", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
}

# ---------------------------------------------------------------------------
# Page content: the day's eight stories.
# ---------------------------------------------------------------------------
MASTHEAD = "THE WORLD IN ONE IMAGE"
DATELINE = "SUNDAY 22 NOVEMBER 2026"
LEAD_HEADLINE = "COP31 COLLAPSES IN ANTALYA"
LEAD_KICKER = "Final climate deal names no fossil fuels; EU rejects it"
STORIES = [
    ("INDONESIA FACTORY FIRE: 3 DEAD, 36 MISSING",
     "Rescuers search candy factory ruins in Banten, Java"),
    ("NIGERIA FUNERAL BOAT TOLL RISES TO 24",
     "Emergency agency confirms toll after Bayelsa capsize"),
    ("BAHRAIN: IRANIAN ATTACK HITS CIVILIAN SITE",
     "Industrial facility struck; two injured, says Manama"),
    ("S. KOREA EDUCATION MINISTER QUITS",
     "Resigns over AI-cheating chaos around entrance exam"),
    ("RUSSIAN CARGO SHIP STILL BURNING OFF FINLAND",
     "Sparta II ablaze after drone strike; crew evacuated"),
    ("VERSTAPPEN WINS LAS VEGAS THRILLER",
     "Beats Norris by 0.6s in a race of 35 lead changes"),
    ("ITALY AIRPORT STRIKES HIT MILAN AND VENICE",
     "Controllers and airport staff walk out on Sunday"),
]

MARGIN = 36
CONTENT_W = W - 2 * MARGIN


class Canvas:
    def __init__(self):
        self.px = bytearray(bytes(PAPER) * (W * H))

    def rect(self, x, y, w, h, color):
        row = bytes(color) * w
        for yy in range(y, y + h):
            off = (yy * W + x) * 3
            self.px[off:off + 3 * w] = row

    def text_width(self, text, scale):
        if not text:
            return 0
        return len(text) * 6 * scale - scale

    def text(self, x, y, text, scale, color):
        for ch in text:
            glyph = FONT[ch]
            for r in range(7):
                row = glyph[r]
                for c in range(5):
                    if row[c] == "#":
                        self.rect(x + c * scale, y + r * scale,
                                  scale, scale, color)
            x += 6 * scale
        return x

    def text_centered(self, y, text, scale, color):
        x = (W - self.text_width(text, scale)) // 2
        self.text(x, y, text, scale, color)

    def wrap(self, text, scale, max_width):
        """Split text into lines that fit max_width at the given scale."""
        max_chars = (max_width + scale) // (6 * scale)
        lines = []
        current = ""
        for word in text.split(" "):
            trial = word if not current else current + " " + word
            if len(trial) <= max_chars:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines


def draw():
    cv = Canvas()
    y = 28

    # Masthead.
    cv.text_centered(y, MASTHEAD, 5, INK)
    y += 35 + 9
    # Newspaper double rule.
    cv.rect(MARGIN, y, CONTENT_W, 5, INK)
    cv.rect(MARGIN, y + 8, CONTENT_W, 2, INK)
    y += 10 + 10

    # Dateline.
    cv.text_centered(y, DATELINE, 4, RED)
    y += 28 + 12

    # Lead story, with a red side bar matched to the block's real height.
    lead_x = MARGIN + 24
    lead_lines = cv.wrap(LEAD_KICKER, 3, W - lead_x - MARGIN)
    bar_h = 42 + 8 + len(lead_lines) * 21 + (len(lead_lines) - 1) * 3
    cv.rect(MARGIN, y, 10, bar_h, RED)
    cv.text(lead_x, y, LEAD_HEADLINE, 6, INK)
    y += 42 + 8
    for line in lead_lines:
        cv.text(lead_x, y, line, 3, DARK)
        y += 21 + 3
    y += 10

    # The other seven stories. Kickers wrap to the headline column width so
    # no line ever crosses the right margin.
    for i, (headline, kicker) in enumerate(STORIES):
        cv.rect(MARGIN, y, CONTENT_W, 2, HAIR)
        y += 8
        num = str(i + 1) + "."
        cv.text(MARGIN, y, num, 4, RED)
        head_x = MARGIN + 48
        head_lines = cv.wrap(headline, 4, W - head_x - MARGIN)
        for line in head_lines:
            cv.text(head_x, y, line, 4, INK)
            y += 28 + 3
        y += 1
        for line in cv.wrap(kicker, 3, W - head_x - MARGIN):
            cv.text(head_x, y, line, 3, DARK)
            y += 21 + 3
        y += 9

    # Closing rule.
    cv.rect(MARGIN, y, CONTENT_W, 5, INK)
    return cv


def encode_png(cv):
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)  # filter type 0 (None) for every row
        raw += cv.px[yy * stride:(yy + 1) * stride]

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    return png


def output_path():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        os.makedirs(env, exist_ok=True)
        return os.path.join(env, "entry.png")
    try:
        os.makedirs("/output", exist_ok=True)
        return "/output/entry.png"
    except OSError:
        return "./entry.png"


def main():
    png = encode_png(draw())
    path = output_path()
    with open(path, "wb") as fh:
        fh.write(png)


if __name__ == "__main__":
    main()
