from pprint import pprint
from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c = 'a', 'b', 'c'
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)
k, l, m, n = (2, 0), (2, 1), (3, 0), (3, 1)
S, W, e = 'S', 'W', []
tuple_to_char = {
    (0, 0): 'x',
    (0, 1): 'y',
    (1, 0): 'z',
    (1, 1): 'w',
    (2, 0): 'k',
    (2, 1): 'l',
    (3, 0): 'm',
    (3, 1): 'n',
}


def rule(lhs, rhs):
    assert len(rhs) == 1
    return lhs, rhs, [[x], [y]]


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
    # TODO curate
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


def all_non_constrained_rules(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    allOrd = all_ordered(*orders, **symmetries)
    allCon = [o for o in allOrd
              if all(map(lambda l: l in o[0], left))
              if all(map(lambda r: r in o[1], right))]
    return [(lhs, rhs, o) for o in allOrd if o not in allCon]


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


#
# Grammar
#
all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']

# ======================
# Refined non-terminals
refinements = [
    # lA+: Base
    ('lA+', e, [[a], e]),
    # lA+: Fallback
    rule('A+', ['lA+']),
    # lA+: Co-Fallback
    ('lA+', ['A+'], [[x, y], e]),
    # lA+: 3-ins
    all_constrained_rules('lA+', ['lA+'], left=[x], orders=[[x, y], [a, b, c]]),

    # lB+: Base
    ('lB+', e, [[b], e]),
    # lB+: Fallback
    rule('B+', ['lB+']),
    # lB+: Co-Fallback
    ('lB+', ['B+'], [[x, y], e]),
    # lB+: 3-ins
    all_constrained_rules('lB+', ['lB+'], left=[x], orders=[[x, y], [a, b, c]]),

    # rC+: Base
    ('rC+', e, [e, [c]]),
    # rC+: Fallback
    rule('C+', ['rC+']),
    # rC+: Co-Fallback
    ('rC+', ['C+'], [e, [x, y]]),
    # rC+: 3-ins
    all_constrained_rules('rC+', ['rC+'], right=[y], orders=[[x, y], [a, b, c]]),

    # rA-: Base
    ('rA-', e, [e, [b, c]]),
    # rA-: Fallback
    rule('A-', ['rA-']),
    # rA-: Co-Fallback
    ('rA-', ['A-'], [e, [x, y]]),
    # rA-: 3-ins
    all_constrained_rules('rA-', ['rA-'], right=[y], orders=[[x, y], [a, b, c]]),

    # rB-: Base
    all_constrained_rules('rB-', e, right=[a, c], orders=[[a], [c]]),
    # rB-: Fallback
    rule('B-', ['rB-']),
    # rB-: 3-ins
    all_constrained_rules('rB-', ['rB-'], right=[y], orders=[[x, y], [a, b, c]]),

    # lrB-: Base
    ('lrB-', e, [[a], [c]]),
    # lrB-: Fallback
    rule('B-', ['lrB-']),
    # lrB-: 3-ins
    all_constrained_rules('lrB-', ['lrB-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),

    # lC-: Base
    ('lC-', e, [[a, b], e]),
    # lC-: Fallback
    rule('C-', ['lC-']),
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
    all_non_constrained_rules('C-', ['lA+', 'lB+'], left=[x, z], orders=[[x, y], [z, w], [x, z]]),
    # rC+
    all_constrained_rules('lrB-', ['lA+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w], [x, w]]),
    all_non_constrained_rules('B-', ['lA+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w], [x, w]]),
    # rA-
    all_constrained_rules(W, ['lA+', 'rA-'], left=[x], orders=[[x, y], [z, w], [x, w]]), # TODO nonempty
    # lrB-
    # lC-
    # A+
    # B+
    all_constrained_rules('lC-', ['lA+', 'B+'], left=[x, z, w], orders=[[x, y], [z, w], [x, z]]),
    all_non_constrained_rules('C-', ['lA+', 'B+'], left=[x, z, w], orders=[[x, y], [z, w], [x, z]]),
    # C+
    all_constrained_rules('lrB-', ['lA+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),
    all_non_constrained_rules('B-', ['lA+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),
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
    all_non_constrained_rules('A-', ['lB+', 'rC+'], right=[x, w], orders=[[x, y], [z, w], [x, w]]),
    # rA-
    # lrB-
    all_ordered_rules(W, ['lB+', 'lrB-'], [x, y], [z, x, w]),
    # lC-
    # A+
    all_constrained_rules('lC-', ['lB+', 'A+'], left=[z, w, x], orders=[[x, y], [z, w, x]]),
    all_non_constrained_rules('C-', ['lB+', 'A+'], left=[z, w, x], orders=[[x, y], [z, w, x]]),
    # B+
    # C+
    all_constrained_rules('rA-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]),
    all_non_constrained_rules('A-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]),
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
    all_ordered_rules(W, ['rC+', 'lC-'], [x, y], [z, w], [z, y]),
    # A+
    all_constrained_rules('lrB-', ['rC+', 'A+'], left=[z, w], right=[y], orders=[[x, y], [z, w]]),
    all_non_constrained_rules('B-', ['rC+', 'A+'], left=[z, w], right=[y], orders=[[x, y], [z, w]]),
    # B+
    all_constrained_rules('rA-', ['rC+', 'B+'], right=[z, w, y], orders=[[x, y], [z, w, y]]),
    all_non_constrained_rules('A-', ['rC+', 'B+'], right=[z, w, y], orders=[[x, y], [z, w, y]]),
    # C+
    # A-
    # B-
    # C-
    all_ordered_rules(W, ['rC+', 'C-'], [x, y], [z, w, y]),

    # ==================
    # rA-
    # ==================
    # rA-
    # lrB-
    all_constrained_rules('rC+', ['rA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, y]]),
    all_non_constrained_rules('C+', ['rA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, y]]),
    # lC-
    all_constrained_rules('lB+', ['rA-', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]),
    all_non_constrained_rules('B+', ['rA-', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]),
    # A+
    all_ordered_rules(W, ['rA-', 'A+'], [x, y], [z, w], [z, w, y]),
    # B+
    # C+
    # A-
    # B-
    all_constrained_rules('rC+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    all_non_constrained_rules('C+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    # C-
    all_constrained_rules('lB+', ['rA-', 'C-'], left=[z, w], orders=[[x, y], [z, w, y]]),
    all_non_constrained_rules('B+', ['rA-', 'C-'], left=[z, w], orders=[[x, y], [z, w, y]]),

    # ==================
    # lrB-
    # ==================
    # lrB-
    # lC-
    all_constrained_rules('lA+', ['lrB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    all_non_constrained_rules('A+', ['lrB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    # A+
    # B+
    all_ordered_rules(W, ['lrB-', 'B+'], [x, z, w, y]),
    # C+
    # A-
    all_constrained_rules('rC+', ['lrB-', 'A-'], right=[y], orders=[[x, y], [x, z, w]]),
    all_non_constrained_rules('C+', ['lrB-', 'A-'], right=[y], orders=[[x, y], [x, z, w]]),
    # B-
    # C-
    all_constrained_rules('lA+', ['lrB-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    all_non_constrained_rules('A+', ['lrB-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),

    # C-
    # ==================
    # lC-
    # ==================
    # lC-
    # A+
    # C+
    all_ordered_rules(W, ['lC-', 'C+'], [x, y], [x, z, w]),
    # A-
    all_constrained_rules('lB+', ['lC-', 'A-'], left=[x], orders=[[x, y], [x, z, w]]),
    all_non_constrained_rules('B+', ['lC-', 'A-'], left=[x], orders=[[x, y], [x, z, w]]),
    # B-
    all_constrained_rules('lA+', ['lC-', 'B-'], left=[z, w], orders=[[x, y], [x, z, w]]),
    all_non_constrained_rules('A+', ['lC-', 'B-'], left=[z, w], orders=[[x, y], [x, z, w]]),
    # C-

    # AD-HOC
    all_constrained_rules('rC+', ['rB-', 'A-'], right=[y], orders=[[x, y], [y, z, w]]),
]
# ======================

g = lambda initial_symbol: Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # ======================
    # Debugging
    # ======================
    [('_' + k, [k], [[x, y]]) for k in all_states + ['lA+', 'lB+', 'rC+', 'rA-', 'lrB-', 'lC-']],
    [('$_' + k, [k], [[x, '$', y]]) for k in all_states + ['lA+', 'lB+', 'rC+', 'rA-', 'lrB-', 'lC-']],

    # ======================
    # Meta-rules
    # ======================

    # W: Concatenation
    all_ordered_rules(W, [W, W], [x, y], [z, w], x=z, y=w),

    # A+: Base
    ('A+', e, [e, [a]]),
    # B+: Base
    ('B+', e, [e, [b]]),
    # C+: Base
    ('C+', e, [[c], e]),

    # ======================
    # Meta-meta rules
    # ======================

    # ALL 3-ins
    all_ordered_rules(W, [W], [x, y], [a, b, c]),
    # A+
    all_constrained_rules('lA+', ['A+'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('A+', ['A+'], orders=[[x, y], [a, b, c]], left=[x, y]),
    # B+
    all_constrained_rules('lB+', ['B+'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('B+', ['B+'], orders=[[x, y], [a, b, c]], left=[x, y]),
    # C+
    all_constrained_rules('rC+', ['C+'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('C+', ['C+'], orders=[[x, y], [a, b, c]], right=[x, y]),
    # A-
    all_constrained_rules('rA-', ['A-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('A-', ['A-'], orders=[[x, y], [a, b, c]], right=[x, y]),
    # B-
    all_constrained_rules('rB-', ['B-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('B-', ['B-'], orders=[[x, y], [a, b, c]], right=[x, y]),
    # C-
    all_constrained_rules('lC-', ['C-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_non_constrained_rules('C-', ['C-'], orders=[[x, y], [a, b, c]], left=[x, y]),

    # ======================
    # Meta-rule combinations
    # ======================

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
] + refinements, topdown=True, filtered=True, initial_symbol=initial_symbol)

