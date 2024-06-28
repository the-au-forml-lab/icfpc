from sys import exit, argv

OFFSET = 33
BASE = 94
SPC = " "
NL = "\n"
ALPHA = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"
             "\"#$%&'()*+,-./:;<=>?@[\]^_`|~") + [SPC, NL]


def read_file(fn):
    with open(fn) as fp:
        return fp.read()


def encode_num(n):
    out = []
    while n:
        n, r = divmod(n, BASE)
        out.append(chr(OFFSET + r))
    return(''.join(out[::-1]))

def decode_num(body):
    assert body != ''
    down = (ord(c) - OFFSET for c in body[::-1])
    s = 0
    for p, x in enumerate(down):
        s += x * (BASE ** p)
    return s


def decode_str(s):
    chars = [c for c in list(s)]
    return "".join([ALPHA[(ord(c) - OFFSET)] for c in chars])


def encode_str(s):
    chars = [c for c in list(s)]
    return "".join([chr(ALPHA.index(c) + OFFSET) for c in chars])


#if __name__ == '__main__':
#    # print(parse(read_file(argv[1])))
#    print(encode_str(read_file(argv[1])))
