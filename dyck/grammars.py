from dyck import Grammar
from itertools import permutations
from pprint import pprint


#
# Universal constants
#

a, b, c = 'a', 'b', 'c'
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)

# map_vars = {
#     (0,0): "a"
# }

S, W, e = 'S', 'W', []
std, std_abc = [[x, y], [z, w]], [[a, x, y], [b, z, w, c]]
std_xyzw = [
    [[x, y], [z, w]],
    [[x, z], [y, w]],
    [[x, z], [w, y]],
    [[z, x], [y, w]],
    [[z, x], [w, y]],
    [[z, w], [x, y]],
    [[x, y, z], [w]],
    [[x], [y, z, w]],
]


def is_ordered(symbols, orders):
    return all([is_ordered_single(symbols, order) for order in orders])


def is_ordered_single(symbols, order):
    for i, o in enumerate(order):
        for j, symbol in enumerate(symbols):
            if symbol == o:
                return is_ordered_single(symbols[j+1:], order[i+1:])
            if symbol != o and symbol in order:
                return False
    return True


def ordered_permutations(orders):
    return [''.join(s)
            for s in permutations(''.join(orders))
            if is_ordered(s, orders)]


def ordered_pairs(orders):
    return [(perm[:n1 + 1], perm[n1 + 1:])
            for n1 in range(0, len(''.join(orders)))
            for perm in ordered_permutations(orders)]


def post_process(orders):
    return [(post_process_single(l), post_process_single(r))
            for l, r in ordered_pairs(orders)]


def post_process_single(order):
    return [globals()[c] for c in order]


def pre_process(symbols):
    return [pre_process_single(s) for s in symbols]


def pre_process_single(symbols):
    ret = ""
    for s in symbols:
        if isinstance(s, tuple):
            if s[0] == 0:
                if s[1] == 0:
                    ret += "x"
                else:
                    ret += "y"
            else:
                if s[1] == 0:
                    ret += "z"
                else:
                    ret += "w"
        elif s == []:
            print(s)
            ret += 'e'
        else:
            ret += s
    return ret


def all_ordered(*orders):
    return post_process(pre_process(orders))


#
# New grammar from scratch
#
# TODO define non-terminals, etc...
g2 = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W: Base
    [(W, e, order) for order in all_ordered([a, b, c])],
    (W, e, [[a, b, c], e]),
    # W: Concatenation
    [(W, [W, W], order) for order in all_ordered([x, y], [z, w])],
    # W: Triple insertion
    [(W, [W], order) for order in all_ordered([x, y], [a, b, c])],
    [(W, [W, W], order) for order in all_ordered([x, y], [z, w], [a, b, c])],

    # A-: Base
    [('A-', e, order) for order in all_ordered([b, c])],
    # A-: Double insertion (b, c)
    [('A-', [W], order) for order in all_ordered([x, y], [b, c])],
    # A-: Triple insertion
    [('A-', ['A-'], order) for order in all_ordered([x, y], [a, b, c])],
    # A- -> W
    [(W, ['A-'], order) for order in all_ordered([a, x, y])],

    # C-: Base
    [('C-', e, order) for order in all_ordered([a, b])],
    # C-: Double insertion (a, b)
    [('C-', [W], order) for order in all_ordered([x, y], [a, b])],
    # C-: Triple insertion
    [('C-', ['C-'], order) for order in all_ordered([x, y], [a, b, c])],
    # C- -> W
    [(W, ['C-'], order) for order in all_ordered([x, y, c])],

    # A+: Base
    [('A+', e, order) for order in all_ordered([a])],
    # A+: Single insertion (a)
    [('A+', [W], order) for order in all_ordered([x, y], [a])],
    # A+: Triple insertion
    [('A+', ['A+'], order) for order in all_ordered([x, y], [a, b, c])],
    # A+ -> W
    [(W, ['A+'], order) for order in all_ordered([x, y, b, c])],

    # B+: Base
    [('B+', e, order) for order in all_ordered([b])],
    # B+: Single insertion (a)
    [('B+', [W], order) for order in all_ordered([x, y], [b])],
    # B+: Triple insertion
    [('B+', ['B+'], order) for order in all_ordered([x, y], [a, b, c])],
    # B+ -> W
    [(W, ['B+'], order) for order in all_ordered([a, x, y, c])],

    # C+: Base
    [('C+', e, order) for order in all_ordered([c])],
    # C+: Single insertion (a)
    [('C+', [W], order) for order in all_ordered([x, y], [c])],
    # C+: Triple insertion
    [('C+', ['C+'], order) for order in all_ordered([x, y], [a, b, c])],
    # C+ -> W
    [(W, ['C+'], order) for order in all_ordered([a, b, x, y])],

    #
    # Combinations
    #

    # A- /\ C- => W
    [(W, ['A-', 'C-'], order) for order in all_ordered([a, x, y], [z, w, c])],

    # A+ /\ A- => W
    [(W, ['A+', 'A-'], order) for order in all_ordered([x, y, z, w])],

    # C- /\ C+ => W
    [(W, ['C-', 'C+'], order) for order in all_ordered([x, y, z, w])],

    # A+ /\ B+ => C-
    [('C-', ['A+', 'B+'], order) for order in all_ordered([x, y, z, w])],

    # B+ /\ C+ => A-
    [('A-', ['B+', 'C+'], order) for order in all_ordered([x, y, z, w])],

])


