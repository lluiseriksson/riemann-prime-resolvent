# Paper build

The PDF is built from `main.tex` with `latexmk`, BibTeX, and standard TeX Live packages.

```bash
./scripts/build_paper.sh
```

The script regenerates the numerical and exact-certificate inputs when absent, copies the PDF figures into `paper/figures`, and writes:

```text
paper/one_point_resolvent_hausdorff.pdf
```

The manuscript is licensed under CC BY 4.0; code is Apache-2.0.
