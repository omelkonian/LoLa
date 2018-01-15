import itertools as it
from functools import partial
import colorsys
from math import ceil, floor

import numpy as np
from colors import *
import argparse
from graphviz import Graph, Digraph

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

########################################################################################################################
# Taquin rendering
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


########################################################################################################################
# Web rendering
########################################################################################################################
small_weight, big_weight = '1', '100'
dummy_style = 'invis'
dummy_stroke = ''
w_color = 'green'

class Web(object):

    def __init__(self, word) -> None:
        self.counter = 0
        self.rank = 0
        self.word = word
        self.g = Digraph('web', filename='web.gv')
        self.g.attr(rankdir='TB')
        self.g.attr(newrank='true')
        self.g.attr(ranksep='1.2 equally')
        # self.g.attr(nodesep='1')
        self.g.attr(splines='false')

        with self.g.subgraph(name="cluster_0") as init_g:
            init_g.attr(rank='same')
            init_g.attr(style='invis')
            self.fringe = self.word_to_nodes(constraint=True, graph=init_g)

    def grow(self, before=0, after=0, previous_fringe=None):
        # Visit fringe
        with self.g.subgraph(name='cluster_{}'.format(self.rank + 1)) as sub_g:
            used = False
            to_iterate = [i for i in self.fringe if self.extract_value(i) != 'W']
            sub_g.attr(rank='same')
            sub_g.attr(style='invis')
            sub_g.attr(nodesep='5')

            len_0 = previous_fringe or 0
            # Dummies after
            new_fringe = [self.fresh_id('D', graph=sub_g, label='', style=dummy_style) for _ in range(before)]

            for l, r in zip(to_iterate, to_iterate[1:]):
                # Check if you can use `l`
                if used:
                    used = False
                    continue
                # Check if growth rule applies
                new_ids = self.apply_growth_rule(l, r)
                used = new_ids is not None

                # Update new_fringe
                if used:
                    if len(new_ids) == 2:  # X, Y -> Y, X
                        [new_l, new_r] = new_ids
                        intermediate = self.fresh_id('D', graph=sub_g, label='', fixedsize='true', width='0', style='invis')
                        self.connect(l, intermediate, constraint=True, graph=sub_g, style='invis')
                        self.connect(intermediate, r, constraint=True, graph=sub_g, dir='back', style='invis')
                        self.connect(intermediate, new_r, constraint=True, graph=sub_g, style='invis')
                        self.connect(new_l, intermediate, constraint=True, graph=sub_g, dir='back', style='invis')
                        # Crossing
                        self.connect(l, new_r, constraint=False, dir='both')
                        self.connect(r, new_l, constraint=False, dir='both')
                        new_fringe.extend(new_ids)
                    elif len(new_ids) == 1:  # X, Y -> Z
                        for id in new_ids:
                            self.connect(l, id, constraint=True, graph=sub_g)
                            self.connect(id, r, constraint=True, graph=sub_g, dir='back')
                            # Also one dummy node for alignment
                            dummy = self.fresh_id('D', graph=sub_g, style=dummy_style, label='', width='1')
                            # dummy2 = self.fresh_id('D', graph=sub_g, style=dummy_style, label='', width='0.42')
                            new_fringe.append(dummy)
                            new_fringe.extend(new_ids)
                            # new_fringe.append(dummy2)
                    else:  # X, Y -> W
                        w = self.fresh_id('W', color='green', graph=sub_g, style=dummy_style, fixedsize='true', width='1')
                        self.connect(l, w, constraint=True, graph=sub_g)
                        self.connect(w, r, constraint=True, graph=sub_g, dir='back')

                        # Also one dummy node for alignment
                        dummy = self.fresh_id('D', graph=sub_g, style=dummy_style, label='', width='1')
                        # dummy2 = self.fresh_id('D', graph=sub_g, style='invis', label='', width='0.42')
                        new_fringe.append(dummy)
                        new_fringe.append(w)
                        # new_fringe.append(dummy2)

                        # self.connect(self.get_origin(l), self.get_origin(r), constraint=False, color=w_color, dir='both')
                else:
                    # Propagate dummy downwards
                    dummy = self.fresh_id(self.extract_value(l), dummy=self.extract_dummy_origin(l), graph=sub_g, style=dummy_style, label='', width='1')
                    self.connect(l, dummy, dir='none', constraint=False, graph=sub_g)
                    new_fringe.append(dummy)

            if not used:
                # Create last dummy
                last = self.fringe[-1]
                dummy = self.fresh_id(self.extract_value(last), dummy=self.extract_dummy_origin(last), graph=sub_g, style='invis', label='', width='1')
                self.connect(last, dummy, dir='none', constraint=False, graph=sub_g)
                new_fringe.append(dummy)

            # Dummies after
            new_fringe.extend([self.fresh_id('D', graph=sub_g, label='', style=dummy_style) for _ in range(after)])


            self.same_depth(new_fringe, constraint=True, graph=sub_g)

        if new_fringe == self.fringe:
            raise RuntimeError("Not growing")
        # print('Fringe: {}'.format(new_fringe))
        self.fringe = [i for i in new_fringe if self.extract_value(i) not in ['W', 'D']]
        len_1 = len(self.fringe)
        print('before, after, len_1, len2', (before, after, len_0, len_1))

        to_insert = len_0 - len_1 if len_0 > len_1 else 0
        ins_left, ins_right = 0, 0 # int(floor(to_insert/2)), int(ceil(to_insert/2))
        print('ins, insL, insR', (to_insert, ins_left, ins_right))

        # Grow from new fringe
        if self.fringe:
            self.rank += 1
            self.grow(before=before + ins_left, after=after + ins_right, previous_fringe=len_1)
        else:
            self.rank = 0

    def apply_growth_rule(self, l_id, r_id, graph=None):
        l, r = map(self.extract_value, [l_id, r_id])
        ret = {
            ('A+', 'B+'): ['C-'],
            ('A+', 'C+'): ['B-'],
            ('B+', 'C+'): ['A-'],
            ('B-', 'A-'): ['C+'],
            ('C-', 'A-'): ['B+'],
            ('C-', 'B-'): ['A+'],
            # +/-
            ('B+', 'B-'): ['A-', 'A+'],
            ('B+', 'A-'): ['A-', 'B+'],
            ('A+', 'B-'): ['B-', 'A+'],
            ('A+', 'A-'): [],
            # -/+
            ('B-', 'B+'): ['C+', 'C-'],
            ('B-', 'C+'): ['C+', 'B-'],
            ('C-', 'B+'): ['B+', 'C-'],
            ('C-', 'C+'): [],
        }.get((l, r), None)
        if ret is not None:
            ret = list(map(partial(self.fresh_id, graph=graph, width='1' if len(ret) == 1 else '1'), ret))
        return ret

    def word_to_nodes(self, graph=None, constraint=False):
        # word: "aabbcc"
        to_reverse = False
        nodes = []
        for c in (reversed(self.word) if to_reverse else self.word):
            fresh_id = self.fresh_id(c.upper() + '+', graph=graph)
            nodes.append(fresh_id)
        if to_reverse:
            nodes.reverse()
        self.same_depth(nodes, graph=graph, constraint=constraint)
        return nodes

    def extract_dummy_origin(self, id):
        if self.is_dummy(id):
            return id.split('$')[0]
        return self.extract_id(id)

    def get_origin(self, dummy):
        if not self.is_dummy(dummy):
            return dummy
        return '{}@{}'.format(self.extract_dummy_origin(dummy), self.extract_value(dummy))

    def extract_id(self, id):
        if self.is_dummy(id):
            return self.extract_id(id.split('$')[1])
        return id.split('@')[0]

    def extract_value(self, id):
        return id.split('@')[1]

    def is_dummy(self, id):
        return '$' in id

    def fresh_id(self, value, graph=None, dummy=None, **style):
        self.counter += 1
        new_id = '{}{}@{}'.format('{}$'.format(dummy) if dummy else '', self.counter, value)
        (graph or self.g).node(new_id, **style)
        return new_id

    def connect(self, id1, id2, graph=None, constraint=False, propagate_constraint=False, reverse=False, **style):
        # Dummy has reached its endpoint
        style.update(
            tailclip='false' if '$' in id1 else style.get('tailclip'),
            headclip='false' if '$' in id2 else style.get('headclip'),
            style='invis' if (('$' in id1 or '$' in id2) and 'style' not in style) else style.get('style')
        )
        if style.get('dir') is 'back':
            reverse = True

        if 'W' in id1 or 'W' in id2:
            style.update(
                headclip='false',
                dir='none'
            )
        (graph or self.g).edge(id1, id2, constraint='true' if constraint else 'false', **style)

        if reverse:
            t = id1
            id1 = id2
            id2 = t
        if self.is_dummy(id1) and not self.is_dummy(id2) and ('color' not in style or style['color'] != 'red') and self.extract_value(id2) != 'D':
            self.connect(self.get_origin(id1), id2,
                         graph=self.g, constraint=propagate_constraint, style=dummy_stroke, dir='none', weight='1')

    def same_depth(self, ids, graph=None, constraint=False):
        for l, r in zip(ids, ids[1:]):
            self.connect(l, r, graph=(graph or self.g), constraint=constraint, color='red', dir='none', style='invis')

    def render(self):
        self.grow()
        # print('Graph: {}'.format(self.g))
        self.g.view()


#
# Entry-point
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Colored rendering of Dyck promotions.')
    parser.add_argument('-k', type=int, help='symbols in the alphabet', default=3, nargs='?')
    parser.add_argument('-n', type=int, help='number of "abc" occurences', default=3, nargs='?')
    parser.add_argument('-o', help='enable output', action='store_true')
    parser.add_argument('-w', type=str, help='single word to check', nargs='?')
    args = parser.parse_args()

    if 'w' in vars(args):
        Web(args.w).render()
    else:
        render_all_orbits(args.k, args.n, to_print=args.o)
