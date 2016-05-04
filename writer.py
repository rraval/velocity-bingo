import unicodedata

class Safe(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def runWriter(out, gen, escape):
    for val in gen:
        strval = str(val)
        if not isinstance(val, Safe):
            strval = escape(strval)
        out.write(strval)

def latex_escape_char(c, skip=set()):
    from_dict = ESCAPE_CHARS.get(c)
    if from_dict is not None and c not in skip:
        return from_dict

    # skip any control characters because they cause xelatex to fail
    return '' if unicodedata.category(c)[0] == 'C' else c

def latex_escape(s, skip=set()):
    if s is None:
        return None

    if isinstance(s, bytes):
        # tornado is dumb and utf8 encodes the value /before/ calling the
        # escape function.
        s = s.decode('utf-8')
    else:
        s = str(s)

    return ''.join(latex_escape_char(c, skip) for c in s if unicodedata.category(c)[0] != 'C')

# latex escaping
ESCAPE_CHARS = {
    '&':  r'\&',
    '%':  r'\%',
    '$':  r'\$',
    '#':  r'\#',
    '_':  r'\_',
    '{':  r'\{',
    '}':  r'\}',
    '~':  r'\textasciitilde{}',
    '^':  r'\textasciicircum{}',
    '\\': r'\textbackslash{}',

    # apparently luatex uses unicode replacement char as an encoding failure
    # and dies: http://ntg-context.ntg.narkive.com/WqPRk0d5/unicode-question
    '�': ' ',

    # escape newlines because paragraph breaks in weird places (like \section)
    # can wreak havoc
    '\n': r' ',

    # diacritics
    'é': r'\'e',
    'è': r'\`e',
    'à': r'\`a',
    'ù': r'\`u',
    'â': r'\^a',
    'ê': r'\^e',
    'î': r'\^i',
    'ô': r'\^o',
    'û': r'\^u',
    'ë': r'\"e',
    'ï': r'\"i',
    'ü': r'\"u',
    'ÿ': r'\"y',
    'ç': r"\c c",

    'É': r'\'E',
    'È': r'\`E',
    'À': r'\`A',
    'Ù': r'\`U',
    'Â': r'\^A',
    'Ê': r'\^E',
    'Î': r'\^I',
    'Ô': r'\^O',
    'Û': r'\^U',
    'Ë': r'\"E',
    'Ï': r'\"I',
    'Ü': r'\"U',
    'Ÿ': r'\"Y',
    'Ç': r"\c C",

    # unicode escapes
    '“': r'``',
    '”': r"''",
    '‘': r"`",
    '’': r"'",
    '®': r'\textsuperscript{\textregistered}',
}
