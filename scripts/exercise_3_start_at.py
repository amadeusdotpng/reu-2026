from math import ceil

def f(rows: int):
    return (
        f'start at: {2**(rows.bit_length()-1) - ceil(rows / 2):0>{rows.bit_length()-1}b}',
        f'start with copy seed?: {rows % 2 == 1}',
    )

print(f'rows = 97: {f(97)}')
