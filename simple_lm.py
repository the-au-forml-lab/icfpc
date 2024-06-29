import os
from time import sleep

import numpy as np

WALL, PILL, LM = '#', '.', 'L'


def read_file(fn):
    return open(fn, 'r').read().splitlines()


def parse(in_, start_symb=""):
    world = np.array([list(ln) for ln in in_])
    start = list(zip(*np.where(world == start_symb)))[0]
    pills = list(zip(*np.where(world == PILL)))
    return world, start, pills


def show(world, overlay=None, start=None):
    from colorama import Fore, Style
    has_o = overlay is not None
    overlay = overlay if has_o else world
    fsymb = lambda x: f"{x}"
    dchar = lambda i, j, w, o: \
        ((Fore.LIGHTGREEN_EX + fsymb(LM) + Style.RESET_ALL)
         if (i, j) == start else
         (Fore.LIGHTMAGENTA_EX + fsymb(o) + Style.RESET_ALL)
         if o and has_o else fsymb(w))
    [print("".join(
        [dchar(i, j, w, o)
         for j, (w, o) in enumerate(zip(line, overlay[i]))]))
        for i, line in enumerate(world)]
    print()


def reconstruct_path(from_: dict, current):
    total_path = [current]
    while current in from_.keys():
        current = from_[current]
        total_path.insert(0, current)
    return total_path


def moves(wld, y, x):
    return [(ny, nx) for ny, nx in
            [(y - 1, x), (y + 1, x), (y, x - 1),
             (y, x + 1), (y, x)] if
            0 <= ny < wld.shape[0] and 0 <= nx < wld.shape[1]
            and wld[ny, nx] != WALL]


def find_path(world, start, goal):
    h = lambda pt: calc_dist(goal, pt)
    g_score = np.full(world.shape, 999)
    g_score[start] = 0
    f_score = np.full(world.shape, 999)
    f_score[start] = h(start)
    open_set = [start]
    from_ = {}
    while open_set:
        current = open_set.pop(0)
        if current == goal:
            return reconstruct_path(from_, current)
        for nb in moves(world, *current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[nb]:
                from_[nb] = current
                g_score[nb] = tentative_g_score
                f_score[nb] = tentative_g_score + h(nb)
                if nb not in open_set:
                    open_set.append(nb)
    return False


def path_to_map(symb, path, h, w):
    pm = np.full((h, w), '')
    for pt in path:
        pm[pt] = symb
    return pm


def calc_dist(yx1, yx2):
    (y1, x1), (y2, x2) = yx1, yx2
    return abs(y1 - y2) + abs(x1 - x2)


def xto_points(curr, points):
    return sorted([(calc_dist(curr, pt), pt) for pt in points])


def closest(cur, pills):
    assert pills
    d2p = xto_points(cur, pills)
    min_dist, node = d2p[0]
    return node


def gen_order(start, pills):
    path = [start]
    curr, rem = start, pills
    while rem:
        nxt = closest(curr, rem)
        rem.remove(nxt)
        path.append(nxt)
        curr = nxt
    return path


def path_to_dirs(path):
    fst, seq = path[0], path[1:]
    result = []
    while seq:
        snd = seq.pop(0)
        (y1, x1), (y2, x2) = fst, snd
        if y1 == y2 and x1 > x2: result.append('L')
        if y1 == y2 and x1 < x2: result.append('R')
        if y1 < y2 and x1 == x2: result.append('D')
        if y1 > y2 and x1 == x2: result.append('U')
        fst = snd
    return ''.join(result)


def main(puzzle):
    w, s, p = parse(read_file(puzzle), start_symb=LM)

    # put the pill-coords in order using distance heuristic
    # this will determine how good the results will be
    visits = gen_order(s, p)

    # find the shortest path between segments
    curr, rest = visits[0], visits[1:]
    full_path = [s]
    while rest:
        goal = rest.pop(0)
        sub_path = find_path(w, curr, goal)
        for pt in sub_path:
            if pt in rest:
                rest.remove(pt)
        full_path += sub_path[1:]
        curr = goal
    # convert path to directions
    dirs = path_to_dirs(full_path)

    # # draw the world+path (needs: pip install colorama)
    # o = path_to_map('.', full_path, *w.shape)
    # show(w, o, s)
    #
    # for i in range(len(full_path)+1):
    #     os.system('clear')
    #     o = path_to_map('x', full_path[:i], *w.shape)
    #     show(w, o, s)
    #     sleep(.15)

    print(dirs)
    print(len(dirs))


if __name__ == '__main__':
    main('lambdaman_mazes/lambdaman1.txt')
