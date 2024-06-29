from sys import exit, argv


def read_file(fn):
    with open(fn) as fp:
        return fp.read()


def dist(yx1, yx2):
    (y1, x1), (y2, x2) = yx1, yx2
    return abs(y1 - y2) + abs(x1 - x2)


def pts_dist(cur, coords):
    return sorted([(dist(cur, p), p) for p in coords])


def gen_order(start, positions):
    path = [start]
    cur, rem = start, positions
    while rem:
        nxt = pts_dist(cur, rem)[0][1]
        rem.remove(nxt)
        path.append(nxt)
        cur = nxt
    return path


def press_key(press):
    return ['', (-1, -1), (0, -1), (1, -1),
            (-1, 0), (0, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)].index(press)


if __name__ == '__main__':
    input_ = "spaceship_problems/spaceship3.txt"
    raw = [l.split(' ') for l in read_file(input_).split('\n')]
    ch = [tuple([int(c) for c in r]) for r in raw]
    ordered = gen_order((0, 0), ch)
    vx, vy, presses = 0, 0, []
    curr, opn = ordered[0], ordered[1:]
    while opn:
        nxt = (n1x, n1y) = opn.pop(0)
        t1 = (t1x, t1y) = (curr[0] + vx, curr[1] + vy)
        acc_x, acc_y = n1x - t1x, n1y - t1y
        print(curr,'->', nxt, t1, (acc_x, acc_y))
        # can only handle steps of 1
        assert abs(acc_x) <= 1 and abs(acc_y) <= 1
        pkey = press_key((acc_x, acc_y))
        presses.append(pkey)
        vx += acc_x
        vy += acc_y
        curr = nxt
    print(''.join([str(s) for s in presses]))