import random
from writer import Safe, runWriter, latex_escape

def writeMain(master, pages):
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
        yield from writeTable(master)
        yield Safe(r'\allowbreak\hfill{}')

        if (i % 2) == 1:
            yield Safe(r'\par\vspace{\bMargin}')

    yield Safe(r'\end{document}')

def writeTable(master):
    words = random.sample(master, 24)
    words = words[:12] + ['"Um" or awkward pause'] + words[12:]

    yield Safe(r'\begin{tabular}{|P|P|P|P|P|}')
    yield Safe(r'\hline{}')

    for i, w in enumerate(words):
        yield Safe(r'\parbox{\dimexpr\bCellWidth-6pt\relax}{\centering{}')
        yield w
        yield Safe(r'}')

        if (i % 5) == 4:
            yield Safe(r'\\')
            yield Safe(r'\hline ')
        else:
            yield Safe(r'&')

    yield Safe(r'\end{tabular}')

WORDS = '''
Machine Learning... Somehow
Our Primary Market: students
Social for...
Uber for...
Tinder for…
AirBnB for...
We'll Sell Analytics!
Hyper Local
"Disrupt"
"1% of X billion market..."
"Revolutionize"
"Hacker"
"Hustler"
"Rock star"
"Drones"
"Autonomous"
Chatbot
Food
Carsharing
Transit App
Solve Teaching / Education
VR
Commercial Home Services
Wearables
Smart clothing
Search engine
Grocery
NFC / QR / RFID
Crowd Sourcing
Meal Tracking
Gamification
Internet of Things
Music
Dating
Two Sided Market
Note Taking / To-Do
"Freemium"
"Curated"
"Eco-system"
Life Tracking
Fashion / Clothing Apps
Ship Things from China!
Ant Farm
Parking
Email
Project Management
Accounting / Taxes
"Software as a service" / "SaaS"
Environmental / Green
Global Energy
Sales CRM
Photo Sharing App
Agriculture
Weed
Book a Meeting
Tools for Startups
Brainstorming
'''.strip().split('\n')

if __name__ == '__main__':
    import sys
    runWriter(sys.stdout, writeMain(WORDS, 20), latex_escape)
