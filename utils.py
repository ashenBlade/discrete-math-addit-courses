def power_mod(number, power, modulus):
    def get_bits(): return (x == '1' for x in bin(power))

    result = 1
    for b in get_bits():
        result = (result ** 2) % modulus
        if b:
            result = (result * number) % modulus

    return result
