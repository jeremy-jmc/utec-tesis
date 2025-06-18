build:
	pdflatex main.tex && bibtex main.aux && pdflatex main.tex

open:
	xdg-open main.pdf

recreate:
	$(MAKE) build && $(MAKE) build && $(MAKE) open