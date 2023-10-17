from utils import power_mod


def _get_generators(p):
    r = (p - 1) // 2

    for n in range(2, p - 1):
        if n ** 2 % p != 1 and power_mod(n, r, p) != 1:
            yield n


def get_generator(p):
    return next(_get_generators(p))

