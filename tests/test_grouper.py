"""
    test_grouper
    ~~~~~~~~~~~~

    Tests for the :mod:`~pai_parser.grouper` module.
"""

import pytest

from pai_parser import grouper, tokenizer


@pytest.fixture(scope='module', params=[
    ('a:b', 3, 1),
    ('a:b:c', 2, 1),
    ('a:b:c:d', 3, 1),
    ('a:b:c:d:e:f', 4, 2),
    ('a:b:c:d:e:f', 5, 1)
])
def invalid_data_string_with_group_size(request):
    """
    Fixture that returns a three-element tuple of (valid data string, n, incorrect number of parsed items).
    """
    return request.param


@pytest.fixture(scope='module', params=[
    -1024,
    -512,
    -256,
    -100,
    -42,
    -13,
    -10,
    -1
])
def invalid_n(request):
    """
    Fixture that returns invalid "n" values methods that perform groupings.
    """
    return request.param


def test_group_gen_yields_nothing_on_empty_data():
    """
    Assert that :meth:`~pai_parser.grouper.group_gen` yields no items when given an empty string.
    """
    with pytest.raises(StopIteration):
        next(grouper.group_gen(''))


def test_group_gen_raises_on_non_iterator():
    """
    Assert that :meth:`~pai_parser.grouper.group_gen` raises a :class:`TypeError` when given a non-iterator.
    """
    with pytest.raises(TypeError):
        next(grouper.group_gen(None))


def test_group_gen_raises_on_negative_n(valid_data_string, invalid_n):
    """
    Assert that :meth:`~pai_parser.grouper.group_gen` raises a :class:`ValueError` when given a negative 'n' value.
    """
    with pytest.raises(ValueError):
        next(grouper.group_gen(valid_data_string, invalid_n))


def test_group_raises_on_negative_n(valid_data_string, invalid_n):
    """
    Assert that :meth:`~pai_parser.grouper.group` raises a :class:`ValueError` when given a negative 'n' value.
    """
    with pytest.raises(ValueError):
        next(grouper.group(tokenizer.tokenize(valid_data_string), invalid_n))


def test_group_gen_yields_expected_number_of_items(valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.grouper.group_gen` yields the expected number of items based on the
    provided 'n' value.
    """
    data, n, expected_len = valid_data_string_with_group_size
    assert len(list(grouper.group_gen(tokenizer.tokenize(data), n=n))) == expected_len


def test_group_returns_expected_number_of_items(valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.grouper.group` returns a list with the expected number of items
    based on the provided 'n' value.
    """
    data, n, expected_len = valid_data_string_with_group_size
    assert len(grouper.group(tokenizer.tokenize(data), n=n)) == expected_len


def test_group_gen_raises_on_non_multiple_n(invalid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.grouper.group_gen` raises a :class:`grouper.GroupSizeInconsistency` when the
    yielded number of items is not a multiple of 'n'.
    """
    data, n, _ = invalid_data_string_with_group_size
    with pytest.raises(grouper.GroupSizeInconsistency):
        list(grouper.group_gen(tokenizer.tokenize(data), n=n))


def test_group_raises_on_non_multiple_n(invalid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.grouper.group` raises a :class:`grouper.GroupSizeInconsistency` when the
    returned number of items is not a multiple of 'n'.
    """
    data, n, _ = invalid_data_string_with_group_size
    with pytest.raises(grouper.GroupSizeInconsistency):
        grouper.group(tokenizer.tokenize(data), n=n)


def test_group_returns_list():
    """
    Assert that :meth:`~pai_parser.grouper.group` returns a :class:`list` instance.
    """
    assert isinstance(grouper.group(''), list)


