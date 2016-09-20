"""
    test_slicer
    ~~~~~~~~~~~

    Tests for the :mod:`~pai_parser.slicer` module.
"""

import pytest

from pai_parser import slicer


@pytest.fixture(scope='function', params=[
    [1, 2],
    [1, 2, 3],
    [1, 2, 3, 4],
    list(range(0, 10))
])
def sequence(request):
    """
    Fixture that yields sequence objects that support iteration.
    """
    return request.param


@pytest.fixture(scope='function')
def iterable_with_correct_size(sequence):
    """
    Fixture that yields a two item tuple (iterable, a number less than or equal to the number of items in the iterable).
    """
    return iter(sequence), len(sequence) - 1


@pytest.fixture(scope='function')
def iterable_with_incorrect_size(sequence):
    """
    Fixture that yields a two item tuple (iterable, a number greater than the number of items in the iterable).
    """
    return iter(sequence), len(sequence) + 1


def test_iter_slice_raises_on_empty_iterable():
    """
    Assert that :func:`~pai_parser.slicer.iter_slice` raises a :class:`~pai_parser.slicer.SliceIterableEmpty` exception
    when the given iterable has no items.
    """
    with pytest.raises(slicer.SliceIterableEmpty):
        slicer.iter_slice(iter([]), 1)


def test_iter_slice_raises_on_exhausted_iterable(iterable_with_incorrect_size):
    """
    Assert that :func:`~pai_parser.slicer.iter_slice` raises a :class:`~pai_parser.slicer.SliceIterableExhausted`
    exception when the given iterable yields less than 'n' requested items.
    """
    with pytest.raises(slicer.SliceIterableExhausted):
        slicer.iter_slice(*iterable_with_incorrect_size)


def test_iter_returns_correctly_sized_slice(iterable_with_correct_size):
    """
    Assert that :func:`~pai_parser.slicer.iter_slice` returns 'n' number of items.
    """
    iterable, n = iterable_with_correct_size

    items = slicer.iter_slice(iterable, n)
    assert len(items) == n


def test_iter_returns_slice_with_given_class(iterable_with_correct_size):
    """
    Assert that :func:`~pai_parser.slicer.iter_slice` returns the slice based on the 'slice_cls' parameter.
    """
    list_items = slicer.iter_slice(*iterable_with_correct_size, slice_cls=list)
    assert isinstance(list_items, list)
