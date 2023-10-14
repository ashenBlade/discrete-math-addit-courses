def power_mod(number, power, modulus):
    def get_bits():
        return (x == '1' for x in bin(power))

    result = 1
    for bit in get_bits():
        result = (result ** 2) % modulus
        if bit:
            result = (result * number) % modulus

    return result
