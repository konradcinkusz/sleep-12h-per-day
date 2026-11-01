# CLAUDE.md — working on this book

Context for continuing *Dwanaście godzin snu*. Conventions inherited from `german-from-zero-to-hero` (same tooling shape) and the `architecture-standards` research-documentation skill.

## Status
Read numbers from the ledgers, never from this file: `python3 tools/debt.py`.
Review status: **Recenzja lekarza medycyny snu: NIEUSTALONA.** Reported on every build; do not let it quietly go away.

## Conventions
1. `data/chapters.tsv` is the sequence; `data/*.tsv` are the tables. `generated/` is written by `tools/gen.py`, committed, drift-gated (`gen.py --check`). Never hand-edit it.
2. Every number a table prints is computed (`\val{key}`, `\generated{name}`). Keys are ASCII. Arithmetic taught inline is fine.
3. A claim about the world not verified against a primary source is wrapped in `\verify{}`. Never invent studies, authors or citations.
4. Chapter anatomy (gate): `\chapteropen{NN}`, `cele` (>=3), >=4 sections, >=1100 words, `przyklad`, `falle`, `cwiczenia` with >=6 `\exitem{q}{answer}`, `\zadanie{}`.
5. Run source gates before the build: `python3 tools/gen.py --check && python3 tools/check_book.py`.
6. No placeholders ship. An unchanged page count after an edit is a build that did not run.
7. CI runs on GitHub-hosted runners (public repository).
