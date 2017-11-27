import sys
import argparse
from itertools import permutations
from pprint import pprint
from MCFParser import *


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
        print('-------------- [{0} out of {1}] --------------'.format(c - 1, len(ws)))

    def test_soundness(self):
        for n in range(1, 10):
            d = dyck(3, n)
            for w in permutations('abc' * n):
                s = "".join(w)
                if s not in d and self.parser.chart_parse(w):
                    print('[{}] UNSOUND!!!'.format(n))
                    break
            print('[{}] SOUND!'.format(n))


#
# Grammar 1
#
S, W, e = 'S', 'W', []
a, b, c = 'a', 'b', 'c'
A, A_, B, B_, C, C_ = 'A', 'A-', 'B', 'B-', 'C', 'C-'
AB, AC, BA, CA, BC, CB, AA, BB, CC = 'AB', 'AC', 'BA', 'CA', 'BC', 'CB', 'AA', 'BB', 'CC'
A_B_, A_C_, B_A_, C_A_, B_C_, C_B_, A_A_, B_B_, C_C_ = 'A-B-', 'A-C-', 'B-A-', 'C-A-', 'B-C-', 'C-B-', 'A-A-', 'B-B-', 'C-C-'
AC_, C_A, A_A, AA_, CC_, CA_, A_C, BA_, C_B, B_C, AB_, BB_, BC_ = 'AC-', 'C-A', 'A-A', 'AA-', 'CC-', 'CA-', 'A-C', 'BA-', 'C-B', 'B-C', 'AB-', 'BB_', 'BC_'
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)
std, std_abc = [[x, y], [z, w]], [[a, x, y], [b, z, w, c]]
all_singles = [A, A_, B, B_, C, C_]
all_doubles = [AA, AA_, AB, AB_, AC, AC_, BA_, BB, BB_, BC, BC_, CC, CC_, A_A_, A_B_, A_C_, B_B_, B_C_, C_C_]

