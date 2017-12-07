import ox
import re
import io
import collections

def lexer(string):
    
    lexer = ox.make_lexer([
            ('ANSWER', r'ANSWER:\s*[a-zA-Z]'),
            ('OPTION', r'[a-zA-Z][.)]\s'),
            ('ANY', r'.*\n'),
    ])
        
    return lexer(string)

def parse(string):
    
    token_list = ['ANSWER', 'OPTION', 'ANY']
    
    parser_exec = ox.make_parser([
        ('question : cmd options answer', lambda x, y , z: (x.rstrip() , y ,z)),
        ('cmd : cmd ANY', lambda x,y : x+y),
        ('cmd : ANY', lambda x: x),
        ('options : options option', lambda x,y: x + [y]),
        ('options : option', lambda x: [x]),
        ('option : OPTION ANY', lambda x,y: (x.strip(),y.strip())),
        ('answer : ANSWER', lambda x: x[7:].strip()),
        ], token_list)
        
    ast = parser_exec(lexer(string))
        
    return ast

class Aiken(list):
    """
    Represents the result of parsing an Aiken string.
    """
    def __init__(self):
        self.question = ""
        self.full_options = {}
        self.options = []
        self.answer = ""

    def append(self, s):
        ord_dict = collections.OrderedDict(sorted(self.full_options.items(), key=lambda t: t[0]))
        option_letter = list(ord_dict.keys())[-1] # Gets the last alphabetic letter from options
        next_letter = ""
        if(")" in option_letter):
            next_letter = chr(ord(option_letter.rstrip(')'))+1)
            next_letter += ")" 
        else:
            next_letter = chr(ord(option_letter.rstrip('.'))+1)
            next_letter += "."
        print("Proxima letra: ", next_letter)
        self.full_options.update({next_letter: s})        

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

    ast = parse(content)
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
aiken_with_string.append("Maybe")
aiken_with_file.append("Shit")
print(dump(aiken_with_string))
print(dump(aiken_with_file))

