#!/usr/bin/env python3
"""Source gates for the book. Reads .tex and data/, needs no PDF.

  1. data/chapters.tsv and chapters/ agree; each chapter opens with its own number.
  2. each chapter carries the required teaching elements and a minimum length.
  3. every exercise item has a non-empty answer.
  4. every \val{key} resolves in generated/values.tex.
  5. environments and braces balance in every source file.
  6. no TODO / FIXME / placeholder text ships.
Run BEFORE building. Stdlib only.  --partial skips unwritten chapters (authoring aid; CI never passes it).
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTIAL = "--partial" in sys.argv
MIN_WORDS, MIN_EX = 1100, 6
errs = []
err = errs.append

def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)

def balanced_args(s, start):
    depth, i = 0, start
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 2; continue
        if c == "{": depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0: return s[start + 1:i], i + 1
        i += 1
    return None, len(s)

def words(s):
    s = re.sub(r"\\[A-Za-z]+\*?", " ", s)
    s = re.sub(r"[{}\\$&%#_^~]", " ", s)
    return len(re.findall(r"[^\W\d_]{2,}", s))

rows = [ln.split("\t") for ln in (ROOT / "data/chapters.tsv").read_text(encoding="utf-8").splitlines()[1:] if ln.strip()]
expected = {f"c{int(r[0]):02d}-{r[3]}.tex": int(r[0]) for r in rows}
present = {p.name for p in (ROOT / "chapters").glob("c*.tex")}
for name in sorted(expected.keys() - present):
    if not PARTIAL: err(f"chapters/{name} is listed in data/chapters.tsv but does not exist")
for name in sorted(present - expected.keys()):
    err(f"chapters/{name} exists but is not listed in data/chapters.tsv")

REQUIRED = [
    (r"\\begin\{cele\}", "a \\begin{cele} block (goals)"),
    (r"\\begin\{cwiczenia\}", "an exercise block"),
    (r"\\zadanie\{", "a \\zadanie{...} production task"),
    (r"\\begin\{falle\}", "a trap box (falle)"),
    (r"\\begin\{przyklad\}", "a worked example (przyklad)"),
]
vp = ROOT / "generated/values.tex"
keys = set(re.findall(r"gval@([A-Za-z0-9.]+)\}", vp.read_text(encoding="utf-8"))) if vp.exists() else set()

sources = sorted(ROOT.glob("chapters/*.tex")) + sorted(ROOT.glob("frontmatter/*.tex")) + \
    sorted(ROOT.glob("appendices/*.tex")) + [ROOT / "main.tex", ROOT / "preamble.tex"]
for p in sources:
    rel = p.relative_to(ROOT)
    raw = p.read_text(encoding="utf-8")
    s = strip_comments(raw)
    begins = re.findall(r"\\begin\{([A-Za-z*]+)\}", s)
    ends = re.findall(r"\\end\{([A-Za-z*]+)\}", s)
    for env in set(begins) | set(ends):
        if begins.count(env) != ends.count(env):
            err(f"{rel}: \\begin{{{env}}} x{begins.count(env)} vs \\end x{ends.count(env)}")
    depth, i = 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\": i += 2; continue
        depth += (c == "{") - (c == "}")
        if depth < 0: err(f"{rel}: unmatched closing brace"); break
        i += 1
    if depth > 0: err(f"{rel}: {depth} unclosed brace(s)")
    for m in re.finditer(r"\b(TODO|FIXME|XXX|TBD|lorem ipsum)\b", raw, re.I):
        err(f"{rel}: placeholder text {m.group(0)!r}")
    for k in re.findall(r"\\val\{([^}]+)\}", s):
        if k not in keys: err(f"{rel}: \\val{{{k}}} has no definition in generated/values.tex")
    if p.parent.name == "chapters" and p.name in expected:
        nn = f"{expected[p.name]:02d}"
        opens = re.findall(r"\\chapteropen\{(\d\d)\}", s)
        if opens != [nn]: err(f"{rel}: must contain exactly one \\chapteropen{{{nn}}}, found {opens}")
        for pat, what in REQUIRED:
            if not re.search(pat, s): err(f"{rel}: missing {what}")
        n_ex = 0
        for m in re.finditer(r"\\exitem\{", s):
            q, end = balanced_args(s, m.end() - 1)
            if q is None or not q.strip(): err(f"{rel}: \\exitem with an empty or unbalanced question"); continue
            if end >= len(s) or s[end] != "{": err(f"{rel}: \\exitem lacks an answer near {q[:40]!r}"); continue
            a, _ = balanced_args(s, end)
            if a is None or not a.strip(): err(f"{rel}: \\exitem with an empty answer near {q[:40]!r}")
            n_ex += 1
        if n_ex < MIN_EX: err(f"{rel}: only {n_ex} exercise items (minimum {MIN_EX})")
        if len(re.findall(r"\\section\{", s)) < 4: err(f"{rel}: fewer than 4 sections")
        cele = "".join(re.findall(r"\\begin\{cele\}.*?\\end\{cele\}", s, re.S))
        if len(re.findall(r"\\item", cele)) < 3: err(f"{rel}: fewer than 3 goals")
        w = words(s)
        if w < MIN_WORDS: err(f"{rel}: only {w} words (minimum {MIN_WORDS})")
if errs:
    print("\n".join("FAIL " + e for e in errs)); print(f"\n{len(errs)} problem(s)"); sys.exit(1)
print(f"check_book: {len(rows)} chapters, {len(sources)} sources, all gates green")
