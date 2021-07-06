doc:
	@# compile main.tex with bibliography support
	make latex && make bib && make latex

latex:
	@# run latex on main.tex
	pdflatex main.tex

bib:
	@# compile bibliography
	bibtex main

clean:
	@# clean latex and bibtex auxiliary files
	@rm -f main.bbl main.aux main.nav main.out main.dvi main.snm main.toc main.blg
	@rm -f main.log main.fdb_latexmk main.fls main.dep main.synctex.gz main.vimtex.pdf

publisher:
	@# Create tar.gz to send to publisher
	sh package.sh publisher

arxiv:
	@# Create tar.gz for arxiv submission
	sh package.sh arxiv

all:
	@# Re-compile figures, tables, statistics, and the document
	python scripts/compute_stats.py
	python scripts/create_figures.py --all
	python scripts/create_tables.py --all
	make latex && make bib && make latex
