.PHONY: all

all:
	@test ! -f build/robotoken-refs.bib || rm build/robotoken-refs.bib
	@test ! -f build/arxiv.sty || rm build/arxiv.sty
	latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build robotoken.tex
	cp build/robotoken.pdf robotoken.pdf
	mkdir -p ../website/public/files
	cp robotoken.pdf ../website/public/files/
