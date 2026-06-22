PDF=prime_resolvent_research_programme.pdf

all: $(PDF)

$(PDF): main.tex
	pdflatex -interaction=nonstopmode -halt-on-error -jobname=prime_resolvent_research_programme main.tex
	pdflatex -interaction=nonstopmode -halt-on-error -jobname=prime_resolvent_research_programme main.tex

clean:
	rm -f *.aux *.log *.out *.toc *.pdf
