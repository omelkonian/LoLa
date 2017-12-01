from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c = 'a', 'b', 'c'
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)
S, W, e = 'S', 'W', []


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
    return ''.join(
        [{(0, 0): 'x', (0, 1): 'y', (1, 0): 'z', (1, 1): 'w'}.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(*orders):
    return post_process(pre_process(orders))


def all_ordered_rules(lhs, rhs, *orders):
    return [(lhs, rhs, order) for order in all_ordered(*orders)]

# TODO consider symmetric orders
# def remove_symmetrics(words):
#     ret = []
#     for w in words:
#         from copy import deepcopy
#         w2 = deepcopy(w).replace('x', '%x%').replace('y', '%y%').replace('z', 'x').replace('w', 'y').replace('%x%', 'z').replace('%y%', 'w')
#         if w2 not in ret:
#             ret += [[w]]
#     ret = sum(ret, [])
#     return ret

#
# Grammar
#
all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
g2 = Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # =============
    # Meta-rules
    # =============

    # W: Base
    all_ordered_rules(W, e, [a, b, c]),
    # W: Concatenation
    all_ordered_rules(W, [W, W], [x, y], [z, w]),

    # A-: Base
    all_ordered_rules('A-', e, [b, c]),
    # A-: Double insertion (b, c)
    all_ordered_rules('A-', [W], [x, y], [b, c]),
    # A- -> W
    all_ordered_rules(W, ['A-'], [a, x, y]),
    # A-, W -> A-
    all_ordered_rules('A-', ['A-', W], [x, y], [z, w]),

    # B-: Base
    all_ordered_rules('B-', e, [a, c]),
    # B-: Double insertion (a, c)
    all_ordered_rules('B-', [W], [x, y], [a, c]),
    # B- -> W
    all_ordered_rules(W, ['B-'], [a, x, y]),
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
    all_ordered_rules('A+', e, [a]),
    # A+: Single insertion (a)
    all_ordered_rules('A+', [W], [x, y], [a]),
    # A+ -> W
    all_ordered_rules(W, ['A+'], [x, y, b, c]),
    # A+, W -> A+
    all_ordered_rules('A+', ['A+', W], [x, y], [z, w]),

    # B+: Base
    all_ordered_rules('B+', e, [b]),
    # B+: Single insertion (a)
    all_ordered_rules('B+', [W], [x, y], [b]),
    # B+ -> W
    all_ordered_rules(W, ['B+'], [a, x, y, c]),
    # B+, W -> B+
    all_ordered_rules('B+', ['B+', W], [x, y], [z, w]),

    # C+: Base
    all_ordered_rules('C+', e, [c]),
    # C+: Single insertion (a)
    all_ordered_rules('C+', [W], [x, y], [c]),
    # C+ -> W
    all_ordered_rules(W, ['C+'], [a, b, x, y]),
    # C+, W -> C+
    all_ordered_rules('C+', ['C+', W], [x, y], [z, w]),

    # =============
    # Meta-meta rules
    # =============

    # General 3-ins
    [[(K, [K], order) for order in all_ordered([x, y], [a, b, c])]
     for K in all_states],
    # General 3-ins (2x)
    all_ordered_rules(W, [W, W], [x, y], [z, w], [a, b, c]),
    [[(W, [K, L], order) for order in all_ordered([x, y, z, w], [a, b, c])]
     for K, L in [('C-', 'C+'), ('A+', 'A-')]],
    # TODO UNSOUND!!!
    # [[(W, [K, L], order) for order in all_ordered([x, y, z, w], [a, b, c])]
    #  for K, L in [(W, W), ('C-', 'C+'), ('A+', 'A-')]],

    # =============
    # Meta-rule combinations
    # =============

    all_ordered_rules(W, ['A-', 'C-'], [a, x, y], [z, w, c]),

    # A+
    all_ordered_rules('C-', ['A+', 'B+'], [x, y, z, w]),
    all_ordered_rules('B-', ['A+', 'C+'], [x, y, z, w]),
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
])
