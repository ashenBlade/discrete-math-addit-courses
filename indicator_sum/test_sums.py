import pytest

from indicator_sum.sums import sum_ceil, sum_ceil_non_bound


@pytest.mark.parametrize('n, expected', [
    (2, 7),
    (3, 22),
    (4, 50)
])
def test_sum_ceil(n, expected):
    actual = sum_ceil(n)
    assert actual == expected


@pytest.mark.parametrize('n, expected', [
    (12, 34),
    (21, 75),
    (16, 50),
])
def test_sum_ceil_non_bound(n, expected):
    actual = sum_ceil_non_bound(n)
    assert actual == expected

