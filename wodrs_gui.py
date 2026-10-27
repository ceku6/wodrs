#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wodrs_gui.py — two-pane GUI for the wodrs converter.

Left  : paste / type source text
Right : converted output (read-only)
"""

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont

from wodrs_converter import si_to_wodrs
from wodrs_to_si import wodrs_to_si


class WodrsApp:
    def __init__(self, root):
        self.root = root
        root.title("wodrs — Sinhala ↔ wodrs")
        root.geometry("980x620")
        root.minsize(700, 400)

        # ---------- Fonts -------------------------------------------------
        self.si_font  = self._pick_font(
            ("Iskoola Pota", "Noto Sans Sinhala", "Nirmala UI", "Segoe UI"),
            size=13,
        )
        self.wod_font = self._pick_font(
            ("Wodrs", "Consolas", "Lucida Console", "Courier New"),
            size=13,
        )

        # ---------- Mode bar ---------------------------------------------
        bar = ttk.Frame(root, padding=6)
        bar.pack(fill="x")

        self.mode = tk.StringVar(value="si2wodrs")
        ttk.Radiobutton(bar, text="Sinhala → wodrs",
                        variable=self.mode, value="si2wodrs",
                        command=self._on_mode_change).pack(side="left", padx=4)
        ttk.Radiobutton(bar, text="wodrs → Sinhala",
                        variable=self.mode, value="wodrs2si",
                        command=self._on_mode_change).pack(side="left", padx=4)

        ttk.Separator(bar, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Button(bar, text="Convert",      command=self.convert).pack(side="left", padx=4)
        ttk.Button(bar, text="Swap ↕",        command=self.swap).pack(side="left", padx=4)
        ttk.Button(bar, text="Clear",         command=self.clear).pack(side="left", padx=4)
        ttk.Button(bar, text="Copy result",   command=self.copy_right).pack(side="right", padx=4)

        # ---------- Two panes --------------------------------------------
        panes = ttk.PanedWindow(root, orient="horizontal")
        panes.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        left_frame  = ttk.Frame(panes)
        right_frame = ttk.Frame(panes)
        panes.add(left_frame,  weight=1)
        panes.add(right_frame, weight=1)

        ttk.Label(left_frame, text="Source").pack(anchor="w")
        self.left = tk.Text(left_frame, wrap="word", undo=True,
                            font=self.si_font, padx=8, pady=8)
        self.left.pack(fill="both", expand=True, side="left")
        sb_l = ttk.Scrollbar(left_frame, command=self.left.yview)
        sb_l.pack(side="right", fill="y")
        self.left.config(yscrollcommand=sb_l.set)

        ttk.Label(right_frame, text="Result (read-only)").pack(anchor="w")
        self.right = tk.Text(right_frame, wrap="word",
                             font=self.si_font, padx=8, pady=8,
                             background="#f7f7f7")
        self.right.pack(fill="both", expand=True, side="left")
        sb_r = ttk.Scrollbar(right_frame, command=self.right.yview)
        sb_r.pack(side="right", fill="y")
        self.right.config(yscrollcommand=sb_r.set, state="disabled")

        # ---------- Status bar ------------------------------------------
        self.status = tk.StringVar(value="Ready.")
        ttk.Label(root, textvariable=self.status, anchor="w",
                  padding=4, relief="sunken").pack(fill="x", side="bottom")

        # ---------- Shortcuts & paste handling --------------------------
        root.bind("<Control-Return>",   lambda e: (self.convert(), "break")[1])
        root.bind("<Control-Shift-S>",  lambda e: (self.swap(), "break")[1])
        root.bind("<Control-L>",        lambda e: (self.clear(), "break")[1])

        # Left pane: enable right-click paste menu (Ctrl+V works natively)
        self.left.bind("<Button-3>",    self._show_left_menu)

        # Focus left pane so the user can start typing immediately
        self.left.focus_set()

    # ---------- helpers ------------------------------------------------
    def _pick_font(self, candidates, size):
        families = set(tkfont.families())
        for name in candidates:
            if name in families:
                return (name, size)
        return ("TkDefaultFont", size)

    def _on_mode_change(self):
        if self.mode.get() == "si2wodrs":
            self.right.config(font=self.wod_font)
            self.status.set("Mode: Sinhala → wodrs")
        else:
            self.right.config(font=self.si_font)
            self.status.set("Mode: wodrs → Sinhala")
        self._set_right("")

    def _show_left_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Cut",   command=lambda: self.left.event_generate("<<Cut>>"))
        menu.add_command(label="Copy",  command=lambda: self.left.event_generate("<<Copy>>"))
        menu.add_command(label="Paste", command=lambda: self.left.event_generate("<<Paste>>"))
        menu.add_separator()
        menu.add_command(label="Select all", command=lambda: self.left.tag_add("sel", "1.0", "end"))
        menu.tk_popup(event.x_root, event.y_root)

    def _set_right(self, text):
        self.right.config(state="normal")
        self.right.delete("1.0", "end")
        self.right.insert("1.0", text)
        self.right.config(state="disabled")

    # ---------- actions ------------------------------------------------
    def convert(self):
        src = self.left.get("1.0", "end-1c").strip()
        if not src:
            self.status.set("Nothing to convert.")
            return
        try:
            if self.mode.get() == "si2wodrs":
                data = si_to_wodrs(src)
                preview = data.decode("latin-1")
                self._set_right(preview)
                self.right.config(font=self.wod_font)
                self.status.set(
                    f"Sinhala → wodrs: {len(src)} chars → {len(data)} bytes"
                )
            else:
                data = src.encode("latin-1", errors="replace")
                text = wodrs_to_si(data)
                self._set_right(text)
                self.right.config(font=self.si_font)
                self.status.set(
                    f"wodrs → Sinhala: {len(data)} bytes → {len(text)} chars"
                )
        except Exception as e:
            messagebox.showerror("Conversion error", str(e))
            self.status.set(f"Error: {e}")

    def swap(self):
        result = self.right.get("1.0", "end-1c")
        if not result:
            self.status.set("Nothing to swap.")
            return
        self.left.delete("1.0", "end")
        self.left.insert("1.0", result)
        self._set_right("")
        self.mode.set("wodrs2si" if self.mode.get() == "si2wodrs" else "si2wodrs")
        self._on_mode_change()
        self.status.set("Swapped.")

    def clear(self):
        self.left.delete("1.0", "end")
        self._set_right("")
        self.status.set("Cleared.")

    def copy_right(self):
        text = self.right.get("1.0", "end-1c")
        if not text:
            self.status.set("Nothing to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status.set(f"Copied {len(text)} chars to clipboard.")


def main():
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except Exception:
        pass
    WodrsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()