import random

from utils import power_mod


def _get_s_q(number):
    """
    Получить такие s и q, что
    number - 1 = (2 ^ s) * q
    """
    original = number
    number -= 1
    s = 0

    while True:
        if not (number & 0b1):
            s += 1
        else:
            break
        number //= 2

    return s, original // (1 << s)


def is_prime(number, rounds=1):
    """
    Проверить, что число number простое, используя алгоритм Робина-Миллера
    """
    if number == 1:
        return True

    if number % 2 == 0:
        # Число четное или 0
        return False

    s, d = _get_s_q(number)

    for _ in range(rounds):
        y = None
        a = random.randint(2, number - 1)
        x = power_mod(a, d, number)
        for _ in range(s):
            y = power_mod(x, 2, number)
            if y == 1 and x != 1 and x != (number - 1):
                return False
            x = y
        if y != 1:
            return False
    return True

