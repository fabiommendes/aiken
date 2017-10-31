import pytest
import aiken


def test_project_defines_author_and_version():
    assert hasattr(aiken, '__author__')
    assert hasattr(aiken, '__version__')


def test_lexer1():
    assert aiken.lexer("sdfsdfsdfs") == [sdfsdf]
