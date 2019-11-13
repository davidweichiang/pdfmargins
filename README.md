# pdfmargins

```
usage: pdfmargins.py [-h] [-m DIM] [-t DIM] [-r DIM] [-b DIM] [-l DIM] infile

Check margins of a PDF file.

positional arguments:
  infile                input PDF file

optional arguments:
  -h, --help            show this help message and exit
  -m DIM, --margin DIM  minimum margin on all sides
  -t DIM, --top DIM     minimum top margin
  -r DIM, --right DIM   minimum right margin
  -b DIM, --bottom DIM  minimum bottom margin
  -l DIM, --left DIM    minimum left margin
```

where `DIM` can be expressed in inches (e.g., `1in`) or centimeters
(e.g., `2.5cm`).

If a page contains any printing in the margin, an error will be
displayed saying which page and which margin, and the program will
exit with status 1. Otherwise, nothing is printed, and the program
will exit with status 0.
