def calculate_gcd_extended(a, b):
    """
    Рассчитать НОД по расширенному алгоритму, возвращая кортеж: НОД(a, b), x, y
    Причем
    a*x + b*y = НОД(a, b)
    """
    if a == 0:
        return b, 0, 1
    g, prev_x, prev_y = calculate_gcd_extended(b % a, a)
    x = prev_y - (b // a) * prev_x
    y = prev_x
    return g, x, y


def power_mod(number, power, modulus):
    def get_bits(): return (x == '1' for x in bin(power))

    result = 1
    for b in get_bits():
        result = (result ** 2) % modulus
        if b:
            result = (result * number) % modulus

    return result


def get_input():
    """
    Получить ввод для задачи в виде кортежа: a, b, p
    """
    def input_inner(arg):
        while True:
            try:
                return int(input(f'Введите {arg}: '))
            except ValueError:
                continue

    return input_inner('p'), input_inner('a'), input_inner('b')


def div_modulus_euclid(a, b, p):
    """
    Рассчитать такое x, что
    a*x % p = b
    """
    # check_simple(p)
    gcd, x, y = calculate_gcd_extended(a, p)
    assert gcd == 1, f"НОД({a}, {p}) == {gcd}"
    return (x * b) % p


def div_modulus_fermat(a, b, p):
    """
    Рассчитать такое x, что
    a*x % p = b
    через малую теорему Ферма
    """
    a_powered = power_mod(a, p - 2, p)
    return (a_powered * b) % p


def main():
    a, b, p = get_input()
    answer = div_modulus_euclid(a, b, p)
    print(f'Результат: {answer}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
