"""
    test_tokenizer
    ~~~~~~~~~~~~~~

    Tests for the :mod:`~paip.tokenizer` module.
"""

import collections
import pytest
import shlex

from paip import tokenizer


@pytest.mark.parametrize('data', [
    int(),
    float(),
    list(),
    tuple(),
    dict(),
    set(),
    object()
])
def test_lexer_raises_on_non_str(data):
    """
    Assert that :meth:`~tokenizer._lexer` raises a :class:`~ValueError` exception when
    the `data` parameter is not a string.
    """
    with pytest.raises(ValueError):
        tokenizer._lexer(data)


@pytest.mark.parametrize('data', [
    b'foo',
    b'bar',
    b'foo:bar',
    b'foo:bar:baz'
])
def test_lexer_handles_bytes(data):
    """
    Assert that :meth:`~tokenizer._lexer` returns a :class:`~shlex.shlex` instance when given a valid byte string.
    """
    assert isinstance(tokenizer._lexer(data), shlex.shlex)


def test_lexer_returns_shlex_instance(valid_data_string):
    """
    Assert that :meth:`~tokenizer._lexer` returns a :class:`~shlex.shlex` instance when given a valid string.
    """
    assert isinstance(tokenizer._lexer(valid_data_string), shlex.shlex)


def test_lexer_sets_delimiter_whitespace_attribute(valid_delimiter):
    """
    Assert that :meth:`~tokenizer._lexer` returns a :class:`~shlex.shlex` instance with the `whitespace` attribute
    properly set to the given value.
    """
    lexer = tokenizer._lexer('', delimiter=valid_delimiter)
    assert lexer.whitespace == valid_delimiter


def test_tokenize_iter_returns_iterator():
    """
    Assert that :meth:`~tokenizer.tokenize_iter` returns an object that implements the iterator protocol.
    """
    assert isinstance(tokenizer.tokenize_iter(''), collections.Iterator)


def test_tokenize_iter_yields_nothing_on_empty_data():
    """
    Assert that :meth:`~tokenizer.tokenize_iter` returns an empty iterator when given an empty string.
    """
    with pytest.raises(StopIteration):
        next(tokenizer.tokenize_iter(''))


def test_tokenize_returns_list():
    """
    Assert that :meth:`~tokenizer.tokenize` returns a :class:`list` instance.
    """
    assert isinstance(tokenizer.tokenize(''), list)