g1 = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W BASE
    (W, e, [[a, b, c], e]),
    (W, e, [[a, b], [c]]),
    (W, e, [[a], [b, c]]),
    # W PERMUTATIONS
    (W, [W, W], [[x, y], [z, w]]),
    (W, [W, W], [[x, z], [y, w]]),
    (W, [W, W], [[x, z], [w, y]]),
    (W, [W, W], [[z, x], [y, w]]),
    (W, [W, W], [[z, x], [w, y]]),
    (W, [W, W], [[z, w], [x, y]]),
    (W, [W, W], [[x, y, z], [w]]),
    (W, [W, W], [[x], [y, z, w]]),
    # W TRIPLE INSERTION (BASE)
    # (W, [W], [[a, x, b, y, c], e]),
    # (W, [W], [[a, x, b, y], [c]]),
    (W, [W], [[a, x, b], [y, c]]),
    # (W, [W], [[a, b, x], [y, c]]),
    # (W, [W], [[a, x], [b, y, c]]),
    # (W, [W], [[a], [x, b, y, c]]),
    # (W, [W], [[], [x, b, y, c]]),
    # W TRIPLE INSERTION (COMB)
    (W, [W, W], [[a, x, b], [z, c, y, w]]),
    (W, [W, W], [[a, x, b], [z, c, w, y, ]]),
    (W, [W, W], [[x, z, a, y, b], [w, c]]),
    (W, [W, W], [[x, z, a, w, b], [y, c]]),
    # A+, B+, C+
    [[
        (l.upper(), e, [[l], e]),
        (l.upper(), e, [e, [l]]),
        (l.upper(), [W], [[l, x], [y]]),
        (l.upper(), [W], [[x, l], [y]]),
        (l.upper(), [W], [[x], [y, l]]),
    ] for l in "abc"],
    # NEGATIVES (BASE)
    (C_, [A, B], [[x, y], [z, w]]),
    (A_, [B, C], [[x, y], [z, w]]),
    (B_, [A, C], [[x, y], [z, w]]),
    # NEGATIVES (COMB)
    [[
        (W, [l, r], [[x, y, z, w], e]),
        (W, [l, r], [[x, y, z], [w]]),
        (W, [l, r], [[x, y], [z, w]]),
        # (W, [l, r], [[x],          [y, z, w]]),
    ] for l, r in [(C_, C), (A, A_)]],
    # NEGATIVES (COMB')

    # DOUBLES (INVERSE)
    [(k + l, [l + k], [[x], [y]]) for k in all_singles for l in all_singles],
    # DOUBLES (BASE)
    [(k + l, [k, l], [[x, y], [z, w]]) for k in all_singles for l in all_singles],
    # DOUBLES (REDUCTION)
    [[
        (k + l, [k + A, A_ + l], std),
        (k + l, [k + C_, C + l], std),
        (l, [A, A_ + l], std),
        (k, [k + A, A_], std),
        (l, [C_, C + l], std),
        (k, [k + C_, C], std),
    ] for k in all_singles for l in all_singles],
    # DOUBLES (K/L)
    [[
        # POSITIVE
        (k + C_, [k + A, B], std),
        (k + C_, [A, k + B], std),
        (k + A_, [k + B, C], std),
        (k + A_, [B, k + C], std),
    ] for k in all_singles],
    # AD-HOC
    (A_C_, [AB, BC], std),

    (W, [AA, A_A_], std),
    (W, [C_C_, CC], std),

    (BA, [C_, A_A], std),
    (BB, [C_B, A_], std),

    (C_C_, [AA, BB], std),
    (A_A_, [BB, CC], std),

    (CC, [B_, A_C], std),
    (B_C, [A, CC], std),
    (CC, [B_C, A_], std),

    # DOUBLES (TRIPLE INSERTION)

    #
    # Aggregated
    #
    [[
        (d, [d], [[a, x, b], [y, c]]),
        (d, [d], [[a, b, x], [y, c]])
    ] for d in all_doubles],
    [[
        (d, [A_A, d], std_abc),
    ] for d in all_doubles],
    [[
        (d, [d, CC_], std_abc),
    ] for d in all_doubles],
    [[
        (C_ + r, [A + r, A_C_], std_abc),
    ] for r in all_singles],
    [[
        (l + A_, [A_C_, l + C], std_abc),
    ] for l in all_singles],

    #
    # Exhaustive
    #
    (BA, [AB, A_A], std_abc),
    (BA, [AB, A_A], std_abc),
    (AA, [C_C_, B_B_], std_abc),
    (CC, [B_B_, A_A_], std_abc),

    (W, [AA, A_A_], std_abc),
    (W, [C_C_, CC], std_abc),
    (W, [C_A, A_C], std_abc),

    (W, [A_A, CC_], std_abc),

    # AA
    (AA, [AA, AA_], std_abc),
    (C_, [AA, BA_], std_abc),
    (C_C_, [AA, BB], std_abc),
    (B_B_, [AA, CC], std_abc),
    (B_B_, [AA, CC], std_abc),
    (AA, [AA, CC_], std_abc),
    (W, [AA, A_A_], std_abc),
    (AB_, [AA, A_B_], std_abc),
    (AC_, [AA, A_C_], std_abc),
    # AA_
    (A_, [AA_, BC], std_abc),
    (W, [AA_, CC_], std_abc),
    # AB
    (AB, [AB, AA_], std_abc),
    (C_C_, [AB, AB], std_abc),
    (A, [AB, AC], std_abc),
    (AB, [AB, BB_], std_abc),
    (B, [AB, BC], std_abc),
    (A_, [AB, CA_], std_abc),
    (C, [AB, CC], std_abc),
    (C_, [AB, CC_], std_abc),
    (BA_, [AB, A_A_], std_abc),
    (AA_, [AB, A_B_], std_abc),
    (BC_, [AB, A_C_], std_abc),
    (AB_, [AB, B_B_], std_abc),
    (AC_, [AB, B_C_], std_abc),

])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check your D3 grammar.')
    parser.add_argument('-n', metavar='N', type=int, help='number of "abc" occurences', default=6, nargs='?')
    parser.add_argument('-w', metavar='W', type=str, help='single word to check', nargs='?')
    parser.add_argument('-g', metavar='G', type=str, help='grammar to use', default='g1', nargs='?')
    parser.add_argument('--rules', help='print all rules', action='store_true')
    args = parser.parse_args()
    g = globals()[args.g]
    if args.rules:
        pprint(g.grammar)
    elif 'w' in vars(args) and args.w is not None:
        g.test_parse(args.w)
    else:
        g.test_n(args.n)

