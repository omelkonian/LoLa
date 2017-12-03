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
    return [(perm[:n1 + 1], perm[n1 + 1:])
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

    # B- SPECIAL!.
    # B-: Base
    ('B-', e, [[a], [c]]),
    # all_ordered_rules('B-', e, [a, c]),
    ('B-', [W], [[a, x], [y, c]]),
    # B- -> W
    all_ordered_rules(W, ['B-'], [x, b, y]),
    # B-, W -> B-
    all_constrained_rules('B-', ['B-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),

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

    # ======================
    # Meta-meta rules
    # ======================

    # General 3-ins
    [[(K, [K], order) for order in all_ordered([x, y], [a, b, c])]
     for K in all_states if K != 'B-'],
    # General 3-ins (2x)
    all_ordered_rules(W, [W, W], [x, y], [z, w], [a, b, c], x=z, y=w),
    # [[(W, [K, L], order) for order in all_ordered([x, y, z, w], [a, b, c])]
    #  for K, L in [('C-', 'C+'), ('A+', 'A-')]],
    # TODO UNSOUND!!!
    # [[(W, [K, L], order) for order in all_ordered([x, y, z, w], [a, b, c])]
    #  for K, L in [(W, W), ('C-', 'C+'), ('A+', 'A-')]],

    # ======================
    # Meta-rule combinations
    # ======================

    # all_ordered_rules(W, ['A-', 'C-'], [a, x, y], [z, w, c]),

    # A+
    all_ordered_rules('C-', ['A+', 'B+'], [x, y, z, w]),
    # all_ordered_rules('B-', ['A+', 'C+'], [x, y], [z, w]),
    all_ordered_rules(W, ['A+', 'A-'], [x, y, z, w]),
    # B+
    all_ordered_rules('A-', ['B+', 'C+'], [x, y, z, w]),
    # C+
    # A-
    # B-
    all_ordered_rules('C+', ['B-', 'A-'], [x, y, z, w]),
    all_ordered_rules('C+', ['B-', 'A-'], [x, z, w, y]),
    # C-
    all_ordered_rules(W, ['C-', 'C+'], [x, y, z, w]),
    all_ordered_rules('B+', ['C-', 'A-'], [x, y, z, w]),
    # all_ordered_rules('A+', ['C-', 'B-'], [x, y, z, w]),

    # ======================
    # Refined non-terminals
    # ======================

    # lA-: Base
    ('lA-', e, [[b, c], e]),
    # lA-: Double insertion (b, c)
    all_constrained_rules('lA-', [W], left=[b, c], orders=[[x, y], [b, c]]),
    # lA-, W -> A-
    all_constrained_rules('lA-', ['lA-', W], left=[x], orders=[[x, y], [z, w]]),
    # lA- -> W
    # all_constrained_rules(W, ['lA-'], left=[a, x, y], orders=[[a, x], [y]]),  # TODO set change
    all_ordered_rules(W, ['lA-'], [a, x, y]),
    # lA- -> A-
    all_ordered_rules('A-', ['lA-'], [x, y]),

    # rA-: Base
    ('rA-', e, [e, [b, c]]),
    # rA-: Double insertion (b, c)
    all_constrained_rules('rA-', [W], right=[b, c], orders=[[x, y], [b, c]]),
    # rA-, W -> A-
    all_constrained_rules('rA-', ['rA-', W], right=[y], orders=[[x, y], [z, w]]),
    # rA- -> W
    # all_ordered_rules(W, ['rA-'], [a, y], [x, y]),
    all_constrained_rules(W, ['rA-'], left=[a], orders=[[x, a, y]]),
    # all_constrained_rules(W, ['rA-'], left=[a], orders=[[a, x, y]]), # TODO set change
    # rA- -> A-
    all_ordered_rules('A-', ['rA-'], [x, y]),
], topdown=True, filtered=True)
all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
