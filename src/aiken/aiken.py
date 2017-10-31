import ox


def make_lexer(rules):
    regex = '|'.join(r'(?P<%s>%s)' % item for item in rules)
    regex = re.compile(regex)

    def lexer(expr):
        for match in re.finditer(regex, expr):
            typ = match.lastgroup
            value = match.group(typ)
            yield Token(typ, value)

    return lexer


class Aiken:
    """
    Represents the result of parsing an Aiken string.
    """
    def __init__(self, string):
        self.question = ""
        self.options = {}
        self.answer = ""
        self.parse(string)

    def parse(self, string):
        lexer = make_lexer([
                ('ANSWER', r'\nANSWER:\s*[a-zA-Z]'),
                ('OPTION', r'\n[a-zA-Z][.)]\s'),
                ('ANY', r'.+\n'),
            ])


        print(str(lexer(string)))
        print(type(lexer))

    def append(self, s):
        self.options.append(s)

    def __str__(self):
        print(self.question)
        for option in self.options:
            print(option.key + '.' + option.value)

        print("ANSWER: " + self.answer)



def load(file_or_string):
    """
    Load a file or string in the Aiken format and return a parsed object.

    Args:
        file_or_string:
            A file object containing the Aiken source or a string.

    Returns:
        An :cls:`Aiken` instance.
    """

    raise NotImplementedError


def dump(aiken, file=None):
    """
    Writes aiken object in the given file. If no file is given, return a string
    with the file contents.
    """

    raise NotImplementedError

question = Aiken("""Is this a valid Aiken Question?
A. Yes
B. No
ANSWER: A""")
