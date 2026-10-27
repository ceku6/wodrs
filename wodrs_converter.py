#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wodrs_converter.py — SI (Unicode Sinhala) → wodrs EN (legacy bytes)

Usage:
  python wodrs_converter.py                    (interactive mode)
  python wodrs_converter.py input.txt output.txt  (file mode)
"""

import sys
import unicodedata

# ============================================================
# CONSONANTS
# ============================================================
CONSONANTS = {
    '\u0D85': 0x77,  # අ → w
    '\u0D89': 0x62,  # ඉ → b
    '\u0D8B': 0x57,  # උ → W
    '\u0D8D': 0x52,  # ඍ → R
    '\u0D91': 0x74,  # එ → t
    '\u0D94': 0x54,  # ඔ → T
    '\u0D9A': 0x6C,  # ක → l
    '\u0D9B': 0x4C,  # ඛ → L
    '\u0D9C': 0x2E,  # ග → .
    '\u0D9D': 0x3E,  # ඝ → >
    '\u0D9E': 0x3F,  # ඞ → ?
    '\u0D9F': 0xD5,  # ඟ → 0xD5
    '\u0DA0': 0x70,  # ච → p
    '\u0DA1': 0x50,  # ඡ → P
    '\u0DA2': 0x63,  # ජ → c
    '\u0DA3': 0x3F,  # ඣ → ?
    '\u0DA6': 0x3F,  # ඦ → ?
    '\u0DA7': 0x67,  # ට → g
    '\u0DA8': 0x47,  # ඨ → G
    '\u0DA9': 0x76,  # ඩ → v
    '\u0DAA': 0x56,  # ඪ → V
    '\u0DAB': 0x4B,  # ණ → K
    '\u0DAC': 0xCB,  # ඬ → 0xCB
    '\u0DAD': 0x3B,  # ත → ;
    '\u0DAE': 0x3A,  # ථ → :
    '\u0DAF': 0x6F,  # ද → o
    '\u0DB0': 0x4F,  # ධ → O
    '\u0DB1': 0x6B,  # න → k
    '\u0DB3': 0x7C,  # ඳ → |
    '\u0DB4': 0x6D,  # ප → m
    '\u0DB5': 0x4D,  # ඵ → M
    '\u0DB6': 0x6E,  # බ → n
    '\u0DB7': 0x4E,  # භ → N
    '\u0DB8': 0x75,  # ම → u
    '\u0DB9': 0x55,  # ඹ → U
    '\u0DBA': 0x68,  # ය → h
    '\u0DBB': 0x72,  # ර → r
    '\u0DBD': 0x2C,  # ල → ,
    '\u0DC0': 0x6A,  # ව → j
    '\u0DC1': 0x59,  # ශ → Y
    '\u0DC2': 0x49,  # ෂ → I
    '\u0DC3': 0x69,  # ස → i
    '\u0DC4': 0x79,  # හ → y
    '\u0DC5': 0x3C,  # ළ → <
    '\u0DC6': 0x46,  # ෆ → F
}

# ============================================================
# VOWELS_MULTI
# ============================================================
VOWELS_MULTI = {
    '\u0D86': [0x77, 0x64],        # ආ → wd
    '\u0D87': [0x77, 0x65],        # ඇ → we
    '\u0D88': [0x77, 0x45],        # ඈ → wE
    '\u0D8A': [0x42],              # ඊ → B
    '\u0D8C': [0x57, 0x21],        # ඌ → W!
    '\u0D8E': [0x69, 0x44, 0x44],  # ඎ → iDD
    '\u0D92': [0x74, 0x61],        # ඒ → ta
    '\u0D93': [0x66, 0x74],        # ඓ → ft
    '\u0D96': [0x54, 0x21],        # ඖ → T!
}

# ============================================================
# COMPONENT: ඤ/ඥ
# ============================================================
COMPONENT = {
    '\u0DA4': [0x5B, 0x6F],  # ඤ → [ o
    '\u0DA5': [0x7B, 0x6F],  # ඥ → { o
}

# ============================================================
# GROUP 2
# ============================================================
GROUP2 = {
    '\u0D9A',  # ක
    '\u0D9C',  # ග
    '\u0DAD',  # ත
    '\u0DB7',  # භ
    '\u0DC1',  # ශ
}

# ============================================================
# 17 SHAPE-CHANGING CONSONANTS
# ============================================================
PRECOMPOSED_HAL = {
    '\u0D9B': 0xC4, '\u0DA0': 0xC9, '\u0DA1': 0xFE,
    '\u0DA2': 0xCA, '\u0DA7': 0xDC, '\u0DA9': 0xE2,
    '\u0DAC': 0xE5, '\u0DB0': 0xE8, '\u0DB6': 0xED,
    '\u0DB8': 0xEF, '\u0DB9': 0xF2, '\u0DBB': 0xBE,
    '\u0DC0': 0xF5,
}

PRECOMPOSED_I = {
    '\u0D9B': 0xC5, '\u0DA0': 0xD1, '\u0DA1': 0xFD,
    '\u0DA2': 0xDB, '\u0DA7': 0xE1, '\u0DA8': 0xC0,
    '\u0DA9': 0xE4, '\u0DAA': 0xCE, '\u0DAC': 0xE7,
    '\u0DAE': 0xD3, '\u0DB0': 0xEA, '\u0DB5': 0xDD,
    '\u0DB6': 0xEC, '\u0DB8': 0xF1, '\u0DB9': 0xF4,
    '\u0DBB': 0xDF, '\u0DC0': 0xFA,
}

PRECOMPOSED_II = {
    '\u0D9B': 0xC7, '\u0DA0': 0xD6, '\u0DA1': 0xC2,
    '\u0DA2': 0xD4, '\u0DA7': 0xE0, '\u0DA8': 0xC1,
    '\u0DA9': 0xE3, '\u0DAA': 0xD0, '\u0DAC': 0xE9,
    '\u0DAE': 0xD2, '\u0DB0': 0xEB, '\u0DB5': 0xDA,
    '\u0DB6': 0xEE, '\u0DB8': 0xF3, '\u0DB9': 0xF6,
    '\u0DBB': 0xCD, '\u0DC0': 0xF9,
}

# ============================================================
# PILLAS
# ============================================================
PILLAS = {
    '\u0DCF': [0x64], '\u0DD0': [0x65], '\u0DD1': [0x45],
    '\u0DD2': [0x73], '\u0DD3': [0x53],
    '\u0DD4': [0x71], '\u0DD6': [0x51],
    '\u0DD8': [0x44], '\u0DF2': [0x44, 0x44],
    '\u0DCA': [0x61],
}

# ============================================================
# KOMBUVA-BASED PILLAS
# ============================================================
KOMBUVA_PILLAS = {
    '\u0DD9': ([0x66], []),
    '\u0DDA': ([0x66], [0x61]),
    '\u0DDB': ([0x66, 0x66], []),
    '\u0DDC': ([0x66], [0x64]),
    '\u0DDD': ([0x66], [0x64, 0x61]),
    '\u0DDE': ([0x66], [0x21]),
}

# ============================================================
# SPECIAL
# ============================================================
SPECIAL = {
    '\u0D82': [0x78],  # ං → x
    '\u0D83': [0x58],  # ඃ → X
    '\u0D95': [0xB4],  # ඕ → 0xB4
    '\u0DDF': [0x21],  # ෟ → !
}

# ============================================================
# PRECOMPOSED
# ============================================================
PRECOMPOSED = {
    ('\u0DAF', '\u0DD4'): [0xFF],        # දු
    ('\u0DAF', '\u0DD6'): [0xA5],        # දූ
    ('\u0DB3', '\u0DD4'): [0xF7],        # ඳු
    ('\u0DB3', '\u0DD6'): [0xAA],        # ඳූ
    ('\u0DBD', '\u0DD4'): [0xA8],        # ලු
    ('\u0DBD', '\u0DD6'): [0xC6],        # ලූ
    ('\u0DC5', '\u0DD4'): [0xBF],        # ළු
    ('\u0DC5', '\u0DD6'): [0xBF, 0x45],  # ළූ
    ('\u0DBB', '\u0DD0'): [0x2F],        # රැ → /
    ('\u0DBB', '\u0DD1'): [0x3F],        # රෑ → ?
    ('\u0DBB', '\u0DD4'): [0x72, 0x65],  # රු → re
    ('\u0DBB', '\u0DD6'): [0x72, 0x45],  # රූ → rE
    ('\u0DA4', '\u0DD4'): [0x5B, 0xFF],  # ඤු → [ÿ
    ('\u0DA4', '\u0DD6'): [0x5B, 0xA5],  # ඤූ → [¥
    ('\u0DA5', '\u0DD4'): [0x7B, 0xFF],  # ඥු → {ÿ
    ('\u0DA5', '\u0DD6'): [0x7B, 0xA5],  # ඥූ → {¥
}

# ============================================================
# PUNCTUATION
# ============================================================
PUNCTUATION = {
    '\u002E': [0x27],        # . → '
    '\u002C': [0x22],        # , → "
    '\u003B': [0xB7],        # ; → Alt+0183
    '\u003A': [0x28],        # : → (
    '\u003F': [0x40],        # ? → @
    '\u0021': [0x60],        # ! → `
    '\u002F': [0x24],        # / → $
    '\u0028': [0x5E],        # ( → ^
    '\u0029': [0x26],        # ) → &
    '\u003D': [0x7D],        # = → }
    '\u002B': [0xA4],        # + → Alt+0164
    '\u00D7': [0x8B],        # × → Alt+0139
    '\u2018': [0x7A],        # ' → z
    '\u2019': [0x5A],        # ' → Z
    '\u201C': [0x7A, 0x7A],  # " → zz
    '\u201D': [0x5A, 0x5A],  # " → ZZ
}


# ============================================================
# CONVERTER
# ============================================================
def si_to_wodrs(text):
    """Convert Unicode Sinhala → wodrs legacy bytes."""

    # Fix broken ඕ keyboard bug
    text = text.replace('\u0D94\u0DCA', '\u0D95')

    # NFD decompose
    text = unicodedata.normalize('NFD', text)

    # Yansaya: ්‍ය → H
    text = text.replace('\u0DCA\u200D\u0DBA', 'H')

    out = bytearray()
    i = 0
    n = len(text)

    # Quote state tracking
    single_open = False
    double_open = False

    while i < n:
        ch = text[i]

        # --- Reph: ර + ් + ZWJ + consonant ---
        if ch == '\u0DBB' and i + 3 < n \
           and text[i+1] == '\u0DCA' and text[i+2] == '\u200D':
            next_ch = text[i+3]
            if next_ch in CONSONANTS:
                out.append(CONSONANTS[next_ch])
                out.append(0x5F)  # reph
                i += 4
                continue
            # Fallback: reph alone (shouldn't normally happen)
            out.append(0x5F)
            i += 3
            continue

        # --- ZWJ alone ---
        if ch == '\u200D':
            i += 1
            continue

        # ============================================================
        # ්‍ර (rakaransaya) handling
        # ============================================================

        # --- ද + ්‍ර (precomposed 0xF8) ---
        if i + 3 < n and ch == '\u0DAF' \
           and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB':
            out.append(0xF8)
            i += 4
            continue

        # --- Consonant + ්‍ර + ි ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD2':
            if ch in PRECOMPOSED_I:
                out.append(PRECOMPOSED_I[ch])
            else:
                out.append(CONSONANTS.get(ch, ord(ch)))
                out.append(0x73)
            out.append(0x25)
            i += 5
            continue

        # --- Consonant + ්‍ර + ී ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD3':
            if ch in PRECOMPOSED_II:
                out.append(PRECOMPOSED_II[ch])
            else:
                out.append(CONSONANTS.get(ch, ord(ch)))
                out.append(0x53)
            out.append(0x25)
            i += 5
            continue

        # --- Consonant + ්‍ර + ැ ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD0':
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            out.append(0x65)
            i += 5
            continue

        # --- Consonant + ්‍ර + ෑ ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD1':
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            out.append(0x45)
            i += 5
            continue

        # --- Consonant + ්‍ර + ා ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DCF':
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            out.append(0x64)
            i += 5
            continue

        # --- Consonant + ්‍ර + ේ (kombuva + ්) ---
        if i + 5 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD9' \
           and text[i+5] == '\u0DCA':
            out.append(0x66)
            if ch in PRECOMPOSED_HAL:
                out.append(PRECOMPOSED_HAL[ch])
            else:
                out.append(CONSONANTS.get(ch, ord(ch)))
                out.append(0x61)
            out.append(0x25)
            i += 6
            continue

        # --- Consonant + ්‍ර + ො (kombuva + ා) ---
        if i + 5 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD9' \
           and text[i+5] == '\u0DCF':
            out.append(0x66)
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            out.append(0x64)
            i += 6
            continue

        # --- Consonant + ්‍ර + ෝ (kombuva + ා + ්) ---
        if i + 6 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD9' \
           and text[i+5] == '\u0DCF' and text[i+6] == '\u0DCA':
            out.append(0x66)
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            out.append(0x64)
            out.append(0x61)
            i += 7
            continue

        # --- Consonant + ්‍ර + ෙ (kombuva only) ---
        if i + 4 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB' and text[i+4] == '\u0DD9':
            out.append(0x66)
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            i += 5
            continue

        # --- Consonant + ්‍ර (no pilla) ---
        if i + 3 < n and text[i+1] == '\u0DCA' and text[i+2] == '\u200D' \
           and text[i+3] == '\u0DBB':
            out.append(CONSONANTS.get(ch, ord(ch)))
            out.append(0x25)
            i += 4
            continue

        # ============================================================
        # Regular handling
        # ============================================================

        # --- PRECOMPOSED (consonant + pilla) ---
        if i + 1 < n and (ch, text[i+1]) in PRECOMPOSED:
            for b in PRECOMPOSED[(ch, text[i+1])]:
                out.append(b)
            i += 2
            continue

        # --- VOWELS_MULTI ---
        if ch in VOWELS_MULTI:
            for b in VOWELS_MULTI[ch]:
                out.append(b)
            i += 1
            continue

        # --- COMPONENT (ඤ/ඥ) ---
        if ch in COMPONENT:
            for b in COMPONENT[ch]:
                out.append(b)
            i += 1
            continue

        # --- 17-list: consonant + ෙ + ් (NFD of ේ) ---
        if i + 2 < n and ch in PRECOMPOSED_HAL \
           and text[i+1] == '\u0DD9' and text[i+2] == '\u0DCA':
            out.append(0x66)
            out.append(PRECOMPOSED_HAL[ch])
            i += 3
            continue

        # --- 17-list: consonant + ් (standalone) ---
        if i + 1 < n and ch in PRECOMPOSED_HAL and text[i+1] == '\u0DCA':
            out.append(PRECOMPOSED_HAL[ch])
            i += 2
            continue

        # --- 17-list: consonant + ි ---
        if i + 1 < n and ch in PRECOMPOSED_I and text[i+1] == '\u0DD2':
            out.append(PRECOMPOSED_I[ch])
            i += 2
            continue

        # --- 17-list: consonant + ී ---
        if i + 1 < n and ch in PRECOMPOSED_II and text[i+1] == '\u0DD3':
            out.append(PRECOMPOSED_II[ch])
            i += 2
            continue

        # --- Consonant + kombuva-based pilla (reorder) ---
        if ch in CONSONANTS and i + 1 < n and text[i+1] in KOMBUVA_PILLAS:
            kp, rp = KOMBUVA_PILLAS[text[i+1]]
            for b in kp:
                out.append(b)
            out.append(CONSONANTS[ch])
            for b in rp:
                out.append(b)
            i += 2
            continue

        # --- Consonant + ු/ූ (Group 2 override) ---
        if ch in CONSONANTS and i + 1 < n and text[i+1] in ('\u0DD4', '\u0DD6'):
            if ch in GROUP2:
                out.append(CONSONANTS[ch])
                out.append(0x3D if text[i+1] == '\u0DD4' else 0x2B)
            else:
                out.append(CONSONANTS[ch])
                out.append(0x71 if text[i+1] == '\u0DD4' else 0x51)
            i += 2
            continue

        # --- Plain consonant ---
        if ch in CONSONANTS:
            out.append(CONSONANTS[ch])
            i += 1
            continue

        # --- Standalone kombuva pilla ---
        if ch in KOMBUVA_PILLAS:
            kp, rp = KOMBUVA_PILLAS[ch]
            for b in kp:
                out.append(b)
            for b in rp:
                out.append(b)
            i += 1
            continue

        # --- Regular pilla ---
        if ch in PILLAS:
            for b in PILLAS[ch]:
                out.append(b)
            i += 1
            continue

        # --- SPECIAL ---
        if ch in SPECIAL:
            for b in SPECIAL[ch]:
                out.append(b)
            i += 1
            continue

        # ============================================================
        # Quote handling with state tracking
        # ============================================================

        # --- Straight double quote (U+0022) ---
        if ch == '\u0022':
            if double_open:
                out.append(0x5A)
                out.append(0x5A)  # ZZ = close double
                double_open = False
            else:
                out.append(0x7A)
                out.append(0x7A)  # zz = open double
                double_open = True
            i += 1
            continue

        # --- Straight single quote (U+0027) — may be part of '' ---
        if ch == '\u0027':
            # Check for '' pair (double quote)
            if i + 1 < n and text[i+1] == '\u0027':
                if double_open:
                    out.append(0x5A)
                    out.append(0x5A)  # ZZ = close double
                    double_open = False
                else:
                    out.append(0x7A)
                    out.append(0x7A)  # zz = open double
                    double_open = True
                i += 2
                continue
            # Single quote
            if single_open:
                out.append(0x5A)  # Z = close single
                single_open = False
            else:
                out.append(0x7A)  # z = open single
                single_open = True
            i += 1
            continue

        # --- PUNCTUATION (including curly quotes) ---
        if ch in PUNCTUATION:
            for b in PUNCTUATION[ch]:
                out.append(b)
            i += 1
            continue

        # --- Unknown ---
        try:
            out.append(ord(ch))
        except (ValueError, OverflowError):
            pass
        i += 1

    return bytes(out)


def convert_file(input_path, output_path):
    print(f"Reading: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"Input length: {len(text)} characters")
    result = si_to_wodrs(text)
    with open(output_path, 'wb') as f:
        f.write(result)
    print(f"Output: {output_path}")
    print(f"Output bytes: {len(result)}")
    print()
    print("Done. Open output file in Notepad with wodrs font.")


def interactive_mode():
    print("=" * 60)
    print("Wij 9 SI → wodrs EN Converter (interactive)")
    print("=" * 60)
    print()
    print("Paste Sinhala text, press Enter. Type 'exit' to quit.")
    print()

    while True:
        try:
            text = input("SI > ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if text.strip().lower() in ('exit', 'quit', 'q', 'x'):
            break
        if not text:
            continue

        result = si_to_wodrs(text)
        hex_str = ' '.join(f'{b:02X}' for b in result)
        latin = result.decode('latin-1')

        print()
        print(f"  Input:   {text}")
        print(f"  Hex:     {hex_str}")
        print(f"  wodrs:   {latin}")
        print(f"  Bytes:   {len(result)}")
        print()


def main():
    if len(sys.argv) == 3:
        convert_file(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        interactive_mode()
    else:
        print("Usage:")
        print("  python wodrs_converter.py                       (interactive)")
        print("  python wodrs_converter.py input.txt output.txt  (file mode)")
        sys.exit(1)


if __name__ == '__main__':
    main()