#
# Old grammar: does not scale...
#
A, A_, B, B_, C, C_ = 'A', 'A-', 'B', 'B-', 'C', 'C-'
AB, AC, BA, CA, BC, CB, AA, BB, CC = 'AB', 'AC', 'BA', 'CA', 'BC', 'CB', 'AA', 'BB', 'CC'
A_B_, A_C_, B_A_, C_A_, B_C_, C_B_, A_A_, B_B_, C_C_ = 'A-B-', 'A-C-', 'B-A-', 'C-A-', 'B-C-', 'C-B-', 'A-A-', 'B-B-', 'C-C-'
AC_, C_A, A_A, AA_, CC_, CA_, A_C, BA_, C_B, B_C, AB_, BB_, BC_ = 'AC-', 'C-A', 'A-A', 'AA-', 'CC-', 'CA-', 'A-C', 'BA-', 'C-B', 'B-C', 'AB-', 'BB_', 'BC_'
all_singles = [A, A_, B, B_, C, C_]
all_doubles = [AA, AA_, AB, AB_, AC, AC_, BA_, BB, BB_, BC, BC_, CC, CC_, A_A_, A_B_, A_C_, B_B_, B_C_, C_C_]
all_pairs = [(k, l) for k in all_singles for l in all_singles]


g1 = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W BASE
    (W, e, [[a, b, c], e]),
    (W, e, [[a, b], [c]]),
    (W, e, [[a], [b, c]]),
    # W PERMUTATIONS
    [(W, [W, W], s) for s in std_xyzw],
    # W TRIPLE INSERTION (BASE)
    # (W, [W], [[a, x, b, y, c], e]),
    # (W, [W], [[a, x, b, y], [c]]),
    (W, [W], [[a, x, b], [y, c]]),
    # (W, [W], [[a, b, x], [y, c]]),
    # (W, [W], [[a, x], [b, y, c]]),
    # (W, [W], [[a], [x, b, y, c]]),
    # W TRIPLE INSERTION (COMB)
    (W, [W, W], [[a, x, b], [z, c, y, w]]),
    (W, [W, W], [[a, x, b], [z, c, w, y, ]]),
    (W, [W, W], [[x, z, a, y, b], [w, c]]),
    (W, [W, W], [[x, z, a, w, b], [y, c]]),
    # A+, B+, C+
    [[
        (l.upper(), e, [[l], e]),
        (l.upper(), [W], [[l, x], [y]]),
        (l.upper(), [W], [[x, l], [y]]),
        (l.upper(), [W], [[x], [y, l]]),
    ] for l in "abc"],
    # NEGATIVES (BASE)
    (C_, [A, B], [[x, y], [z, w]]),
    (A_, [B, C], [[x, y], [z, w]]),
    # (B_, [A, C], [[x, y], [z, w]]),
    # NEGATIVES (COMB)
    [[
        (W, [l, r], [[x, y, z, w], e]),
        (W, [l, r], [[x, y, z], [w]]),
        (W, [l, r], [[x, y], [z, w]]),
        # (W, [l, r], [[x],          [y, z, w]]),
    ] for l, r in [(C_, C), (A, A_)]],
    # DOUBLES (INVERSE)
    # [(k + l, [l + k], [[x], [y]]) for k, l in all_pairs],
    # DOUBLES (BASE)
    [(k + l, [k, l], s) for k, l in all_pairs for s in std_xyzw],
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
    # AB_
    (AB_, [AB_, AA_], std_abc),
    (BB_, [AB_, BA_], std_abc),
    (B_B_, [AB_, BB_], std_abc),
    (B_, [AB_, BC], std_abc),
    (B_C, [AB_, CA_], std_abc),
    (AB_, [AB_, CC_], std_abc),
    (C, [AB_, A_A_], std_abc),
    (B_B_, [AB_, AB_], std_abc),
    (B_C_, [AB_, A_C_], std_abc),
    # BB
    (A_A_, [BB, CC], std_abc),
    # AC
    [(c, [AC, r], std_abc)
     for r, c in [
         (AA_, AC), (BA_, BC), (BB_, AC), (BC, C), (CA_, CC), (CC_, B_),
         (A_A_, CA_), (A_C_, CC_), (B_C_, AB_),
     ]],
    # AC_
    [(c, [AC_, r], std_abc)
     for r, c in [
         (AA_, C_A), (AC, AA), (BA_, C_B), (BB_, C_A), (BC, C_), (CA_, W),
         (B_C, AB_), (CC, B_), (CC_, AC_), (A_A_, C_A_), (A_B_, A), (A_C_, C_C_),
     ]],
])
