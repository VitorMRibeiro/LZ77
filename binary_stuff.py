""" A bunch of auxiliary functions that have to do with binaries """

def radix(number, size, digits=['0', '1']):
    """ converts 'number' to it's representation in base 'base'. """
    s = ''
    base = len(digits)
    for _ in range(size):
        number, reminder = divmod(number, base)
        reminder = digits[reminder]
        s = reminder + s
        
    return s

def byt_to_str(byt_arr):
    """ converts a bytearray into a string of '1's and '0's """
    s = ''
    for i in byt_arr:
        s += radix(int(i), 8)
        #print(radix(int(i), 8))
    return s

def str_to_byt(s):
    """ converts a string of '1's and '0's into a bytearray """
    byt = bytearray()
    for i in range(0, len(s), 8):
        dif = 8 - len(s[i:i+8])
        number = 2**dif * int(s[i:i+8], 2)
        byt.append(number)
    return byt



