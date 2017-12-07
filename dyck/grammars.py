from pprint import pprint

from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c = 'a', 'b', 'c'
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)
S, W, e = 'S', 'W', []
tuple_to_char = {
    (0, 0): 'x',
    (0, 1): 'y',
    (1, 0): 'z',
    (1, 1): 'w'
}

def filter_nonempty(rules):
    return [(lhs, rhs, orders) for lhs, rhs, orders in rules if orders[0] != []]


def symbols_from_orders(orders):
    return ''.join(list(set(''.join(orders))))


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


def ordered_permutations(orders, **symmetries):
    return remove_symmetries([
            ''.join(s)
            for s in permutations(symbols_from_orders(orders))
            if is_ordered(s, orders)], **symmetries)


def ordered_pairs(orders, **symmetries):
    return [(perm[:n1+1], perm[n1+1:])
            for n1 in range(0, len(symbols_from_orders(orders)))
            for perm in ordered_permutations(orders, **symmetries)]


def post_process(orders, **symmetries):
    return [(post_process_single(l), post_process_single(r))
            for l, r in ordered_pairs(orders, **symmetries)]


def post_process_single(order):
    return [globals()[c] for c in order]


def pre_process(symbols):
    return [pre_process_single(s) for s in symbols]


def pre_process_single(symbols):
    return ''.join(
        [tuple_to_char.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(*orders, **symmetries):
    return post_process(pre_process(orders), **symmetries)


def all_ordered_rules(lhs, rhs, *orders, **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(*orders, **symmetries)]


def all_constrained_rules(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(*orders, **symmetries)
            if all(map(lambda l: l in order[0], left))
            if all(map(lambda r: r in order[1], right))]


def remove_symmetries(words, **symmetries):
    ret = []
    for w in words:
        if [translate(w, **symmetries)] not in ret:
            ret += [[w]]
    return sum(ret, [])


def translate(word, **symmetries):
    symmetries = {k: (tuple_to_char[v] if isinstance(v, tuple) else v) for k, v in symmetries.items()}
    symmetries = dict(symmetries, **{v: k for k, v in symmetries.items()})  # add inverse translations
    return ''.join([symmetries.get(c, c) for c in word])


# pprint(all_constrained_rules('rA-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]))

#
# Grammar
#
all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
g2 = Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # ======================
    # Meta-rules
    # ======================

    # W: Base
    all_ordered_rules(W, e, [a, b, c]),
    # W: Permutation
    all_ordered_rules(W, [W], [x, y]),
    # W: Concatenation
    all_ordered_rules(W, [W, W], [x, y], [z, w], x=z, y=w),

    # A-: Base
    all_ordered_rules('A-', e, [b, c]),
    # A-: Double insertion (b, c)
    all_ordered_rules('A-', [W], [x, y], [b, c]),
    # A- -> W
    all_ordered_rules(W, ['A-'], [a, x, y]),
    # A-, W -> A-
    all_ordered_rules('A-', ['A-', W], [x, y], [z, w]),

    # B-: Base
    all_ordered_rules('B-', e, [a], [c]),
    # B-: Double insertion (a, c)
    all_ordered_rules('B-', [W], [x, y], [a], [c]),
    # B-, W -> B-
    all_ordered_rules('B-', ['B-', W], [x, y], [z, w]),

    # C-: Base
    all_ordered_rules('C-', e, [a, b]),
    # C-: Double insertion (a, b)
    all_ordered_rules('C-', [W], [x, y], [a, b]),
    # C- -> W
    all_ordered_rules(W, ['C-'], [x, y, c]),
    # C-, W -> C-
    all_ordered_rules('C-', ['C-', W], [x, y], [z, w]),

    # A+: Base
    ('A+', e, [[a], e]),
    # A+: Single insertion (a)
    all_ordered_rules('A+', [W], [x, y], [a]),
    # A+ -> W
    all_ordered_rules(W, ['A+'], [x, y, b, c]),
    # A+, W -> A+
    all_ordered_rules('A+', ['A+', W], [x, y], [z, w]),

    # B+: Base
    ('B+', e, [[b], e]),
    # ('B+', e, [e, [b]]),
    # B+: Single insertion (b)
    all_ordered_rules('B+', [W], [x, y], [b]),
    # B+ -> W
    all_ordered_rules(W, ['B+'], [a, x, y, c]),
    # B+, W -> B+
    all_ordered_rules('B+', ['B+', W], [x, y], [z, w]),

    # C+: Base
    ('C+', e, [[c], e]),
    # C+: Single insertion (b)
    all_ordered_rules('C+', [W], [x, y], [c]),
    # C+ -> W
    all_ordered_rules(W, ['C+'], [a, b, x, y]),
    # C+, W -> C+
    all_ordered_rules('C+', ['C+', W], [x, y], [z, w]),

    # ======================
    # Meta-meta rules
    # ======================

    # General 3-ins
    [[(K, [K], order) for order in all_ordered([x, y], [a, b, c])]
     for K in all_states],

    # ======================
    # Meta-rule combinations
    # ======================

    # all_ordered_rules(W, ['A-', 'C-'], [a, x, y], [z, w, c]),

    # A+
    all_ordered_rules('C-', ['A+', 'B+'], [x, y, z, w]),
    all_ordered_rules('B-', ['A+', 'C+'], [x, y], [z, w]),
    all_ordered_rules(W, ['A+', 'A-'], [x, y, z, w]),
    # B+
    all_ordered_rules('A-', ['B+', 'C+'], [x, y, z, w]),
    # C+
    # A-
    # B-
    all_ordered_rules('C+', ['B-', 'A-'], [x, y, z, w]),
    # C-
    all_ordered_rules(W, ['C-', 'C+'], [x, y, z, w]),
    all_ordered_rules('B+', ['C-', 'A-'], [x, y, z, w]),
    all_ordered_rules('A+', ['C-', 'B-'], [x, y, z, w]),
    # all_constrained_rules('lA+', ['C-', 'B-'], left=[z,w], orders=[[x, y, z, w]]),

    # ======================
    # Refined non-terminals
    # ======================

    # lA+: Base
    ('lA+', e, [[a], e]),
    # lA+: Single insertion (a)
    all_constrained_rules('lA+', [W], left=[a], orders=[[x, y], [a]]),
    # lA+, W -> lA+
    all_constrained_rules('lA+', ['lA+', W], left=[x], orders=[[x, y], [z, w]]),
    # lA+ -> W
    all_ordered_rules(W, ['lA+'], [x, y], [x, b, c]),
    # lA+: Fallback
    all_ordered_rules('A+', ['lA+'], [x, y]),
    # lA+: Co-Fallback
    ('lA+', ['A+'], [[x, y], e]),
    # lA+: 3-ins
    all_constrained_rules('lA+', ['lA+'], left=[x], orders=[[x, y], [a, b, c]]),

    # lB+: Base
    ('lB+', e, [[b], e]),
    # lB+: Single insertion (b)
    all_constrained_rules('lB+', [W], left=[b], orders=[[x, y], [b]]),
    # lB+, W -> lB+
    all_constrained_rules('lB+', ['lB+', W], left=[x], orders=[[x, y], [z, w]]),
    # lB+ -> W
    all_ordered_rules(W, ['lB+'], [x, y], [a, x, c]),
    # lB+: Fallback
    all_ordered_rules('B+', ['lB+'], [x, y]),
    # lB+: Co-Fallback
    ('lB+', ['B+'], [[x, y], e]),
    # lB+: 3-ins
    all_constrained_rules('lB+', ['lB+'], left=[x], orders=[[x, y], [a, b, c]]),

    # rC+: Base
    ('rC+', e, [e, [c]]),
    # rC+: Single insertion (c)
    all_constrained_rules('rC+', [W], right=[c], orders=[[x, y], [c]]),
    # rC+, W -> rC+
    all_constrained_rules('rC+', ['rC+', W], right=[y], orders=[[x, y], [z, w]]),
    # rC+ -> W
    all_constrained_rules(W, ['rC+'], left=[a], orders=[[x, y], [a, b, y]]), # TODO nonempty
    # rC+: Fallback
    all_ordered_rules('C+', ['rC+'], [x, y]),
    # rC+: Co-Fallback
    ('rC+', ['C+'], [e, [x, y]]),
    # rC+: 3-ins
    all_constrained_rules('rC+', ['rC+'], right=[y], orders=[[x, y], [a, b, c]]),

    # rA-: Base
    ('rA-', e, [e, [b, c]]),
    # rA-: Double insertion (b, c)
    all_constrained_rules('rA-', [W], right=[b, c], orders=[[x, y], [b, c]]),
    # rA-, W -> rA-
    all_constrained_rules('rA-', ['rA-', W], right=[y], orders=[[x, y], [z, w]]),
    # rA- -> W
    all_constrained_rules(W, ['rA-'], left=[a], orders=[[x, a, y]]),  #  TODO non-empty
    # rA-: Fallback
    all_ordered_rules('A-', ['rA-'], [x, y]),
    # rA-: Co-Fallback
    ('rA-', ['A-'], [e, [x, y]]),
    # rA-: 3-ins
    all_constrained_rules('rA-', ['rA-'], right=[y], orders=[[x, y], [a, b, c]]),

    # lrB-: Base
    ('lrB-', e, [[a], [c]]),
    # lrB-: Double insertion (a, c)
    all_constrained_rules('lrB-', [W], left=[a], right=[c], orders=[[x, y], [a, c]]),
    # lrB-, W -> lrB-
    all_constrained_rules('lrB-', ['lrB-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),
    # lrB- -> W
    all_ordered_rules(W, ['lrB-'], [x, b, y]),
    # lrB-: Fallback
    all_ordered_rules('B-', ['lrB-'], [x, y]),
    # lrB-: 3-ins
    all_constrained_rules('lrB-', ['lrB-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),

    # lC-: Base
    ('lC-', e, [[a, b], e]),
    # lC-: Double insertion (a, b)
    all_constrained_rules('lC-', [W], left=[a, b], orders=[[x, y], [a, b]]),
    # lC-, W -> lC-
    all_constrained_rules('lC-', ['lC-', W], left=[x], orders=[[x, y], [z, w]]),
    # lC- -> W
    all_ordered_rules(W, ['lC-'], [x, c, y]),
    # lC-: Fallback
    all_ordered_rules('C-', ['lC-'], [x, y]),
    # lC-: Co-Fallback
    ('lC-', ['C-'], [[x, y], e]),
    # lC-: 3-ins
    all_constrained_rules('lC-', ['lC-'], left=[x], orders=[[x, y], [a, b, c]]),

    # ==================
    # lA+
    # ==================
    # lA+
    # lB+
    all_constrained_rules('lC-', ['lA+', 'lB+'], left=[x, z], orders=[[x, y], [z, w], [x, z]]),
    all_ordered_rules('C-', ['lA+', 'lB+'], [x, y], [z, w], [x, z]), # TODO minimize
    # rC+
    all_constrained_rules('lrB-', ['lA+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w], [x, w]]),
    all_ordered_rules('B-', ['lA+', 'rC+'], [x, y], [z, w]),
    # rA-
    all_constrained_rules(W, ['lA+', 'rA-'], left=[x], orders=[[x, y], [z, w], [x, w]]), # TODO nonempty
    # lrB-
    # lC-
    # A+
    # B+
    all_constrained_rules('lC-', ['lA+', 'B+'], left=[x, z, w], orders=[[x, y], [z, w], [x, z]]),
    all_ordered_rules('C-', ['lA+', 'B+'], [x, y], [z, w], [x, z]),
    # C+
    all_constrained_rules('lrB-', ['lA+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),
    all_ordered_rules('B-', ['lA+', 'C+'], [x, y], [z, w]),
    # A-
    all_ordered_rules(W, ['lA+', 'A-'], [x, y], [z, w], [x, z]),
    # B-
    # C-

    # ==================
    # lB+
    # ==================
    # lB+
    # rC+
    all_constrained_rules('rA-', ['lB+', 'rC+'], right=[x, w], orders=[[x, y], [z, w], [x, w]]),
    all_ordered_rules('A-', ['lB+', 'rC+'], [x, y], [z, w], [x, w]),
    # rA-
    # lrB-
    all_ordered_rules(W, ['lB+', 'lrB-'], [x, y], [z, x, w]),
    # lC-
    # A+
    all_constrained_rules('lC-', ['lB+', 'A+'], left=[z, w, x], orders=[[x, y], [z, w, x]]),
    all_ordered_rules('C-', ['lB+', 'A+'], [x, y], [z, w, x]),
    # B+
    # C+
    # all_constrained_rules('rA-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]), # TODO nonempty
    ('rA-', ['lB+', 'C+'], [e, [x, y, z, w]]),
    ('rA-', ['lB+', 'C+'], [e, [x, z, y, w]]),
    ('rA-', ['lB+', 'C+'], [e, [x, z, w, y]]),
    ('rA-', ['lB+', 'C+'], [e, [x, z, y, w]]),
    all_ordered_rules('A-', ['lB+', 'C+'], [x, y], [x, z, w]),
    # A-
    # B-
    # C-

    # ==================
    # rC+
    # ==================
    # rC+
    # rA-
    # lrB-
    # lC-
    all_constrained_rules(W, ['rC+', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]), # TODO nonempty
    # A+
    all_constrained_rules('lrB-', ['rC+', 'A+'], left=[z, w], right=[y], orders=[[x, y], [z, w]]),
    all_ordered_rules('B-', ['rC+', 'A+'], [x, y], [z, w]),
    # B+
    all_constrained_rules('rA-', ['rC+', 'B+'], right=[z, w, y], orders=[[x, y], [z, w, y]]),
    all_ordered_rules('A-', ['rC+', 'B+'], [x, y], [z, w, y]),
    # C+
    # A-
    # B-
    # C-
    # all_ordered_rules(W, ['rC+', 'C-'], [x, y], [z, w, y]) # TODO nonempty
    all_constrained_rules(W, ['rC+', 'C-'], left=[x, z], orders=[[x, z, w, y]]),
    all_ordered_rules(W, ['rC+', 'C-'], [z, w, x, y]),
    all_ordered_rules(W, ['rC+', 'C-'], [z, x, w, y]),

    # ==================
    # rA-
    # ==================
    # rA-
    # lrB-
    all_constrained_rules('rC+', ['rA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, y]]),
    all_ordered_rules('C+', ['rA-', 'A+'], [x, y], [z, w], [z, y]),
    # lC-
    all_constrained_rules('lB+', ['rA-', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]),
    all_constrained_rules('lB+', ['rA-', 'lC-'], left=[y], orders=[[x, y], [z, w], [z, y]]),
    all_ordered_rules('B+', ['rA-', 'lC-'], [x, y], [z, w], [z, y]),
    # A+
    all_constrained_rules(W, ['rA-', 'A+'], left=[z], orders=[[x, y], [z, w], [z, w, y]]), # TODO nonempty
    # B+
    # C+
    # A-
    # B-
    all_constrained_rules('rC+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    all_ordered_rules('C+', ['rA-', 'B-'], [x, y], [z, w, y]),
    # C-
    all_constrained_rules('lB+', ['rA-', 'C-'], left=[z, w], orders=[[x, y], [z, w, y]]),
    all_constrained_rules('lB+', ['rA-', 'C-'], left=[y], orders=[[x, y], [z, w, y]]),
    all_ordered_rules('B+', ['rA-', 'C-'], [x, y], [z, w, y]),

    # ==================
    # lrB-
    # ==================
    # lrB-
    # lC-
    all_constrained_rules('lA+', ['lrB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    all_ordered_rules('A+', ['lrB-', 'lC-'], [x, y], [z, w], [z, y]),
    # A+
    # B+
    all_ordered_rules(W, ['lrB-', 'B+'], [x, z, w, y]),
    # C+
    # A-
    all_constrained_rules('rC+', ['lrB-', 'A-'], right=[y], orders=[[x, y], [x, z, w]]),
    all_constrained_rules('rC+', ['lrB-', 'A-'], right=[z, w], orders=[[x, z, w, y]]), # TODO spurious
    all_ordered_rules('C+', ['lrB-', 'A-'], [x, y], [x, z, w]),
    # B-
    # C-
    all_constrained_rules('lA+', ['lrB-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    all_constrained_rules('lA+', ['lrB-', 'C-'], left=[z, w], orders=[[x, z, w, y]]), # TODO spurious
    all_ordered_rules('A+', ['lrB-', 'C-'], [x, y], [z, w, y]),

    # ==================
    # lC-
    # ==================
    # lC-
    # A+
    # C+
    all_ordered_rules(W, ['lC-', 'C+'], [x, y], [x, z, w]),
    # A-
    all_constrained_rules('lB+', ['lC-', 'A-'], left=[x], orders=[[x, y], [x, z, w]]),
    all_constrained_rules('lB+', ['lC-', 'A-'], left=[z, w], orders=[[x, y], [x, z, w]]), # TODO spurious
    all_ordered_rules('B+', ['lC-', 'A-'], [x, y], [x, z, w]),
    # B-
    all_constrained_rules('lA+', ['lC-', 'B-'], left=[z, w], orders=[[x, y], [x, z, w]]),
    all_ordered_rules('A+', ['lC-', 'B-'], [x, y], [x, z, w]),
    # C-

], topdown=True, filtered=True)
