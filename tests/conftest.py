"""
    conftest
    ~~~~~~~~

    High level fixtures used across all test modules.
"""

import pytest


@pytest.fixture(scope='module', params=[
    ':',
    ';',
    ',',
    '.',
    '$',
    '#',
    '@'
])
def valid_delimiter(request):
    """
    Fixture that yields valid delimiter strings.
    """
    return request.param


@pytest.fixture(scope='module', params=[
    'foo',
    'bar',
    'baz',
    'foo{delimiter}bar',
    'foo{delimiter}bar{delimiter}baz'
])
def valid_data_string(request, valid_delimiter):
    """
    Fixture that yields valid data strings.
    """
    return request.param.format(delimiter=valid_delimiter)


@pytest.fixture(scope='module', params=[
    ('a', 1, 1),
    ('a:b', 1, 2),
    ('a:b', 2, 1),
    ('a:b:c', 1, 3),
    ('a:b:c', 3, 1),
    ('a:b:c:d', 1, 4),
    ('a:b:c:d', 2, 2),
    ('a:b:c:d', 4, 1),
    ('a:b:c:d:e:f', 1, 6),
    ('a:b:c:d:e:f', 2, 3),
    ('a:b:c:d:e:f', 3, 2),
    ('a:b:c:d:e:f', 6, 1)
])
def valid_data_string_with_group_size(request):
    """
    Fixture that returns a three-element tuple of (valid data string, n, expected number of parsed items).
    """
    return request.param

