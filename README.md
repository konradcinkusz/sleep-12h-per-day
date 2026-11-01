# Dwanaście godzin snu

Jak ułożyć dobę tak, żeby spać 12 godzin i mieć czas na pieczenie chleba: budżet czasu, rytm snu, dom w minimum i chleb na zimnej fermentacji. Uczciwie: 12 h to więcej niż typowe zalecenia, a książka nie jest poradą medyczną.

* 10 rozdziałów w trzech częściach: cele, przykład, pułapka, ćwiczenia z kluczem, zadanie na tydzień.
* Liczby w tablicach i recepturach są **liczone z danych** (`data/`, `tools/gen.py`), nie wpisywane.
* Twierdzenia o świecie, których autor nie sprawdził w źródle, oznaczone są pomarańczowym **[?]** (`\verify{}`); ich liczba jest drukowana w rejestrze (ostatni dodatek).

## Budowanie

```bash
python3 tools/gen.py && python3 tools/check_book.py   # bramki źródłowe (sekundy)
latexmk -pdf main.tex                                 # PDF
python3 tools/check_log.py main.log                   # log: błędy, odwołania, overfull
```

## Status

**Wersja robocza.** Recenzja lekarza medycyny snu: NIEUSTALONA. Treść: CC BY-NC-SA 4.0 (`LICENSE-CONTENT`), kod: MIT (`LICENSE`).
