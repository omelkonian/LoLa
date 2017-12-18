import numpy
from math import ceil
from os.path import isfile

from MCFParser import *
from grammars import *

import time
import argparse
from pprint import pprint, pformat
import re
from itertools import permutations


#
# Dyck generation
#
def shuffle(l, r):
    if not (l and r):  # left and/or right pack are empty
        return [l + r]
    else:
        return [l[0] + w for w in shuffle(l[1:], r)] + [r[0] + w for w in shuffle(l, r[1:])]


def dshuffle(l, r):
    return [l + r] if not (l and r) else\
        [(l, r)[i][0] + w for i in range(2) if not i or r[0] < l[0] for w in dshuffle(l[(i + 1) % 2:], r[i % 2:])]


def dyck_file(n):
    return 'data/{}.dyck'.format(n)


def dyck(k, n):
    # Utilize pre-generated Dyck words
    if isfile(dyck_file(n)):
        with open(dyck_file(n), 'r') as f:
            return f.read().splitlines()
    sigma = ''.join([chr(97+i) for i in range(k)])  # a,b,c,... (k letters)
    return [sigma*n] if n < 2 else sum([dshuffle(sigma, w) for w in dyck(k, n-1)], [])


def rand_dyck(n):
    val = {
        'a': n,
        'b': 0,
        'c': 0
    }
    ret = ""
    while True:
        choices = [k for k, v in val.items() if v > 0]
        if not choices:
            break
        choice = numpy.random.choice(choices)
        ret += choice
        val[choice] -= 1
        if choice == 'a':
            val['b'] += 1
        elif choice == 'b':
            val['c'] += 1
    return ret

#
# Grammar class
#
class Grammar(object):
    def __init__(self, rules, initial_symbol='S', **kwargs):
        # Normalize rules
        rules = sum(map(lambda r: r if isinstance(r, list) else [r],
                        map(lambda r: sum(r, []) if isinstance(r, list) and (not r or not isinstance(r[0], tuple)) else r,
                    rules)), [])
        # Construct rule tuples
        self.grammar = [('{}: {} <- {} ({})'.format(i, lhs, rhs, recipe), lhs, rhs, recipe)
                        for i, (lhs, rhs, recipe) in enumerate(rules)]
        self.parser = Parser(self.grammar, [initial_symbol], **kwargs)

    def test_parse(self, word):
        return self.parser.chart_parse(list(word))

    def single_parse(self, word):
        print(self.format_parse(next(self.parser.parse(list(word)))))

    def parse(self, word):
        for t in self.parser.parse(list(word)):
            print('{}\n'.format(self.format_parse(t)))

    def min_parse(self, word):
        l, min_parse = 100, None
        for t in self.parser.parse(list(word)):
            p = self.format_parse(t)
            cur_l = len(p.split('\n'))
            if cur_l < l:
                l, min_parse = cur_l, p
        print('{}\n'.format(min_parse))

    def test_n(self, n, range=(0.0, 100.0)):
        ws = dyck(3, n)
        l = len(ws)
        start, end = map(lambda p: int(ceil(l * (p/100))), range)
        print('Checking {} to {}'.format(start, end))
        ws = ws[start:end]
        c = 1
        for i, w in enumerate(ws):
            sys.stdout.write("\r{0:.2f}%".format(float(i) / float(len(ws)) * 100.0))
            sys.stdout.flush()
            if not self.parser.chart_parse(list(w)):
                print('\n{0}.\t {1}'.format(c, w))
                c += 1
        print('\n-------------- [{0} out of {1}] --------------'.format(c - 1, len(ws)))

    def test_soundness(self, n_range=range(1, 10)):
        for n in n_range:
            d = dyck(3, n)
            for w in permutations('abc' * n):
                s = "".join(w)
                if s not in d and self.parser.chart_parse(w):
                    print('[{}] UNSOUND for {}'.format(n, s))
                    return
            print('[{}] SOUND!'.format(n))

    @staticmethod
    def format_parse(s):
        return re.sub(r'\(.*\: ', '',
                      pformat(s, indent=3)
                      .replace('(0, 0)', 'x').replace('(0, 1)', 'y').replace('(1, 0)', 'z')
                      .replace('(1, 1)', 'w').replace(' [] ', '').replace('"', ''))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check your D3 grammar.')
    parser.add_argument('-n', type=int, help='number of "abc" occurences', default=6, nargs='?')
    parser.add_argument('-w', type=str, help='single word to check', nargs='?')
    parser.add_argument('-p', help='single parse of a word', action='store_true')
    parser.add_argument('-minp', help='show minimal parse of a word', action='store_true')
    parser.add_argument('-r', help='single word to check in reverse', action='store_true')
    parser.add_argument('-ws', type=str, help='file containing words to check', nargs='?')
    parser.add_argument('-ps', type=str, help='multiple parses of a word', nargs='?')
    parser.add_argument('-g', type=str, help='grammar to use', default='g', nargs='?')
    parser.add_argument('-i', type=str, help='initial symbol to use', default='S', nargs='?')
    parser.add_argument('--rules', help='print all rules', action='store_true')
    parser.add_argument('--check', help='check soundness', action='store_true')
    parser.add_argument('--gen', help='generate dyck words', action='store_true')
    parser.add_argument('--range', type=str, default='0-100%', help='search in given percentage range')
    parser.add_argument('--time', help='measure execution time', action='store_true')
    parser.add_argument('--rand', help='generate random Dyck word', action='store_true')
    parser.add_argument('--full', help='stress test given word', action='store_true')
    args = parser.parse_args()
    if args.r:
        args.w = ''.join(list(reversed(args.w.replace('a', '$').replace('c', 'a').replace('$', 'c'))))
        print(args.w)
    if args.full:
        args.i = '$_W'
    g = globals()[args.g](args.i)
    if args.time:
        start = time.time()
    if args.rand:
        while True:
            r = rand_dyck(args.n)
            print('{}: {}'.format(r, g.test_parse(r)))
    elif args.gen:
        assert args.n
        ws = dyck(3, args.n)
        with open(dyck_file(args.n), 'w') as f:
            for w in ws:
                f.write('{}\n'.format(w))
    elif args.check:
        assert args.n
        g.test_soundness(n_range=[args.n])
    elif args.rules:
        pprint(g.grammar)
    elif 'w' in vars(args) and args.w is not None:
        if args.full:
            choices = range(0, len(args.w) + 1)
            for index in choices:
                new_w = args.w[:index] + '$' + args.w[index:]
                print('{}: {}'.format(new_w, g.test_parse(new_w)))
        else:
            if args.p:
                g.single_parse(args.w)
            elif args.minp:
                g.min_parse(args.w)
            else:
                print(g.test_parse(args.w))
    elif 'ps' in vars(args) and args.ps is not None:
        g.parse(args.ps)
    elif 'ws' in vars(args) and args.ws is not None:
        with open(args.ws, 'r') as f:
            for w in f.read().splitlines():
                print('{}: {}'.format(w, g.test_parse(w)))
    else:
        g.test_n(args.n, range=map(float, args.range.strip('%').split('-')))
    if args.time:
        print('Time elapsed: {} seconds'.format(time.time() - start))
