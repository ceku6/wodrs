#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wodrs_to_si.py — wodrs EN (legacy bytes) → SI (Unicode Sinhala)
"""

import sys
import unicodedata

# ---------- TABLES ----------
CONSONANT_INV = {
    0x77: '\u0D85', 0x62: '\u0D89', 0x57: '\u0D8B', 0x52: '\u0D8D',
    0x74: '\u0D91', 0x54: '\u0D94',
    0x6C: '\u0D9A', 0x4C: '\u0D9B', 0x2E: '\u0D9C', 0x3E: '\u0D9D',
    0x3F: '\u0D9E', 0xD5: '\u0D9F',
    0x70: '\u0DA0', 0x50: '\u0DA1', 0x63: '\u0DA2',
    0x67: '\u0DA7', 0x47: '\u0DA8', 0x76: '\u0DA9', 0x56: '\u0DAA',
    0x4B: '\u0DAB', 0xCB: '\u0DAC',
    0x3B: '\u0DAD', 0x3A: '\u0DAE',
    0x6F: '\u0DAF', 0x4F: '\u0DB0', 0x6B: '\u0DB1', 0x7C: '\u0DB3',
    0x6D: '\u0DB4', 0x4D: '\u0DB5', 0x6E: '\u0DB6', 0x4E: '\u0DB7',
    0x75: '\u0DB8', 0x55: '\u0DB9',
    0x68: '\u0DBA', 0x72: '\u0DBB', 0x2C: '\u0DBD', 0x6A: '\u0DC0',
    0x59: '\u0DC1', 0x49: '\u0DC2', 0x69: '\u0DC3', 0x79: '\u0DC4',
    0x3C: '\u0DC5', 0x46: '\u0DC6',
}

GROUP2 = {0x6C, 0x2E, 0x3B, 0x4E, 0x59}   # ක ග ත භ ශ

VOWELS_MULTI_INV = {
    (0x77, 0x64): '\u0D86', (0x77, 0x65): '\u0D87', (0x77, 0x45): '\u0D88',
    (0x42,): '\u0D8A',
    (0x57, 0x21): '\u0D8C', (0x69, 0x44, 0x44): '\u0D8E',
    (0x74, 0x61): '\u0D92', (0x66, 0x74): '\u0D93', (0x54, 0x21): '\u0D96',
}

COMPONENT_INV = {(0x5B, 0x6F): '\u0DA4', (0x7B, 0x6F): '\u0DA5'}

PRECOMPOSED_HAL_INV = {
    0xC4:'\u0D9B',0xC9:'\u0DA0',0xFE:'\u0DA1',0xCA:'\u0DA2',0xDC:'\u0DA7',
    0xE2:'\u0DA9',0xE5:'\u0DAC',0xE8:'\u0DB0',0xED:'\u0DB6',0xEF:'\u0DB8',
    0xF2:'\u0DB9',0xBE:'\u0DBB',0xF5:'\u0DC0',
}
PRECOMPOSED_I_INV = {
    0xC5:'\u0D9B',0xD1:'\u0DA0',0xFD:'\u0DA1',0xDB:'\u0DA2',0xE1:'\u0DA7',
    0xC0:'\u0DA8',0xE4:'\u0DA9',0xCE:'\u0DAA',0xE7:'\u0DAC',0xD3:'\u0DAE',
    0xEA:'\u0DB0',0xDD:'\u0DB5',0xEC:'\u0DB6',0xF1:'\u0DB8',0xF4:'\u0DB9',
    0xDF:'\u0DBB',0xFA:'\u0DC0',
}
PRECOMPOSED_II_INV = {
    0xC7:'\u0D9B',0xD6:'\u0DA0',0xC2:'\u0DA1',0xD4:'\u0DA2',0xE0:'\u0DA7',
    0xC1:'\u0DA8',0xE3:'\u0DA9',0xD0:'\u0DAA',0xE9:'\u0DAC',0xD2:'\u0DAE',
    0xEB:'\u0DB0',0xDA:'\u0DB5',0xEE:'\u0DB6',0xF3:'\u0DB8',0xF6:'\u0DB9',
    0xCD:'\u0DBB',0xF9:'\u0DC0',
}

PILLA_INV = {
    0x64:'\u0DCF',0x65:'\u0DD0',0x45:'\u0DD1',0x73:'\u0DD2',0x53:'\u0DD3',
    0x71:'\u0DD4',0x51:'\u0DD6',0x44:'\u0DD8',0x61:'\u0DCA',
}

SPECIAL_INV = {0x78:'\u0D82',0x58:'\u0D83',0xB4:'\u0D95'}

PRECOMPOSED_INV = {
    (0xFF,):'\u0DAF\u0DD4',(0xA5,):'\u0DAF\u0DD6',
    (0xF7,):'\u0DB3\u0DD4',(0xAA,):'\u0DB3\u0DD6',
    (0xA8,):'\u0DBD\u0DD4',(0xC6,):'\u0DBD\u0DD6',
    (0xBF,):'\u0DC5\u0DD4',(0xBF,0x45):'\u0DC5\u0DD6',
    (0x2F,):'\u0DBB\u0DD0',(0x3F,):'\u0DBB\u0DD1',
    (0x72,0x65):'\u0DBB\u0DD4',(0x72,0x45):'\u0DBB\u0DD6',
    (0x5B,0xFF):'\u0DA4\u0DD4',(0x5B,0xA5):'\u0DA4\u0DD6',
    (0x7B,0xFF):'\u0DA5\u0DD4',(0x7B,0xA5):'\u0DA5\u0DD6',
}

PUNCT_INV = {
    0x27:'.',0x22:',',0xB7:';',0x28:':',0x40:'?',0x60:'!',
    0x24:'/',0x5E:'(',0x26:')',0x7D:'=',0xA4:'+',0x8B:'\u00D7',
}

# ---------- TRIE ----------
class TrieNode:
    __slots__ = ('children','value')
    def __init__(self): self.children={}; self.value=None

def build_trie(mapping):
    root=TrieNode()
    for k,v in mapping.items():
        if isinstance(k,int): k=(k,)
        node=root
        for b in k: node=node.children.setdefault(b,TrieNode())
        node.value=v
    return root

def trie_match(root,data,pos):
    node=root; best_val=None; best_len=0; i=pos; n=len(data)
    while i<n and data[i] in node.children:
        node=node.children[data[i]]; i+=1
        if node.value is not None: best_val,best_len=node.value,i-pos
    return best_val,best_len

# ---------- HELPERS ----------
def last_is_sinhala_consonant(out):
    if not out: return False
    s=out[-1]
    if not s: return False
    c=s[-1]
    return '\u0D9A' <= c <= '\u0DC6'

def append_to_last(out,suffix):
    if out: out[-1]=out[-1]+suffix
    else: out.append(suffix)

# ---------- MAIN ----------
def wodrs_to_si(data: bytes) -> str:
    trie_vowels    = build_trie(VOWELS_MULTI_INV)
    trie_component = build_trie(COMPONENT_INV)
    trie_precomp   = build_trie(PRECOMPOSED_INV)
    consonant_bytes = set(CONSONANT_INV.keys())

    out=[]; i=0; n=len(data)
    single_open=False; double_open=False

    while i<n:
        b=data[i]

        # 0. YANSAYA
        if b==0x48:
            out.append('\u0DCA\u200D\u0DBA'); i+=1; continue

        # 1. REPH: cons + 0x5F
        if i+1<n and data[i+1]==0x5F and b in consonant_bytes:
            out.append('\u0DBB\u0DCA\u200D'+CONSONANT_INV[b]); i+=2; continue

        # 2. RAKARANSAYA: cons + 0x25
        if i+1<n and data[i+1]==0x25 and b in consonant_bytes:
            out.append(CONSONANT_INV[b]+'\u0DCA\u200D\u0DBB'); i+=2; continue

        # precomp + 0x25
        if i+1<n and data[i+1]==0x25:
            if b in PRECOMPOSED_I_INV:
                out.append(PRECOMPOSED_I_INV[b]+'\u0DCA\u200D\u0DBB\u0DD2'); i+=2; continue
            if b in PRECOMPOSED_II_INV:
                out.append(PRECOMPOSED_II_INV[b]+'\u0DCA\u200D\u0DBB\u0DD3'); i+=2; continue
            if b in PRECOMPOSED_HAL_INV:
                out.append(PRECOMPOSED_HAL_INV[b]+'\u0DCA\u200D\u0DBB\u0DCA'); i+=2; continue

        # orphan 0x25 — attach rakaransaya to the preceding consonant,
        # inserting it BEFORE any pilla that follows the consonant.
        if b == 0x25:
            attached = False
            for k in range(len(out) - 1, -1, -1):
                s = out[k]
                if not s:
                    continue
                c = s[-1]
                # Sinhala consonant range
                if '\u0D9A' <= c <= '\u0DC6':
                    # insert hal+ZWJ+ra right after the consonant,
                    # i.e. before any pills already appended to that chunk
                    # Find position within s: consonant may be followed by pilla
                    # Simplest: split s at the consonant boundary
                    # s looks like "<consonant><maybe pillas>"
                    # We rebuild: consonant + ්‍ර + rest
                    cons = s[0]
                    rest = s[1:]
                    out[k] = cons + '\u0DCA\u200D\u0DBB' + rest
                    attached = True
                    break
                # Stop scanning if we hit a non-pilla, non-consonant character
                # (space, punctuation, another word) — the 0x25 is genuinely orphan.
                if not ('\u0D9A' <= c <= '\u0DFF'):
                    break
            if not attached:
                out.append('%')
            i += 1
            continue

        # 3. GROUP2: = (ු) and + (ූ)
        if i+1<n and b in GROUP2 and data[i+1]==0x3D:
            out.append(CONSONANT_INV[b]+'\u0DD4'); i+=2; continue
        if i+1<n and b in GROUP2 and data[i+1]==0x2B:
            out.append(CONSONANT_INV[b]+'\u0DD6'); i+=2; continue
        if b==0x3D:
            if last_is_sinhala_consonant(out): append_to_last(out,'\u0DD4')
            else: out.append('=')
            i+=1; continue
        if b==0x2B:
            if last_is_sinhala_consonant(out): append_to_last(out,'\u0DD6')
            else: out.append('+')
            i+=1; continue

        # 4a. RAKARANSAYA + kombuva
        # 4a-pre. RAKARANSAYA + kombuva + hal:  0x66 + cons + 0x61 + 0x25
        #   → consonant + ්‍ර + ේ
        if b==0x66 and i+3<n and data[i+2]==0x61 and data[i+3]==0x25 \
           and data[i+1] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+1]] + '\u0DCA\u200D\u0DBB\u0DDA')
            i += 4
            continue
        if b==0x66 and i+2<n and data[i+2]==0x25:
            mid=data[i+1]
            if mid in consonant_bytes:
                out.append(CONSONANT_INV[mid]+'\u0DCA\u200D\u0DBB\u0DD9'); i+=3; continue
            if mid in PRECOMPOSED_HAL_INV:
                out.append(PRECOMPOSED_HAL_INV[mid]+'\u0DCA\u200D\u0DBB\u0DDA'); i+=3; continue
        if b==0x66 and i+3<n and data[i+2]==0x25 and data[i+3]==0x64:
            mid=data[i+1]
            if mid in consonant_bytes:
                out.append(CONSONANT_INV[mid]+'\u0DCA\u200D\u0DBB\u0DDC'); i+=4; continue
        if b==0x66 and i+4<n and data[i+2]==0x25 and data[i+3]==0x64 and data[i+4]==0x61:
            mid=data[i+1]
            if mid in consonant_bytes:
                out.append(CONSONANT_INV[mid]+'\u0DCA\u200D\u0DBB\u0DDD'); i+=5; continue
        if b==0x66 and i+3<n and data[i+2]==0x25 and data[i+3]==0x65:
            mid=data[i+1]
            if mid in consonant_bytes:
                out.append(CONSONANT_INV[mid]+'\u0DCA\u200D\u0DBB\u0DD0'); i+=4; continue
        if b==0x66 and i+3<n and data[i+2]==0x25 and data[i+3]==0x45:
            mid=data[i+1]
            if mid in consonant_bytes:
                out.append(CONSONANT_INV[mid]+'\u0DCA\u200D\u0DBB\u0DD1'); i+=4; continue

        # 4b. DOUBLE KOMBUVA: 66 66 = ෛ
        if b==0x66 and i+2<n and data[i+1]==0x66 and data[i+2] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+2]]+'\u0DDB'); i+=3; continue
        if b==0x66 and i+1<n and data[i+1]==0x66:
            if last_is_sinhala_consonant(out): append_to_last(out,'\u0DDB')
            else: out.append('\u0DD9\u0DD9')
            i+=2; continue

        # 4c. SINGLE KOMBUVA variants
        if b==0x66 and i+2<n and data[i+2]==0x64 and data[i+1] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+1]]+'\u0DDC'); i+=3; continue
        if b==0x66 and i+3<n and data[i+2]==0x64 and data[i+3]==0x61 and data[i+1] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+1]]+'\u0DDD'); i+=4; continue
        if b==0x66 and i+2<n and data[i+2]==0x21 and data[i+1] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+1]]+'\u0DDE'); i+=3; continue
        if b==0x66 and i+1<n and data[i+1] in consonant_bytes:
            out.append(CONSONANT_INV[data[i+1]]+'\u0DD9'); i+=2; continue
        if b==0x66 and i+1<n and data[i+1] in PRECOMPOSED_HAL_INV:
            out.append(PRECOMPOSED_HAL_INV[data[i+1]]+'\u0DDA'); i+=2; continue

        # 5. 0xF8
        if b==0xF8:
            out.append('\u0DAF\u0DCA\u200D\u0DBB'); i+=1; continue

        # 6. Precomposed pairs
        val,ln = trie_match(trie_precomp, data, i)
        if val is not None: out.append(val); i+=ln; continue

        # 7. Precomp I/II/HAL
        if b in PRECOMPOSED_I_INV:  out.append(PRECOMPOSED_I_INV[b]+'\u0DD2'); i+=1; continue
        if b in PRECOMPOSED_II_INV: out.append(PRECOMPOSED_II_INV[b]+'\u0DD3'); i+=1; continue
        if b in PRECOMPOSED_HAL_INV:out.append(PRECOMPOSED_HAL_INV[b]+'\u0DCA'); i+=1; continue

        # 8. ඤ/ඥ, vowels
        val,ln = trie_match(trie_component, data, i)
        if val is not None: out.append(val); i+=ln; continue
        val,ln = trie_match(trie_vowels, data, i)
        if val is not None: out.append(val); i+=ln; continue

        # 9. Quotes
        if b==0x7A and i+1<n and data[i+1]==0x7A:
            out.append('\u201D' if double_open else '\u201C'); double_open=not double_open; i+=2; continue
        if b==0x5A and i+1<n and data[i+1]==0x5A:
            out.append('\u201D' if double_open else '\u201C'); double_open=not double_open; i+=2; continue
        if b==0x7A:
            out.append('\u2019' if single_open else '\u2018'); single_open=not single_open; i+=1; continue
        if b==0x5A:
            out.append('\u2019' if single_open else '\u2018'); single_open=not single_open; i+=1; continue

        # 10. Punct
        if b in PUNCT_INV: out.append(PUNCT_INV[b]); i+=1; continue

        # 11. ! (standalone ෟ)
        if b==0x21: out.append('\u0DDF'); i+=1; continue

        # 12. Special
        if b in SPECIAL_INV: out.append(SPECIAL_INV[b]); i+=1; continue

        # 13. Plain consonant
        if b in CONSONANT_INV: out.append(CONSONANT_INV[b]); i+=1; continue

        # 13b. ෲ: 44 44
        if b==0x44 and i+1<n and data[i+1]==0x44:
            if last_is_sinhala_consonant(out): append_to_last(out,'\u0DF2')
            else: out.append('\u0DF2')
            i+=2; continue

        # 14. Plain pilla
        if b in PILLA_INV: out.append(PILLA_INV[b]); i+=1; continue

        # 15. Unknown
        out.append(chr(b)); i+=1

    return unicodedata.normalize('NFC', ''.join(out))

# ---------- I/O ----------
def convert_file(input_path, output_path):
    print(f"Reading: {input_path}")
    with open(input_path,'rb') as f: data=f.read()
    print(f"Input bytes: {len(data)}")
    result = wodrs_to_si(data)
    with open(output_path,'wb') as f: f.write(result.encode('utf-8'))
    print(f"Output: {output_path}")
    print(f"Output chars: {len(result)}")
    print("Done.")

def interactive_mode():
    print("wodrs EN → SI (interactive). Type 'exit' to quit.")
    while True:
        try: line=input("EN > ")
        except (EOFError,KeyboardInterrupt): print(); break
        if line.strip().lower() in ('exit','quit','q','x'): break
        if not line: continue
        print(f"  SI: {wodrs_to_si(line.encode('latin-1',errors='replace'))}")

def main():
    if len(sys.argv)==3: convert_file(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==1: interactive_mode()
    else: print("Usage: python wodrs_to_si.py input.bin output.txt"); sys.exit(1)

if __name__=='__main__': main()