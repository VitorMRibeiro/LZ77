""" lz77's encode and decode methods """

import binary_stuff as b
import math

# buffer size
n = 8192 + 256
# word length
L_s = 256

alphabet = ['0', '1']
# alphabet size
alpha = len(alphabet)

# globals
Buffer = ''
input_size = 0

def dump_buffer(Buffer):
    """ print the contents of buffer colored in way that helps visualization """
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

    print(OKGREEN + Buffer[:n-L_s-1] + ENDC, end='')
    print(Buffer[n - L_s - 1], end='')
    print(OKBLUE + Buffer[n-L_s:n] + ENDC)

def compute_prefix_function(offset):
    prefix_array = [0]
    k = 0
    range_q = min(L_s, len(Buffer) - offset - (n-L_s))
    for q in range(1, range_q):
        while k > 0 and Buffer[offset+n-L_s+k] != Buffer[offset+n-L_s+q]:
            k = prefix_array[k-1]
        if Buffer[offset+n-L_s+k] == Buffer[offset+n-L_s+q]:
            k = k + 1
        prefix_array.append(k)
    return prefix_array

def KMP(offset):
    """ this is an adapted versio of Knuth-Moris-Pratt to find the best match to a pattern """
    larger_match = 0
    larger_index = 0
    index = 0
    q = 0
    prefix_function = compute_prefix_function(offset)
    range_s = min(n, len(Buffer) - offset)
    range_q = min(L_s, len(Buffer) - offset - (n-L_s))
    for s in range(range_s):
        while q > 0 and Buffer[offset+n-L_s+q] != Buffer[offset+s]:
            q = prefix_function[q-1]
            index = s - q
        if index >= n-L_s-1: # this doesn't come from KMP, it's a problem specific condition
            break
        if q >= range_q - 1:
            break

        if Buffer[offset+n-L_s+q] == Buffer[offset+s]:
            if q == 0:
                index = s
            if index >= n-L_s-1: # this doesn't come from KMP, it's a problem specific condition
                break
            q += 1
            if q > larger_match:
                larger_match = q
                larger_index = index
            if q >= range_q - 1:
                break

        if q == L_s:
            # there's no reason to continue since no better match will be found
            larger_index = index
            break

    return larger_index, larger_match

def encode(S):
    """ encode a strig using lz77 compression algorithm """
    global Buffer
    global input_size

    print(f'buffer size: {n}')
    print(f'word size: {L_s}')
    print(f'codeword size: {math.ceil(math.log(n - L_s, alpha)) + math.ceil(math.log(L_s, alpha)) + 1} bits')

    Z = ''
    for _ in range(n - L_s):
        Z += alphabet[0]
    Buffer = Z + S

    rep_ext = []
    Code = ''

    input_size = len(S)
    i = L_s
    while i < input_size + L_s:
        offset = i - L_s
        pointer, j = KMP(offset) # use KMP string matching alogorithm to find reproduceble exetentions
        rep_ext.append(Buffer[offset+n-L_s:offset+n-L_s+j+1])
        l = len(rep_ext[-1])
        C_1 = b.radix(pointer, math.ceil(math.log(n - L_s, alpha)), alphabet)
        C_2 = b.radix(l-1, math.ceil(math.log(L_s, alpha)), alphabet)
        C_3 = rep_ext[-1][-1]

        Code += C_1 + C_2 + C_3
        i += l
    return Code

def decode(Code):
    #print(Code)
    # Decoding
    Z = ''

    for _ in range(n - L_s):
        Z += alphabet[0]

    buffer = Z

    reconstructed_string = ''
    while Code != '':
        #dump_buffer(buffer)
        i1 = math.ceil(math.log(n - L_s, alpha))
        i2 = i1+math.ceil(math.log(L_s, alpha))

        try:
            pointer = int(Code[0:i1], alpha)
            l = int(Code[i1:i2], alpha) + 1
            C_3 = Code[i2]
        except:
            pass

        # do the buffer shifts
        for _ in range(l-1):
            buffer = buffer[1:] + buffer[pointer]
        buffer = buffer[1:] + C_3

        reconstructed_string += buffer[-l:]
        
        Code = Code[i2 + 1:]
    return reconstructed_string
