from MCFParser import *
from grammars import *

import time
import argparse
from pprint import pprint, pformat
import re
from itertools import permutations, chain, combinations


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


def dyck(k, n):
    # if isfile('data/{}'.format(n)):
    #     with open('data/{}'.format(n), 'r') as f:
    #         return f.read().splitlines()
    sigma = ''.join([chr(97+i) for i in range(k)])  # a,b,c,... (k letters)
    return [sigma*n] if n < 2 else sum([dshuffle(sigma, w) for w in dyck(k, n-1)], [])


#
# Grammar class
#
class Grammar(object):
    def __init__(self, rules, initial_symbol='S', **kwargs):
        # Normalize rules
        rules = sum(map(lambda r: r if isinstance(r, list) else [r],
                        map(lambda r: sum(r, []) if isinstance(r, list) and not isinstance(r[0], tuple) else r,
                    rules)), [])
        # Construct rule tuples
        self.grammar = [('{}: {} <- {} ({})'.format(i, lhs, rhs, recipe), lhs, rhs, recipe) for i, (lhs, rhs, recipe) in enumerate(rules)]
        self.parser = Parser(self.grammar, [initial_symbol], **kwargs)
        # Print statistics
        # self.parser.print_grammar_statistics()
        # self.test_parse('aaaabbcabbcbccc')
        # self.parser.print_parse_statistics()

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

    def test_n(self, n, reverse=False, half=False):
        ws = dyck(3, n)[::(-1 if reverse else 1)]
        if half:
            ws = ws[:len(ws)/2+1]
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
    parser.add_argument('-ws', type=str, help='file containing words to check', nargs='?')
    parser.add_argument('-p', type=str, help='single parse of a word', nargs='?')
    parser.add_argument('-minp', type=str, help='show minimal parse of a word', nargs='?')
    parser.add_argument('-ps', type=str, help='multiple parses of a word', nargs='?')
    parser.add_argument('-g', type=str, help='grammar to use', default='g2', nargs='?')
    parser.add_argument('--rules', help='print all rules', action='store_true')
    parser.add_argument('--check', help='check soundness', action='store_true')
    parser.add_argument('--gen', help='generate dyck words', action='store_true')
    parser.add_argument('--reverse', help='search in reverse', action='store_true')
    parser.add_argument('--half', help='search in reverse', action='store_true')
    parser.add_argument('--time', help='measure execution time', action='store_true')
    args = parser.parse_args()
    g = globals()[args.g]
    if args.time:
        start = time.time()
    if args.gen:
        assert args.n
        with open('data/{}'.format(args.n), 'w') as f:
            for w in dyck(3, args.n):
                f.write('{}\n'.format(w))
    elif args.check:
        assert args.n
        g.test_soundness(n_range=[args.n])
    elif args.rules:
        pprint(g.grammar)
    elif 'w' in vars(args) and args.w is not None:
        print(g.test_parse(args.w))
    elif 'p' in vars(args) and args.p is not None:
        g.single_parse(args.p)
    elif 'minp' in vars(args) and args.minp is not None:
        g.min_parse(args.minp)
    elif 'ps' in vars(args) and args.ps is not None:
        g.parse(args.ps)
    elif 'ws' in vars(args) and args.ws is not None:
        with open(args.ws, 'r') as f:
            for w in f.read().splitlines():
                print('{}: {}'.format(w, g.test_parse(w)))
    else:
        g.test_n(args.n, reverse=args.reverse, half=args.half)
    if args.time:
        print('Time elapsed: {} seconds'.format(time.time() - start))
