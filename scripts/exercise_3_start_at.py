from math import floor

def f(rows: int):
    print(2**(rows.bit_length() - 1))
    print(floor(rows / 2))
    return (
        f'start at: {2**(rows.bit_length()) - floor(rows / 2):0>{rows.bit_length()}b}',
        f'start with copy seed?: {rows % 2 == 1}',
    )

print(f'rows = 5: {f(5)}')

# 2**B - 1
# 1 row
# 

# 5
#
# 0b100
# 0b011
# 0b011
# 0b010
# 0b010

# 6
#
# 0b000
# 0b111
# 0b111
# 0b110
# 0b110
# 0b101

# 7
#
# 0b000
# 0b111
# 0b111
# 0b110
# 0b110
# 0b101
# 0b101

# 8
#
# 0b1000
# 0b1111
# 0b1111
# 0b1110
# 0b1110
# 0b1101
# 0b1101
# 0b1100

# 9
#
# 0b1000
# 0b1111
# 0b1111
# 0b1110
# 0b1110
# 0b1101
# 0b1101
# 0b1100
# 0b1100
