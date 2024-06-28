from sys import argv

OFFSET = 33
SPC = " "
NL = "\n"
ALPHA = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"
             "\"#$%&'()*+,-./:;<=>?@[\]^_`|~") + [SPC, NL]


def read_file(fn):
    with open(fn) as fp:
        return fp.read()


def parse(s):
    print(indicator(s))
    return s


def decode_str(s):
    chars = [c for c in list(s)]
    return "".join([ALPHA[(ord(c) - OFFSET)] for c in chars])


def encode_str(s):
    chars = [c for c in list(s)]
    return "".join([chr(ALPHA.index(c) + OFFSET) for c in chars])


def indicator(s):
    fst = s[0]
    if fst == 'T': return "true"
    if fst == 'F': return "false"
    if fst == 'I': return "int"
    if fst == 'S': return decode_str(s[1:])
    if fst == 'U': return 'unary'
    if fst == 'B': return 'binary'
    if fst == '?': return 'if'
    if fst == 'L': return 'lambda abs'


if __name__ == '__main__':
    # print(parse(read_file(argv[1])))

    print(encode_str(read_file(argv[1])))
