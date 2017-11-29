import argparse
from itertools import permutations
from pprint import pprint
from MCFParser import *
from grammars import *


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
    sigma = ''.join([chr(97+i) for i in range(k)])  # a,b,c,... (k letters)
    return [sigma*n] if n < 2 else sum([dshuffle(sigma, w) for w in dyck(k, n-1)], [])


#
# Grammar class
#
class Grammar(object):
    def __init__(self, rules, initial_symbol='S'):
        # Normalize rules
        rules = sum(map(lambda r: r if isinstance(r, list) else [r],
                        map(lambda r: sum(r, []) if isinstance(r, list) and not isinstance(r[0], tuple) else r,
                    rules)), [])
        # Construct rule tuples
        self.grammar = [('r{}'.format(i), lhs, rhs, recipe) for i, (lhs, rhs, recipe) in enumerate(rules)]
        self.parser = Parser(self.grammar, [initial_symbol])

    def test_parse(self, word):
        print(self.parser.chart_parse(list(word)))

    def parse(self, word):
        for t in self.parser.parse(list(word)):
            print(t)

    def test_n(self, n):
        ws = dyck(3, n)
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
                    print('[{}] UNSOUND!!!'.format(n))
                    break
            print('[{}] SOUND!'.format(n))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check your D3 grammar.')
    parser.add_argument('-n', metavar='N', type=int, help='number of "abc" occurences', default=6, nargs='?')
    parser.add_argument('-w', metavar='W', type=str, help='single word to check', nargs='?')
    parser.add_argument('-g', metavar='G', type=str, help='grammar to use', default='g2', nargs='?')
    parser.add_argument('--rules', help='print all rules', action='store_true')
    parser.add_argument('--check', help='check soundness', action='store_true')
    args = parser.parse_args()
    g = globals()[args.g]
    if args.check:
        assert args.n
        g.test_soundness(n_range=[args.n])
    elif args.rules:
        pprint(g.grammar)
    elif 'w' in vars(args) and args.w is not None:
        g.test_parse(args.w)
    else:
        g.test_n(args.n)

