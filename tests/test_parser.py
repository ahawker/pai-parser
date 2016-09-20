"""
    test_parser
    ~~~~~~~~~~~

    Tests for the :mod:`~pai_parser.parser` module.
"""

import pytest

from pai_parser import parser


@pytest.fixture(scope='function')
def conforming_visitor():
    """
    Fixture that yields an object that conforms to the "visitor" interface.
    """
    class Visitor:
        def supports(self, group_size, rtl):
            raise NotImplementedError()

        def visit(self, tokens, group_size, rtl, parent=None):
            raise NotImplementedError()

    return Visitor()


@pytest.fixture(scope='module', params=[
    str(),
    int(),
    dict(),
    set(),
    list(),
    tuple(),
    object()
])
def non_conforming_visitor(request):
    """
    Fixture that yields an object that does not implement the "visitor" interface.
    """
    return request.param


@pytest.fixture(scope='function')
def non_supporting_visitor(conforming_visitor):
    """
    Fixture that yields an object that returns :bool:`False` on its :func:`support` function.
    """
    conforming_visitor.supports = lambda group_size, rtl: False
    return conforming_visitor


@pytest.fixture(scope='function')
def single_token_ordered_visitor():
    """
    Fixture that yields an object that conforms to the "visitor" interface and visits/consumes tokens and returns
    them back, one by own, in the order that they were read.
    """
    class Visitor:
        def supports(self, group_size, rtl):
            return True

        def visit(self, tokens, group_size, rtl, parent=None):
            return next(tokens, None)

    return Visitor()


def is_a_reverse_shallow_copy_list(x, y):
    """
    Return :bool:`True` if 'y' is a reversed copy of 'x' and :bool:`False` otherwise.
    """
    return x == list(reversed(y))


def test_parse_gen_raises_on_non_conforming_visitor(non_conforming_visitor):
    """
    Assert that :meth:`~pai_parser.parser.parse_gen` raises a :class:`ValueError` when given an object that does not
    conform to the visitor interface.
    """
    with pytest.raises(ValueError):
        list(parser.parse_gen('', non_conforming_visitor))


def test_parse_raises_on_non_conforming_visitor(non_conforming_visitor):
    """
    Assert that :meth:`~pai_parser.parser.parse` raises a :class:`ValueError` when given an object that does not
    conform to the visitor interface.
    """
    with pytest.raises(ValueError):
        parser.parse('', non_conforming_visitor)


def test_parse_gen_raises_on_non_supporting_visitor(non_supporting_visitor):
    """
    Assert that :meth:`~pai_parser.parser.parse_gen` raises a :class:`ValueError` when given a visitor object that
    returns :bool:`False` from its :func:`support` function.
    """
    with pytest.raises(ValueError):
        list(parser.parse_gen('', non_supporting_visitor))


def test_parse_raises_on_non_supporting_visitor(non_supporting_visitor):
    """
    Assert that :meth:`~pai_parser.parser.parse` raises a :class:`ValueError` when given a visitor object that
    returns :bool:`False` from its :func:`support` function.
    """
    with pytest.raises(ValueError):
        parser.parse('', non_supporting_visitor)


def test_parse_gen_visits_expected_number_of_nodes(single_token_ordered_visitor, valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse_gen` visits and yields the expected number of nodes based on the input
    and group size.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    nodes = list(parser.parse_gen(valid_data_string, single_token_ordered_visitor, group_size=n))
    assert len(nodes) == expected_len


def test_parse_visits_expected_number_of_nodes(single_token_ordered_visitor, valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse` visits and yields the expected number of nodes based on the input
    and group size.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    nodes = parser.parse(valid_data_string, single_token_ordered_visitor, group_size=n)
    assert len(nodes) == expected_len


def test_parse_gen_reverses_tokens_on_rtl(single_token_ordered_visitor, valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse_gen` visits and yields nodes in "reverse" order when using
    right-to-left mode.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    ltr = list(parser.parse_gen(valid_data_string, single_token_ordered_visitor, group_size=n))
    rtl = list(parser.parse_gen(valid_data_string, single_token_ordered_visitor, group_size=n, rtl=True))

    assert is_a_reverse_shallow_copy_list(ltr, rtl)


def test_parse_reverses_tokens_on_rtl(single_token_ordered_visitor, valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse` visits and yields nodes in "reverse" order when using
    right-to-left mode.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    ltr = parser.parse(valid_data_string, single_token_ordered_visitor, group_size=n)
    rtl = parser.parse(valid_data_string, single_token_ordered_visitor, group_size=n, rtl=True)

    assert is_a_reverse_shallow_copy_list(ltr, rtl)


def test_parse_gen_visits_expected_number_of_nodes_with_default_visitor(valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse_gen` visits and yields the expected number of nodes based on the input
    and group size when using the default visitor.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    nodes = list(parser.parse_gen(valid_data_string, group_size=n))
    assert len(nodes) == expected_len


def test_parse_visits_expected_number_of_nodes_with_default_visitor(valid_data_string_with_group_size):
    """
    Assert that :meth:`~pai_parser.parser.parse` visits and yields the expected number of nodes based on the input
    and group size when using the default visitor.
    """
    valid_data_string, n, expected_len = valid_data_string_with_group_size

    nodes = parser.parse(valid_data_string, group_size=n)
    assert len(nodes) == expected_len