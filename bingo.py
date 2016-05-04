import random
from writer import Safe, runWriter, latex_escape

def writeMain(phrases, pages):
    yield Safe(r'''
        \documentclass[11pt]{article}
        \usepackage[margin=0.25in,landscape]{geometry}
        \usepackage{fontspec}
        \usepackage{polyglossia}

        \usepackage{array}

        \defaultfontfeatures{Scale=MatchUppercase,Ligatures=TeX}
        \setmainfont{TeX Gyre Heros}

        \newlength{\bMargin}
        \newlength{\bWidth}
        \newlength{\bHeight}
        \newlength{\bCellWidth}
        \newlength{\bCellHeight}

        \setlength{\parindent}{0pt}
        \setlength{\parskip}{0pt}
        \setlength{\tabcolsep}{0pt}
        \setlength{\arrayrulewidth}{1pt}

        \pagestyle{empty}

        \newcolumntype{?}{!{\vrule width \bBorder}}
        \newcolumntype{P}{%
            @{\parbox[c][\bCellHeight]{0pt}{}}
            >{\centering\arraybackslash}
            m{\dimexpr\bCellWidth}
        }

        \begin{document}
        \setlength{\bMargin}{0.25in}
        \setlength{\bWidth}{0.5\dimexpr\textwidth-\bMargin}
        \setlength{\bHeight}{0.5\dimexpr\textheight-\bMargin}
        \setlength{\bCellWidth}{0.2\dimexpr\bWidth-6\arrayrulewidth}
        \setlength{\bCellHeight}{0.2\dimexpr\bHeight-6\arrayrulewidth}
    ''')

    for i in range(pages * 4):
        yield from writeTable(phrases)
        yield Safe(r'\allowbreak\hfill{}')

        if (i % 2) == 1:
            yield Safe(r'\par\vspace{\bMargin}')

    yield Safe(r'\end{document}')

def writeTable(phrases):
    sample = random.sample(phrases, 24)
    sample = sample[:12] + ['"Um" or awkward pause'] + sample[12:]

    yield Safe(r'\begin{tabular}{|P|P|P|P|P|}')
    yield Safe(r'\hline{}')

    for i, w in enumerate(sample):
        yield Safe(r'\parbox{\dimexpr\bCellWidth-6pt\relax}{\centering{}')
        yield w
        yield Safe(r'}')

        if (i % 5) == 4:
            yield Safe(r'\\')
            yield Safe(r'\hline ')
        else:
            yield Safe(r'&')

    yield Safe(r'\end{tabular}')

if __name__ == '__main__':
    import sys

    with open('phrases.txt') as fp:
        phrases = [l.strip() for l in fp.readlines()]

    runWriter(sys.stdout, writeMain(phrases, pages=20), latex_escape)
