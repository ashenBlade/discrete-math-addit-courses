import pytest

from modulus_div import div_modulus


@pytest.mark.parametrize('a, b, p, expected', [
    (10, 5, 11, 6),
    (9241290472471904707, 988932747, 2 ** 127 - 1, 62654933479415419288145004284824942875),
    (1234, 381114, 4180051, 3096392),
    (4486100, 3457249, 20973859, 17739904),
])
def test_modulus(a, b, p, expected):
    actual = div_modulus(a, b, p)
    assert actual == expected, f"{a}*x % {p} == {b}. Ожидался {expected}. Рассчитан {actual}"

