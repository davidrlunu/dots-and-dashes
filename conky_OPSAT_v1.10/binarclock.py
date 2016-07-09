#! /usr/bin/python3
import time
from itertools import zip_longest


def main():
    print(vertical_strings(bcd(time.strftime('%H%M%S'))).replace('1', '${color2}○${color}').replace('0', '○'))

def bcd(digits):
    def bcdigit(d):
        # [2:] strips the '0b' prefix added by bin().
        return bin(d)[2:].rjust(4, '0')
    return (bcdigit(int(d)) for d in digits)

def vertical_strings(strings):
    #Orient an iterable of strings vertically: one string per column.'
    iters = [iter(s) for s in strings]
    concat = ' '.join
    return '\n'.join(map(concat, zip_longest(*iters, fillvalue=' ')))


if __name__ == '__main__':
    main()

