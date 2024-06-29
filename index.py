from sys import exit, argv

OFFSET = 33
BASE = 94
SPC = " "
NL = "\n"
ALPHA = list(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"
    "\"#$%&'()*+,-./:;<=>?@[\]^_`|~") + [SPC, NL]


def read_file(fn):
    with open(fn) as fp:
        return fp.read()


def encode_num(n):
    out = []
    while n:
        n, r = divmod(n, BASE)
        out.append(chr(OFFSET + r))
    return ''.join(out[::-1])


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


def decode_bin(c):
    if c == '.': return 'concat'
    if c == 'T': return 'take'
    if c == 'D': return 'drop'
    if c == '$': return 'B$'
    return c


def decode_lambda(l):
    return f'v{decode_num(l)}'


def decode_tokens(s):
    tokens = s.split(' ')
    if [t for t in tokens if t[0] not in 'TF?SBLvI']:
        print('original:\n' + s)
        print(f'yellow tokens not translated')
    return " ".join([
        'true' if t[0] == 'T' else
        'false' if t[0] == 'F' else
        'if' if t[0] == '?' else
        decode_str(t[1:]) if t[0] == 'S' else
        decode_bin(t[1:]) if t[0] == 'B' else
        decode_lambda(t[1:]) if t[0] in ('L', 'v') else
        str(decode_num(t[1:])) if t[0] == 'I'
        else f'\033[93m{t}\033[0m'
        for t in tokens if t])


# if __name__ == '__main__':
#    # print(parse(read_file(argv[1])))
#    print(encode_str(read_file(argv[1])))
