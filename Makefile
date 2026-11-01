.PHONY: all gen check clean debt
all: gen check
	latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
	python3 tools/check_log.py main.log
gen:
	python3 tools/gen.py
# Source gates read .tex and data/, need no PDF. Run BEFORE a build.
check:
	python3 tools/gen.py --check
	python3 tools/check_book.py
debt:
	@python3 tools/debt.py
clean:
	latexmk -C
	rm -f *.ilg *.ind *.idx
