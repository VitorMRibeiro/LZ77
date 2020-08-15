from encode_decode import encode, decode
import binary_stuff as b
import argparse
import binascii

parser = argparse.ArgumentParser(usage='python lz77.py encode/decode [file name] -o [output file name]', description='compresses files')
parser.add_argument('Mode', choices=['encode', 'decode'], action='store')
parser.add_argument('File', action='store')
parser.add_argument('-o', help='name of the output file', action='store')

arguments = parser.parse_args()

with open(arguments.File, 'rb', encoding=None) as file:
    bin = file.read()
    pass

if arguments.o == None:
    if arguments.Mode == 'encode':
        output = arguments.File + '.Hz'
    else: 
        if arguments.File.endswith('.Hz'):
            output = arguments.File[:-2]
        else:
            output = 'decompressed_file'
else:
    output = arguments.o

if arguments.Mode == 'encode':
    S = b.byt_to_str(bin)
    bin = b.str_to_byt(encode(S))
    with open(output, 'wb', encoding=None) as file:
        file.write(bin)
else:
    C = b.byt_to_str(bin)
    bin = b.str_to_byt(decode(C))
    with open(output, 'wb', encoding=None) as file:
        file.write(bin)