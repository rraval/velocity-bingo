#!/bin/sh

for i in `seq 1 5`; do
    python3 bingo.py > sample$i.tex && lualatex sample$i.tex
    rm sample$i.tex
done
rm -f *.aux *.log
