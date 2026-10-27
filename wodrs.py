#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wodrs — Unicode Sinhala ↔ wodrs legacy bytes converter.

Usage:
    wodrs si2wodrs  <input>              # SI  → wodrs  (auto-name output)
    wodrs si2wodrs  <input> <output>     # SI  → wodrs  (explicit output)
    wodrs wodrs2si  <input>              # wodrs → SI   (auto-name output)
    wodrs wodrs2si  <input> <output>     # wodrs → SI   (explicit output)
    wodrs wodrs2si                       # interactive  (paste, Ctrl+D to exit)
    wodrs check     <input>              # round-trip self-test
"""

import argparse
import os
import sys

from wodrs_converter import si_to_wodrs
from wodrs_to_si import wodrs_to_si


def read_si(path):
    with open(path, 'rb') as f:
        data = f.read()
    if data.startswith(b'\xef\xbb\xbf'):
        data = data[3:]
    return data.decode('utf-8')


def read_wodrs(path):
    with open(path, 'rb') as f:
        return f.read()


def write_bytes(path, data):
    with open(path, 'wb') as f:
        f.write(data)


def _strip_direction_suffix(name):
    for suffix in ('_SI', '_EN'):
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


def auto_output_path(input_path, direction):
    folder = os.path.dirname(os.path.abspath(input_path))
    stem   = os.path.splitext(os.path.basename(input_path))[0]
    stem   = _strip_direction_suffix(stem)
    out_name = f"{stem}_{direction}.txt"
    return os.path.join(folder, out_name)


def cmd_si2wodrs(input_path, output_path):
    text = read_si(input_path)
    data = si_to_wodrs(text)
    write_bytes(output_path, data)
    print(f"si2wodrs:  {input_path}  →  {output_path}")
    print(f"  input : {len(text)} chars (UTF-8)")
    print(f"  output: {len(data)} bytes (wodrs)")


def cmd_wodrs2si(input_path, output_path):
    data = read_wodrs(input_path)
    text = wodrs_to_si(data)
    write_bytes(output_path, text.encode('utf-8'))
    print(f"wodrs2si:  {input_path}  →  {output_path}")
    print(f"  input : {len(data)} bytes (wodrs)")
    print(f"  output: {len(text)} chars (UTF-8)")


def cmd_check(input_path):
    text = read_si(input_path)
    orig = text.replace('\r\n', '\n')
    forward  = si_to_wodrs(text)
    backward = wodrs_to_si(forward)
    rt = backward.replace('\r\n', '\n')

    print(f"check: {input_path}")
    print(f"  Input :  {len(orig)} chars")
    print(f"  Output:  {len(rt)} chars")

    if orig == rt:
        print(f"  Diffs :  0")
        print(f"  Result: PASS")
        return 0

    diffs = []
    n = min(len(orig), len(rt))
    for i in range(n):
        if orig[i] != rt[i]:
            diffs.append((i, orig[i], rt[i]))

    print(f"  Diffs :  {len(diffs)}")
    quote_diffs = 0
    for i, a, b in diffs[:30]:
        tag = ""
        if a == '"' and b in ('\u201C', '\u201D'):
            tag = "  (straight → curly quote)"
            quote_diffs += 1
        elif a == "'" and b in ('\u2018', '\u2019'):
            tag = "  (straight → curly single quote)"
            quote_diffs += 1
        print(f"    pos {i:5}: U+{ord(a):04X} '{a}'  →  U+{ord(b):04X} '{b}'{tag}")

    if quote_diffs == len(diffs):
        print(f"  Result: OK — only quote normalization")
        return 0
    else:
        print(f"  Result: FAIL — unexpected differences")
        return 1


def cmd_interactive_wodrs2si():
    print("wodrs2si interactive — paste wodrs lines, Ctrl+Z Enter (Windows) to exit.")
    for line in sys.stdin:
        line = line.rstrip('\n')
        if not line:
            print()
            continue
        data = line.encode('latin-1', errors='replace')
        print(wodrs_to_si(data))


def build_parser():
    p = argparse.ArgumentParser(
        prog='wodrs',
        description='Unicode Sinhala ↔ wodrs legacy bytes converter.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest='cmd', metavar='<command>')

    a = sub.add_parser('si2wodrs', help='SI → wodrs')
    a.add_argument('input')
    a.add_argument('output', nargs='?')

    b = sub.add_parser('wodrs2si', help='wodrs → SI')
    b.add_argument('input',  nargs='?')
    b.add_argument('output', nargs='?')

    c = sub.add_parser('check', help='round-trip self-test')
    c.add_argument('input')

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        parser.print_help()
        return 0

    if args.cmd == 'si2wodrs':
        if not os.path.isfile(args.input):
            print(f"error: no such file: {args.input}", file=sys.stderr)
            return 1
        out = args.output or auto_output_path(args.input, 'EN')
        try:
            cmd_si2wodrs(args.input, out)
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        return 0

    if args.cmd == 'wodrs2si':
        if args.input is None:
            cmd_interactive_wodrs2si()
            return 0
        if not os.path.isfile(args.input):
            print(f"error: no such file: {args.input}", file=sys.stderr)
            return 1
        out = args.output or auto_output_path(args.input, 'SI')
        try:
            cmd_wodrs2si(args.input, out)
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        return 0

    if args.cmd == 'check':
        if not os.path.isfile(args.input):
            print(f"error: no such file: {args.input}", file=sys.stderr)
            return 1
        try:
            return cmd_check(args.input)
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            return 1

    parser.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
