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

test = '''SB%,,/}!.$}7%,#/-%}4/}4(%}M#(//,}/&}4(%}</5.$}P!2)!",%_~~<%&/2%}4!+).'}!}#/523%j}7%}35''%34}4(!4}9/5}(!6%}!},//+}!2/5.$l}S/5e2%}./7},//+).'}!4}4(%}u).$%8wl}N/}02!#4)#%}9/52}#/--5.)#!4)/.}3+),,3j}9/5}#!.}53%}/52}u%#(/w}3%26)#%l}@524(%2-/2%j}4/}+./7}(/7}9/5}!.$}/4(%2}345$%.43}!2%}$/).'j}9/5}#!.},//+}!4}4(%}u3#/2%"/!2$wl~~;&4%2},//+).'}!2/5.$j}9/5}-!9}"%}!$-)44%$}4/}9/52}&)234}#/523%3j}3/}-!+%}352%}4/}#(%#+}4()3}0!'%}&2/-}4)-%}4/}4)-%l}C.}4(%}-%!.4)-%j})&}9/5}7!.4}4/}02!#4)#%}-/2%}!$6!.#%$}#/--5.)#!4)/.}3+),,3j}9/5}-!9}!,3/}4!+%}/52}u,!.'5!'%y4%34wl~'''
