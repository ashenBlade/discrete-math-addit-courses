import pytest

from modulus_div import div_modulus_euclid, div_modulus_fermat
from utils import power_mod


@pytest.mark.parametrize('a, b, p, expected', [
    (10, 5, 11, 6),
    (9241290472471904707, 988932747, 2 ** 127 - 1, 62654933479415419288145004284824942875),
    (1234, 381114, 4180051, 3096392),
    (4486100, 3457249, 20973859, 17739904),
])
def test_modulus_euclid(a, b, p, expected):
    actual = div_modulus_euclid(a, b, p)
    assert actual == expected, f"{a}*x % {p} == {b}. Ожидался {expected}. Рассчитан {actual}"


@pytest.mark.parametrize('a, b, p, expected', [
    (10, 5, 11, 6),
    (9241290472471904707, 988932747, 2 ** 127 - 1, 62654933479415419288145004284824942875),
    (1234, 381114, 4180051, 3096392),
    (4486100, 3457249, 20973859, 17739904),
])
def test_modulus_fermat(a, b, p, expected):
    actual = div_modulus_fermat(a, b, p)
    assert actual == expected, f"{a}*x % {p} == {b}. Ожидался {expected}. Рассчитан {actual}"


@pytest.mark.parametrize('n, p, m, expected', [
    (2, 3, 5, 3),
    (123, 4567, 2456, 771),
    (34572, 123541, 834576577234, 649547561828),
    (345722388, 1235410, 834576577234, 483453516248),
])
def test_power_mod(n, p, m, expected):
    actual = power_mod(n, p, m)
    assert actual == expected, f"{n} ** {p} % {m}. Ожидался {expected}. Получен: {actual}"
