import itertools as it
import colorsys
import numpy as np
from colors import *
import argparse

########################################################################################################################
# 2017, Dr. Michael Moortgat, Utrecht University
########################################################################################################################

#
# Dyck generation
#
def ishuffle(l, r):
    if not (l and r):
        yield l+r
    else:
        yield from ((l, r)[i][0]+w for i in range(2) if not i or r[0] < l[0] for w in ishuffle(l[(i+1) % 2:], r[i % 2:]))


def idyck(k, n):
    sigma = ''.join([chr(97+i) for i in range(k)]) # a,b,c,... (k letters)
    if n < 2:
        yield sigma*n
    else:
        yield from it.chain.from_iterable((ishuffle(sigma, w) for w in idyck(k, n-1)))


#
# conversion tableaux <-> words
#
def yamanouchi(tbl):
    """Young tableau --> Yamanouchi word"""
    word = np.arange(tbl.size)
    for i, j in np.ndindex(tbl.shape):
        word[tbl[i, j]-1] = i+1
    return word


def tableau(y):
    """Yamanouchi word --> Young tableau"""
    elist = [ j+1 for _,j in sorted(list(zip(y,range(len(y))))) ]
    tbl = np.array(elist).reshape(max(y),len(y)//max(y))
    return tbl


#
# translation to alphabetic form
#
def t2w(tbl):
    return ''.join([ chr(96+i) for i in yamanouchi(tbl) ])

def w2t(word):
    return tableau([ ord(i)-96 for i in word ])


#
# Jeu-de-taquin
#
def taquin(tbl):
    return taquin_move(tbl - 1, 0, 0)


def taquin_move(tbl, r, c):
    if right(tbl, r, c) is None and under(tbl, r, c) is None:
        tbl[r][c] = tbl.size
        return tbl
    else:
        r1, c1 = update(tbl, r, c)
        tbl[r][c] = tbl[r1][c1]
        return taquin_move(tbl, r1, c1)


def update(tbl, r, c):
    if right(tbl, r, c) is None: return r + 1, c
    if under(tbl, r, c) is None: return r, c + 1
    if min(right(tbl, r, c), under(tbl, r, c)) == tbl[r + 1][c]: return r + 1, c
    return r, c + 1


def right(tbl, r, c):
    if c >= len(tbl[r]) - 1:
        return None
    else:
        return tbl[r][c + 1]


def under(tbl, r, c):
    if r >= len(tbl) - 1:
        return None
    else:
        return tbl[r + 1][c]


def taquin_star(tbl):
    """closure"""
    result = [tbl]
    while len(result) == 1 or not np.array_equal(result[-1], tbl):
        result.append(taquin(result[-1]))
    return result[:-1]


def taquin_mod(words,out=[]):
    """Orbit partitioning"""
    if not words: return out
    else:
        tws = [ t2w(t) for t in taquin_star(w2t(words[0])) ]
        return taquin_mod([ w for w in words if not w in tws ],out+[ tws ])


########################################################################################################################
# 2017, Orestis Melkonian & Konstantinos Kogkalidis, Utrecht University
########################################################################################################################
def all_orbits(k, n):
    orbits = taquin_mod(list(idyck(k, n)))
    # return orbits_sort_by_rank(list(map(lambda orbit: orbit_sort_by_rank(orbit), orbits)))
    return orbits_sort_by_length(list(map(lambda orbit: orbit_sort_by_rank(orbit), orbits)))


def orbits_sort_by_length(orbits):
    return sorted(orbits, key=lambda orbit: len(orbit), reverse=True)


def orbits_sort_by_rank(orbits):
    return sorted(orbits, key=lambda orbit: orbit_max_rank(orbit), reverse=True)


def orbit_max_rank(orbit):
    return rank_word(orbit_sort_by_rank(orbit)[0])


def orbit_sort_by_rank(orbit):
    return sorted(orbit, key=lambda w: rank_word(w))


def rank_word(word):
    return sum([sum(map(lambda t: abs(t[0] - t[1]), zip(col, col[1:]))) for col in w2t(word).T])


def orbit(word):
    return [t2w(tbl) for tbl in taquin_star(w2t(word))]


def count_orbits(k, n):
    words = list(idyck(k, n))
    mod = taquin_mod(words)
    print('[{}, {}]\t #words: {}\t #orbits: {}'.format(k, n, len(words), len(mod)))


def render_promotion(word, k):
    l = len(word)
    N = int(l/k)
    HSV_tuples = [(x * 1.0 / N, .5, 1) for x in range(N)]
    RGB_tuples = list(map(lambda x: tuple(map(lambda i: int(i * 255), colorsys.hsv_to_rgb(*x))), HSV_tuples))
    colored_word = [()] * l
    for i, word in enumerate(orbit(word), start=1):
        tab = w2t(word)
        for ic, col in enumerate(tab.T):
            col_color = RGB_tuples[ic]
            for ir in col:
                colored_word[ir - 1] = (word[ir - 1], col_color)
        print('{}.\t'.format(i), end='')
        for char, rgb in colored_word:
            print(color(char, fg='black', bg='rgb{}'.format(str(rgb))), end='')
        print()


def render_all_orbits(k, n, to_print=True):
    count_orbits(k, n)
    if to_print:
        for i, orbit in enumerate(all_orbits(k, n), start=1):
            print('-------------- [{}] (#{}) (rank: {})----------------'.format(i, len(orbit), orbit_max_rank(orbit)))
            render_promotion(orbit[0], k)
            # render_promotion(orbit[0], k)

#
# Entry-point
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Colored rendering of Dyck promotions.')
    parser.add_argument('-k', type=int, help='symbols in the alphabet', default=3, nargs='?')
    parser.add_argument('-n', type=int, help='number of "abc" occurences', default=3, nargs='?')
    parser.add_argument('-o', help='enable output', action='store_true')
    args = parser.parse_args()
    render_all_orbits(args.k, args.n, to_print=args.o)
