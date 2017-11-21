import ox
import re
import io

class Aiken:
    """
    Represents the result of parsing an Aiken string.
    """
    def __init__(self):
        self.question = ""
        self.full_options = {}
        self.options = []
        self.answer = ""
        self._token_list = []

    def lexer(self, string):
        lexer = ox.make_lexer([
                ('ANSWER', r'ANSWER:\s*[a-zA-Z]'),
                ('OPTION', r'[a-zA-Z][.)]\s'),
                ('ANY', r'.*\n'),
        ])
        
        return lexer(string)

    def parse(self, string):

        self._token_list = ['ANSWER', 'OPTION', 'ANY']
        
        parser = ox.make_parser([
            ('question : cmd options answer', lambda x, y , z: (x.rstrip() , y ,z)),
            ('cmd : cmd ANY', lambda x,y : x+y),
            ('cmd : ANY', lambda x: x),
            ('options : options option', lambda x,y: x + [y]),
            ('options : option', lambda x: [x]),
            ('option : OPTION ANY', lambda x,y: (x.strip('. '),y.strip())),
            ('answer : ANSWER', lambda x: x[7:].strip()),
        ], self._token_list)
        
        ast = parser(self.lexer(string))
        
        return ast

    def append(self, s):
        self.options.append(s)

    def __str__(self):
        string = ''

        string += self.question + '\n'
        for option in self.options:
            string += option.key + '.' + option.value + '\n'

        string += 'ANSWER: ' + self.answer
        return string

def load(file_or_string):
    """
    Load a file or string in the Aiken format and return a parsed object.

    Args:
        file_or_string:
            A file object containing the Aiken source or a string.

    Returns:
        An :cls:`Aiken` instance.
    """
    aiken = Aiken()
    try:
        file_obj = open(file_or_string)
        content = file_obj.read()
        file_obj.close()
    except:
        content = file_or_string
    ast = aiken.parse(content)
    for options in ast[1]:
        for i in range(len(options)):
            if ((i+1) < len(options)):
                aiken.full_options[options[i]] = options[i+1]
        
    aiken.options = list(aiken.full_options.values())
    aiken.answer = ast[2]
    aiken.question = ast[0]
    return aiken


def dump(aiken, file=None):
    """
    Writes aiken object in the given file. If no file is given, return a string
    with the file contents.
    """
    aiken_content = ""

    aiken_content += aiken.question + "\n"
    aiken_dict = aiken.full_options
    for k, v in sorted(aiken_dict.items()):
        aiken_content += k + " " + v + "\n"
    
    aiken_content += "ANSWER: " +aiken.answer

    if file is not None:
        file = open(file, "w")
        file.write(aiken_content)
        file.close() 
        return ""
    else:
        return aiken_content

    return aiken_content

aiken_with_string = load("""Is this a valid Aiken Question?
A. Yes
B. No
ANSWER: A""")
aiken_with_file = load("aiken_example.txt")

dump(aiken_with_string, "dump_with_string.txt")
dump(aiken_with_file, "dump_with_file.txt")

aiken_without_file = dump(aiken_with_file)
print("Aiken Without file: \n" +aiken_without_file)