class Aiken:
    """
    Represents the result of parsing an Aiken string.
    """


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