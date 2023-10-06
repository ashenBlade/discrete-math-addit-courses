import pytest

from miller_rabin_test import is_prime

known_primes = [
    17015003,
    17019637,
    12796991,
    12858229,
    9767,
    618970019642690137449562111,
    170141183460469231731687303715884105727,
    19175002942688032928599,
    900900900900990990990991,
]

not_primes = [
    977 * 2,
    4691 * 3733 * 145342,
    8779 * 27541 * 40591 * 29303
]


@pytest.mark.parametrize('number', known_primes)
def test_prime(number):
    prime = is_prime(number)
    assert prime


@pytest.mark.parametrize('number', not_primes)
def test_not_prime(number):
    prime = is_prime(number)
    assert not prime

