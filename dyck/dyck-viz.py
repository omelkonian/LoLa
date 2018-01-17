import itertools as it
import shutil
import colorsys
import glob
import os

import numpy as np
from colors import *
import argparse
from graphviz import Digraph
from pdfrw import PdfReader, PdfWriter

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
    elist = [j+1 for _, j in sorted(list(zip(y, range(len(y)))))]
    tbl = np.array(elist).reshape(max(y), len(y)//max(y))
    return tbl


#
# translation to alphabetic form
#
def t2w(tbl):
    return ''.join([chr(96+i) for i in yamanouchi(tbl)])


def w2t(word):
    return tableau([ord(i)-96 for i in word])


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


def taquin_mod(words, out=[]):
    """Orbit partitioning"""
    if not words:
        return out
    else:
        tws = [t2w(t) for t in taquin_star(w2t(words[0]))]
        return taquin_mod([w for w in words if w not in tws], out + [tws])


########################################################################################################################
# 2017, Orestis Melkonian & Konstantinos Kogkalidis, Utrecht University
########################################################################################################################

########################################################################################################################
# Taquin rendering
########################################################################################################################
def all_orbits(k, n):
    orbits = taquin_mod(list(idyck(k, n)))
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
    return max([sum(map(lambda t: abs(t[0] - t[1]), zip(col, col[1:]))) for col in w2t(word).T])


def orbit(word):
    return [t2w(tbl) for tbl in taquin_star(w2t(word))]


def render_promotion(word, k):
    l = len(word)
    N = int(l/k)
    HSV_tuples = [(x * 1.0 / N, .5, 1) for x in range(N)]
    RGB_tuples = list(map(lambda x: tuple(map(lambda i: int(i * 255), colorsys.hsv_to_rgb(*x))), HSV_tuples))
    colored_word = [()] * l
    for i, word in enumerate(orbit_sort_by_rank(orbit(word)), start=1):
        tab = w2t(word)
        for ic, col in enumerate(tab.T):
            col_color = RGB_tuples[ic]
            for ir in col:
                colored_word[ir - 1] = (word[ir - 1], col_color)
        print('{}.\t'.format(i), end='')
        for char, rgb in colored_word:
            print(color(char, fg='black', bg='rgb{}'.format(str(rgb))), end='')
        print()


########################################################################################################################
# Web rendering
########################################################################################################################
small_weight, big_weight = '1', '100'
dummy_style = 'invis'
dummy_stroke = 'invis'
w_color = 'green'
big_node = '2'
node_style = 'invis'
A, B, C = '𝓐', '𝓑', '𝓒'
Ap, Bp, Cp, Am, Bm, Cm = A + '+', B + '+', C + '+', A + '-', B + '-', C + '-'


class Web(object):

    def __init__(self, word) -> None:
        self.counter = 0
        self.rank = 0
        self.word = word
        self.g = Digraph('graph')
        self.g.attr(rankdir='TB')
        self.g.attr(newrank='true')
        self.g.attr(ranksep='1.2')
        # self.g.attr(nodesep='0')
        self.g.attr(splines='false')

        with self.g.subgraph(name="cluster_0") as init_g:
            init_g.attr(rank='same')
            init_g.attr(style='invis')
            self.fringe = self.word_to_nodes(constraint=True, graph=init_g)

    def grow(self):
        # Visit fringe
        with self.g.subgraph(name='cluster_{}'.format(self.rank + 1)) as sub_g:
            used = False
            to_iterate = [i for i in self.fringe if self.extract_value(i) != 'W']
            sub_g.attr(rank='same')
            sub_g.attr(style='invis')

            # Dummies after
            new_fringe = []
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
                        intermediate = self.fresh_id('D', graph=sub_g, fixedsize='true', width='0', style='invis')
                        self.connect(l, intermediate, constraint=True, graph=sub_g, style=dummy_style)
                        self.connect(intermediate, r, constraint=True, graph=sub_g, dir='back', style=dummy_style)
                        self.connect(intermediate, new_r, constraint=True, graph=sub_g, style=dummy_style)
                        self.connect(new_l, intermediate, constraint=True, graph=sub_g, dir='back', style=dummy_style)
                        # Crossing
                        self.connect(l, new_r, constraint=False)
                        self.connect(r, new_l, constraint=False)
                        new_fringe.extend(new_ids)
                    elif len(new_ids) == 1:  # X, Y -> Z
                        new_node = new_ids[0]
                        self.connect(l, new_node, constraint=True, graph=sub_g)
                        self.connect(new_node, r, constraint=True, graph=sub_g, dir='back')
                        new_fringe.append(new_node)
                    else:  # X, Y -> W
                        w = self.fresh_id('W', graph=sub_g, fixedsize='true', width=big_node)
                        self.connect(l, w, constraint=True, graph=sub_g)
                        self.connect(w, r, constraint=True, graph=sub_g, dir='back')
                        new_fringe.append(w)
                else:
                    # Propagate dummy downwards
                    dummy = self.fresh_id(self.extract_value(l), dummy=self.extract_dummy_origin(l), graph=sub_g, style=dummy_style, width='1')
                    self.connect(l, dummy, dir='none', constraint=False, graph=sub_g)
                    new_fringe.append(dummy)

            if not used:
                # Create last dummy
                last = self.fringe[-1]
                dummy = self.fresh_id(self.extract_value(last), dummy=self.extract_dummy_origin(last), graph=sub_g, style=dummy_style, width='1')
                self.connect(last, dummy, dir='none', constraint=False, graph=sub_g)
                new_fringe.append(dummy)

            self.same_depth(new_fringe, constraint=True, graph=sub_g)

        if new_fringe == self.fringe:
            raise RuntimeError("Not growing")
        self.fringe = [i for i in new_fringe if self.extract_value(i) not in ['W', 'D']]

        # Grow from new fringe
        if self.fringe:
            self.rank += 1
            self.grow()
        else:
            self.rank = 0

    def apply_growth_rule(self, l_id, r_id, graph=None):
        l, r = map(self.extract_value, [l_id, r_id])
        ret = {
            (Ap, Bp): [Cm],
            (Ap, Cp): [Bm],
            (Bp, Cp): [Am],
            (Bm, Am): [Cp],
            (Cm, Am): [Bp],
            (Cm, Bm): [Ap],
            # +/-
            (Bp, Bm): [Am, Ap],
            (Bp, Am): [Am, Bp],
            (Ap, Bm): [Bm, Ap],
            (Ap, Am): [],
            # -/+
            (Bm, Bp): [Cp, Cm],
            (Bm, Cp): [Cp, Bm],
            (Cm, Bp): [Bp, Cm],
            (Cm, Cp): [],
        }.get((l, r), None)
        if ret is not None:
            ret = list(map(partial(self.fresh_id, graph=graph, width=big_node if len(ret) == 1 else '1'), ret))
        return ret

    def word_to_nodes(self, graph=None, constraint=False):
        to_reverse = False
        nodes = []
        for c in (reversed(self.word) if to_reverse else self.word):
            fresh_id = self.fresh_id({'a': A, 'b': B, 'c': C}[c] + '+', graph=graph)
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

    @staticmethod
    def extract_value(id):
        return id.split('@')[1]

    @staticmethod
    def is_dummy(id):
        return '$' in id

    def fresh_id(self, value, graph=None, dummy=None, **style):
        self.counter += 1
        new_id = '{}{}@{}'.format('{}$'.format(dummy) if dummy else '', self.counter, value)
        if not self.is_dummy(new_id):
            style.update(shape='none')
        (graph or self.g).node(new_id, label='' if (self.is_dummy(new_id) or 'D' in new_id) else ('●' if 'W' in new_id else value), **style)
        return new_id

    def connect(self, id1, id2, graph=None, constraint=False, propagate_constraint=False, reverse=False, **style):
        # Dummy has reached its endpoint
        style.update(
            tailclip='false' if '$' in id1 else style.get('tailclip'),
            headclip='false' if '$' in id2 else style.get('headclip'),
            style='dotted' if (('$' in id1 or '$' in id2) and 'style' not in style) else style.get('style')
        )
        if 'W' in id1:
            style.update(tailclip='false', dir='none')
        if 'W' in id2:
            style.update(headclip='false', dir='none')
        (graph or self.g).edge(id1, id2, constraint='true' if constraint else 'false', **style)

    def same_depth(self, ids, graph=None, constraint=False):
        for l, r in zip(ids, ids[1:]):
            self.connect(l, r, graph=(graph or self.g), constraint=constraint, color='red', dir='none', style=dummy_style)

    def view(self):
        self.grow()
        self.g.view()

    def render(self, equiv_class=None):
        self.grow()
        self.g.render(filename='{}{}'.format('{}_'.format(equiv_class) if equiv_class else '', self.word),
                      directory='webs',
                      cleanup=True)

    @staticmethod
    def render_orbit(word):
        orbits = orbit_sort_by_rank(orbit(word))
        l = len(orbits)
        for i, w in enumerate(orbits):
            Web(w).render(equiv_class=i)
        merger = PdfWriter()
        for filename in sorted(glob.glob('webs/*.pdf'), reverse=True):
            merger.addpages(PdfReader(filename).pages)
        merger.write('equiv_class.pdf')
        for filename in glob.glob('webs/*.pdf'):
            os.remove(filename)
        shutil.rmtree('./webs')


########################################################################################################################
# Render orbits
########################################################################################################################
def count_orbits(k, n):
    words = list(idyck(k, n))
    mod = taquin_mod(words)
    print('[{}, {}]\t #words: {}\t #orbits: {}'.format(k, n, len(words), len(mod)))


def render_all_orbits(k, n, to_print=True):
    count_orbits(k, n)
    if to_print:
        for i, orbit in enumerate(all_orbits(k, n), start=1):
            print('Orbit: {}'.format(orbit))
            # Taquin
            print('-------------- [{}] (rank: {}) ----------------'.format(i, orbit_max_rank(orbit)))
            render_promotion(orbit[0], k)
            # Webs (only for k = 3)
            if k == 3:
                for w in orbit:
                    Web(w).render(equiv_class=i)
                merger = PdfWriter()
                for filename in glob.glob('webs/*.pdf'):
                    merger.addpages(PdfReader(filename).pages)
                merger.write('equiv_class_{}.pdf'.format(i))
                for filename in glob.glob('webs/*.pdf'):
                    os.remove(filename)
                shutil.rmtree('./webs')


#
# Entry-point
#
if __name__ == '__main__':
    # Command-line parsing
    parser = argparse.ArgumentParser(description='Rendering of Dyck promotions.')
    parser.add_argument('--dim', type=str, help='symbols, size')
    parser.add_argument('--word', type=str, help='single word to render')
    parser.add_argument('-o', help='enable output', action='store_true')
    args = parser.parse_args()

    if args.dim:
        k, n = list(map(int, args.dim.split(',')))
        render_all_orbits(k, n, to_print=args.o)
    elif args.word:
        render_promotion(args.word, 3)
        Web.render_orbit(args.word)

