#!/usr/bin/env python3
"""Print the outstanding-work ledgers from generated/values.tex. Never fatal."""
import re
from pathlib import Path
v = dict(re.findall(r"gval@([A-Za-z0-9.]+)\}\{(\d+)\}", (Path(__file__).resolve().parent.parent / "generated/values.tex").read_text()))
g = lambda k: int(v.get(k, 0))
print(f"chapters written: {g('written.total')} of {g('chapters.total')}")
print(f"exercise items: {g('exercises.total')}  tasks: {g('tasks.total')}  traps: {g('traps.total')}")
print(f"facts flagged \\verify{{}} (need a primary source or a specialist): {g('verify.total')}")
print("Recenzja lekarza medycyny snu: NIEUSTALONA  (reported on every build; see CLAUDE.md)")
