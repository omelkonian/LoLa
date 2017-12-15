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
    return [(perm[:n1], perm[n1:])
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


def all_c(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(*orders, **symmetries)
            if all(map(lambda l: l in order[0], left))
            if all(map(lambda r: r in order[1], right))]


def all_nc(lhs, rhs, left=[], right=[], orders=[], **symmetries):
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
refinements = [
    # lA+: Base
    ('lA+', e, [[a], e]),
    # lA+: Fallback
    rule('A+', ['lA+']),
    # lA+: Co-Fallback
    ('lA+', ['A+'], [[x, y], e]),
    # lA+: 3-ins
    all_c('lA+', ['lA+'], left=[x], orders=[[x, y], [a, b, c]]),
    all_c('lA+', ['lA+'], left=[a], orders=[[x, y], [x, b, c], [a]]),
    all_c('A+', ['lA+'], right=[a], orders=[[x, y], [x, b, c], [a]]),
    # lA+: W interaction
    all_c('lA+', ['lA+', W], left=[x], orders=[[x, y], [z, w]]),

    # lB+: Base
    ('lB+', e, [[b], e]),
    # lB+: Fallback
    rule('B+', ['lB+']),
    # lB+: Co-Fallback
    ('lB+', ['B+'], [[x, y], e]),
    # lB+: 3-ins
    all_c('lB+', ['lB+'], left=[x], orders=[[x, y], [a, b, c]]),
    all_c('lB+', ['lB+'], left=[b], orders=[[x, y], [a, x, c], [b]]),
    all_c('B+', ['lB+'], right=[b], orders=[[x, y], [a, x, c], [b]]),
    # lB+: W interaction
    all_c('lB+', ['lB+', W], left=[x], orders=[[x, y], [z, w]]),

    # rC+: Base
    ('rC+', e, [e, [c]]),
    # rC+: Fallback
    rule('C+', ['rC+']),
    # rC+: Co-Fallback
    ('rC+', ['C+'], [e, [x, y]]),
    # rC+: 3-ins
    all_c('rC+', ['rC+'], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('C+', ['rC+'], left=[c], orders=[[x, y], [a, b, y], [c]]),
    all_c('rC+', ['rC+'], right=[c], orders=[[x, y], [a, b, y], [c]]),
    # rC+: W interaction
    all_c('rC+', ['rC+', W], right=[y], orders=[[x, y], [z, w]]),

    # rA-: Base
    ('rA-', e, [e, [b, c]]),
    # rA-: Fallback
    rule('A-', ['rA-']),
    # rA-: Co-Fallback
    ('rA-', ['A-'], [e, [x, y]]),
    # rA-: 3-ins
    all_c('rA-', ['rA-'], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('A-', ['rA-'], left=[b, c], orders=[[x, y], [a, y], [b, c]]),
    all_c('rA-', ['rA-'], right=[b, c], orders=[[x, y], [a, y], [b, c]]),
    all_c('lrA-', ['rA-'], left=[b], right=[c], orders=[[x, y], [a, y], [b, c]]),
    # rA-: W interaction
    all_c('rA-', ['rA-', W], right=[y], orders=[[x, y], [z, w]]),

    # lrA-: Base
    ('lrA-', e, [[b], [c]]),
    # lrA-: Fallback
    rule('A-', ['lrA-']),
    # lrA-: 3-ins
    all_c('A-', ['lrA-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('rA-', ['lrA-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('lrA-', ['lrA-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),

    all_c('A-', ['lrA-'], left=[b, c], orders=[[a, x, y], [b, c]]),
    all_c('rA-', ['lrA-'], right=[b, c], orders=[[a, x, y], [b, c]]),
    all_c('lrA-', ['lrA-'], left=[b], right=[c], orders=[[a, x, y], [b, c]]),

    all_c('A-', ['lrA-'], left=[x, c], orders=[[x, y], [a, b, y], [x, c]]),
    all_c('rA-', ['lrA-'], right=[x, c], orders=[[x, y], [a, b, y], [x, c]]),
    all_c('lrA-', ['lrA-'], left=[x], right=[c], orders=[[x, y], [a, b, y], [x, c]]),

    all_c('A-', ['lrA-'], left=[b, y], orders=[[x, y], [a, x, c], [b, y]]),
    all_c('rA-', ['lrA-'], right=[b, y], orders=[[x, y], [a, x, c], [b, y]]),
    all_c('lrA-', ['lrA-'], left=[b], right=[y], orders=[[x, y], [a, x, c], [b, y]]),

    # lrA-: W interaction
    all_c('lrA-', ['lrA-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),

    # lB-: Base
    all_c('lB-', e, left=[a, c], orders=[[a], [c]]),
    # lB-: Fallback
    rule('B-', ['lB-']),
    # lB-: Co-Fallback
    ('lB-', ['B-'], [[x, y], e]),
    # lB-: 3-ins
    all_c('lB-', ['lB-'], left=[x], orders=[[x, y], [a, b, c]]),
    all_c('rB-', ['lB-'], right=[x], orders=[[x, y], [a, b, c]]),

    all_c('lB-', ['lB-'], left=[x, a], orders=[[x, y], [x, b, c], [a]]),
    all_c('rB-', ['lB-'], right=[x, a], orders=[[x, y], [x, b, c], [a]]),
    all_c('rlB-', ['lB-'], left=[x], right=[a], orders=[[x, y], [x, b, c], [a]]),
    all_c('lrB-', ['lB-'], left=[a], right=[x], orders=[[x, y], [x, b, c], [a]]),  # TODO EMERGENT!!!!!!!!

    all_c('lB-', ['lB-'], left=[c, x], orders=[[x, y], [a, b, x], [c]]),
    all_c('rB-', ['lB-'], right=[c, x], orders=[[x, y], [a, b, x], [c]]),
    all_c('rlB-', ['lB-'], left=[c], right=[x], orders=[[x, y], [a, b, x], [c]]),
    all_c('lrB-', ['lB-'], left=[x], right=[c], orders=[[x, y], [a, b, x], [c]]),

    # lB-: W interaction
    all_c('lB-', ['lB-', W], left=[x], orders=[[x, y], [z, w]]),

    # rB-: Base
    all_c('rB-', e, right=[a, c], orders=[[a], [c]]),
    # rB-: Fallback
    rule('B-', ['rB-']),
    # lB-: Co-Fallback
    ('rB-', ['B-'], [e, [x, y]]),
    # rB-: 3-ins
    all_c('rB-', ['rB-'], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('lB-', ['rB-'], left=[y], orders=[[x, y], [a, b, c]]),

    all_c('lB-', ['rB-'], left=[y, c], orders=[[x, y], [a, b, y], [c]]),
    all_c('rB-', ['rB-'], right=[y, c], orders=[[x, y], [a, b, y], [c]]),
    all_c('lrB-', ['rB-'], left=[y], right=[c], orders=[[x, y], [a, b, y], [c]]),
    all_c('rlB-', ['rB-'], left=[c], right=[y], orders=[[x, y], [a, b, y], [c]]),

    all_c('lB-', ['rB-'], left=[a, y], orders=[[x, y], [y, b, c], [a]]),
    all_c('rB-', ['rB-'], right=[a, y], orders=[[x, y], [y, b, c], [a]]),
    all_c('lrB-', ['rB-'], left=[a], right=[y], orders=[[x, y], [y, b, c], [a]]),
    all_c('rlB-', ['rB-'], left=[y], right=[a], orders=[[x, y], [y, b, c], [a]]),

    # rB-: W interaction
    all_c('rB-', ['rB-', W], right=[y], orders=[[x, y], [z, w]]),

    # lrB-: Base
    ('lrB-', e, [[a], [c]]),
    # lrB-: Fallback
    rule('B-', ['lrB-']),
    # lrB-: 3-ins
    all_c('lrB-', ['lrB-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('lB-', ['lrB-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('rB-', ['lrB-'], right=[x, y], orders=[[x, y], [a, b, c]]),

    all_c('lrB-', ['lrB-'], left=[a], right=[y], orders=[[x, y], [x, b, c], [a]]),
    all_c('lB-', ['lrB-'], left=[a, y], orders=[[x, y], [x, b, c], [a]]),
    all_c('rB-', ['lrB-'], right=[a, y], orders=[[x, y], [x, b, c], [a]]),
    all_c('rlB-', ['lrB-'], left=[y], right=[a], orders=[[x, y], [x, b, c], [a]]),

    all_c('lrB-', ['lrB-'], left=[x], right=[c], orders=[[x, y], [a, b, y], [c]]),
    all_c('lB-', ['lrB-'], left=[x, c], orders=[[x, y], [a, b, y], [c]]),
    all_c('rB-', ['lrB-'], right=[x, c], orders=[[x, y], [a, b, y], [c]]),
    all_c('rlB-', ['lrB-'], left=[c], right=[x], orders=[[x, y], [a, b, y], [c]]),

    all_c('lrB-', ['lrB-'], left=[a], right=[c], orders=[[x, y], [x, b, y], [a], [c]]),
    all_c('lB-', ['lrB-'], left=[a, c], orders=[[x, y], [x, b, y], [a], [c]]),
    all_c('rB-', ['lrB-'], right=[a, c], orders=[[x, y], [x, b, y], [a], [c]]),
    all_c('rlB-', ['lrB-'], left=[c], right=[a], orders=[[x, y], [x, b, y], [a], [c]]),

    # lrB-: W interaction
    all_c('lrB-', ['lrB-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),

    # rlB-: Base
    ('rlB-', e, [[c], [a]]),
    # rlB-: Fallback
    rule('B-', ['rlB-']),
    # rlB-: 3-ins
    all_c('rlB-', ['rlB-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('lB-', ['rlB-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('rB-', ['rlB-'], right=[x, y], orders=[[x, y], [a, b, c]]),

    all_c('rlB-', ['rlB-'], left=[c], right=[y], orders=[[x, y], [a, b, x], [c]]),
    all_c('lB-', ['rlB-'], left=[c, y], orders=[[x, y], [a, b, x], [c]]),
    all_c('rB-', ['rlB-'], right=[c, y], orders=[[x, y], [a, b, x], [c]]),
    all_c('lrB-', ['rlB-'], left=[y], right=[c], orders=[[x, y], [a, b, x], [c]]),

    all_c('rlB-', ['rlB-'], left=[x], right=[a], orders=[[x, y], [y, b, c], [a]]),
    all_c('lB-', ['rlB-'], left=[x, a], orders=[[x, y], [y, b, c], [a]]),
    all_c('rB-', ['rlB-'], right=[x, a], orders=[[x, y], [y, b, c], [a]]),
    all_c('lrB-', ['rlB-'], left=[a], right=[x], orders=[[x, y], [y, b, c], [a]]),

    # rlB-: W interaction
    all_c('rlB-', ['rlB-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),

    # lC-: Base
    ('lC-', e, [[a, b], e]),
    # lC-: Fallback
    rule('C-', ['lC-']),
    # lC-: Co-Fallback
    ('lC-', ['C-'], [[x, y], e]),
    # lC-: 3-ins
    all_c('lC-', ['lC-'], left=[x], orders=[[x, y], [a, b, c]]),
    all_c('C-', ['lC-'], right=[x], orders=[[x, y], [a, b, c]]),

    all_c('lC-', ['lC-'], left=[a, x], orders=[[x, y], [x, b, c], [a, x]]),
    all_c('C-', ['lC-'], right=[a, x], orders=[[x, y], [x, b, c], [a, x]]),
    all_c('lrC-', ['lC-'], left=[a], right=[x], orders=[[x, y], [x, b, c], [a, x]]),

    all_c('lC-', ['lC-'], left=[b, x], orders=[[x, y], [a, x, c], [x, b]]),
    all_c('C-', ['lC-'], right=[b, x], orders=[[x, y], [a, x, c], [x, b]]),
    all_c('lrC-', ['lC-'], left=[x], right=[b], orders=[[x, y], [a, x, c], [x, b]]),

    all_c('lC-', ['lC-'], left=[a, b], orders=[[x, y], [x, c], [a, b]]),
    all_c('C-', ['lC-'], right=[a, b], orders=[[x, y], [x, c], [a, b]]),
    all_c('lrC-', ['lC-'], left=[a], right=[b], orders=[[x, y], [x, c], [a, b]]),

    # lC-: W interaction
    all_c('lC-', ['lC-', W], left=[x], orders=[[x, y], [z, w]]),

    # lrC-: Base
    ('lrC-', e, [[a], [b]]),
    # lrC-: Fallback
    rule('C-', ['lrC-']),
    # lrC-: 3-ins
    all_c('lrC-', ['lrC-'], left=[x], right=[y], orders=[[x, y], [a, b, c]]),
    all_c('lC-', ['lrC-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('C-', ['lrC-'], right=[x, y], orders=[[x, y], [a, b, c]]),

    all_c('lrC-', ['lrC-'], left=[a], right=[y], orders=[[x, y], [x, b, c], [a, y]]),
    all_c('lC-', ['lrC-'], left=[a, y], orders=[[x, y], [x, b, c], [a, y]]),
    all_c('C-', ['lrC-'], right=[a, y], orders=[[x, y], [x, b, c], [a, y]]),

    all_c('lrC-', ['lrC-'], left=[x], right=[b], orders=[[x, y], [a, y, c], [x, b]]),
    all_c('lC-', ['lrC-'], left=[x, b], orders=[[x, y], [a, y, c], [x, b]]),
    all_c('C-', ['lrC-'], right=[x, b], orders=[[x, y], [a, y, c], [x, b]]),

    all_c('lrC-', ['lrC-'], left=[a], right=[b], orders=[[x, y, c], [a, b]]),
    all_c('lC-', ['lrC-'], left=[a, b], orders=[[x, y, c], [a, b]]),
    all_c('C-', ['lrC-'], right=[a, b], orders=[[x, y, c], [a, b]]),

    # lrC-: W interaction
    all_c('lrC-', ['lrC-', W], left=[x], right=[y], orders=[[x, y], [z, w]]),

    # ==================
    # lA+
    # ==================
    # lA+
    # lB+
    all_c('lrC-', ['lA+', 'lB+'], left=[x], right=[z], orders=[[x, y], [z, w]]),
    all_c('lC-', ['lA+', 'lB+'], left=[x, z], orders=[[x, y], [z, w], [x, z]]),
    all_nc('C-', ['lA+', 'lB+'], left=[x, z], orders=[[x, y], [z, w], [x, z]]),
    # rC+
    all_c('lB-', ['lA+', 'rC+'], left=[x, w], orders=[[x, y], [z, w], [x, w]]),
    all_c('rB-', ['lA+', 'rC+'], right=[x, w], orders=[[x, y], [z, w], [x, w]]),
    all_c('lrB-', ['lA+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w], [x, w]]),
    all_c('rlB-', ['lA+', 'rC+'], left=[w], right=[x], orders=[[x, y], [z, w], [x, w]]),
    all_nc('B-', ['lA+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w], [x, w]]),  # TODO spurious
    # rA-
    all_ordered_rules(W, ['lA+', 'rA-'], [x, y], [z, w], [x, w]),
    # lrA-
    # lB-
    # rB-
    # lrB-
    # rlB-
    # lC-
    # lrC-
    # A+
    # B+
    all_c('lrC-', ['lA+', 'B+'], left=[x], right=[z], orders=[[x, y], [z, w]]),
    all_c('lC-', ['lA+', 'B+'], left=[x, z, w], orders=[[x, y], [z, w], [x, z]]),
    all_nc('C-', ['lA+', 'B+'], left=[x, z, w], orders=[[x, y], [z, w], [x, z]]),
    # C+
    all_c('lB-', ['lA+', 'C+'], left=[x, z, w], orders=[[x, y], [z, w]]),
    all_c('rB-', ['lA+', 'C+'], right=[x, z, w], orders=[[x, y], [z, w]]),
    all_c('lrB-', ['lA+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),
    all_c('rlB-', ['lA+', 'C+'], left=[z, w], right=[x], orders=[[x, y], [z, w]]),
    all_nc('B-', ['lA+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),  # TODO spurious
    # A-
    all_ordered_rules(W, ['lA+', 'A-'], [x, y], [z, w], [x, z]),
    # B-
    # C-
    # ==================
    # lB+
    # ==================
    # lB+
    # rC+
    all_c('lrA-', ['lB+', 'rC+'], left=[x], right=[w], orders=[[x, y], [z, w]]),
    all_c('rA-', ['lB+', 'rC+'], right=[x, w], orders=[[x, y], [z, w], [x, w]]),
    all_nc('A-', ['lB+', 'rC+'], right=[x, w], orders=[[x, y], [z, w], [x, w]]),
    # rA-
    # lrA-
    # lB-
    # rB-
    # lrB-
    all_ordered_rules(W, ['lB+', 'lrB-'], [x, y], [z, x, w]),
    # rlB-
    # lC-
    # lrC-
    # A+
    all_c('lrC-', ['lB+', 'A+'], left=[z, w], right=[x], orders=[[x, y], [z, w]]),
    all_c('lC-', ['lB+', 'A+'], left=[z, w, x], orders=[[x, y], [z, w, x]]),
    all_nc('C-', ['lB+', 'A+'], left=[z, w, x], orders=[[x, y], [z, w, x]]),
    # B+
    # C+
    all_c('lrA-', ['lB+', 'C+'], left=[x], right=[z, w], orders=[[x, y], [z, w]]),
    all_c('rA-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]),
    all_nc('A-', ['lB+', 'C+'], right=[x], orders=[[x, y], [z, w], [x, z]]),
    # A-
    # B-
    # C-
    # ==================
    # rC+
    # ==================
    # rC+
    # rA-
    # lrA-
    # lB-
    # rB-
    # lrB-
    # rlB-
    # lC-
    all_ordered_rules(W, ['rC+', 'lC-'], [x, y], [z, w], [z, y]),
    # lrC-
    # TODO Superceded
    # all_ordered_rules(W, ['rC+', 'lrC-'], [x, y], [z, w], [z, y]),
    # A+
    all_c('lB-', ['rC+', 'A+'], left=[z, w, y], orders=[[x, y], [z, w]]),
    all_c('rB-', ['rC+', 'A+'], right=[z, w, y], orders=[[x, y], [z, w]]),
    all_c('lrB-', ['rC+', 'A+'], left=[z, w], right=[y], orders=[[x, y], [z, w]]),
    all_c('rlB-', ['rC+', 'A+'], left=[y], right=[z, w], orders=[[x, y], [z, w]]),
    all_nc('B-', ['rC+', 'A+'], right=[z, w, y], orders=[[x, y], [z, w]]),
    # B+
    all_c('lrA-', ['rC+', 'B+'], left=[z, w], right=[y], orders=[[x, y], [z, w]]),
    all_c('rA-', ['rC+', 'B+'], right=[z, w, y], orders=[[x, y], [z, w, y]]),
    all_nc('A-', ['rC+', 'B+'], right=[z, w, y], orders=[[x, y], [z, w, y]]),
    # C+
    # A-
    # B-
    # C-
    all_ordered_rules(W, ['rC+', 'C-'], [x, y], [z, w, y]),
    # ==================
    # rA-
    # ==================
    # rA-
    # lrA-
    # lB-
    all_c('rC+', ['rA-', 'lB-'], right=[z], orders=[[x, y], [z, w], [z, y]]),
    all_nc('C+', ['rA-', 'lB-'], right=[z], orders=[[x, y], [z, w], [z, y]]),
    # rB-
    all_c('rC+', ['rA-', 'rB-'], right=[w], orders=[[x, y], [z, w], [w, y]]),
    all_nc('C+', ['rA-', 'rB-'], right=[w], orders=[[x, y], [z, w], [w, y]]),
    # lrB-
    all_c('rC+', ['rA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, y]]),
    all_nc('C+', ['rA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, y]]),
    # rlB-
    all_c('rC+', ['rA-', 'rlB-'], right=[z], orders=[[x, y], [z, w], [w, y]]),
    all_nc('C+', ['rA-', 'rlB-'], right=[z], orders=[[x, y], [z, w], [w, y]]),
    # lC-
    all_c('lB+', ['rA-', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]),
    all_nc('B+', ['rA-', 'lC-'], left=[z], orders=[[x, y], [z, w], [z, y]]),
    # lrC-
    all_c('lB+', ['rA-', 'lrC-'], left=[w], orders=[[x, y], [z, w], [z, y]]),
    all_nc('B+', ['rA-', 'lrC-'], left=[w], orders=[[x, y], [z, w], [z, y]]),
    # A+
    all_ordered_rules(W, ['rA-', 'A+'], [x, y], [z, w], [z, w, y]),
    # B+
    # C+
    # A-
    # B-
    all_c('rC+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    all_nc('C+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    # C-
    all_c('lB+', ['rA-', 'C-'], left=[z, w], orders=[[x, y], [z, w, y]]),
    all_nc('B+', ['rA-', 'C-'], left=[z, w], orders=[[x, y], [z, w, y]]),
    # ==================
    # lrA-
    # ==================
    # lrA-
    # lB-
    # TODO Superceded
    # all_c('rC+', ['lrA-', 'lB-'], right=[z], orders=[[x, y], [z, w], [z, y]]),
    # all_nc('C+', ['lrA-', 'lB-'], right=[z], orders=[[x, y], [z, w], [z, y]]),
    # rB-
    # TODO Superceded
    # all_c('rC+', ['lrA-', 'rB-'], right=[w], orders=[[x, y], [z, w], [w, y]]),
    # all_nc('C+', ['lrA-', 'rB-'], right=[w], orders=[[x, y], [z, w], [w, y]]),
    # lrB-
    all_c('rC+', ['lrA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, x]]),
    all_nc('C+', ['lrA-', 'lrB-'], right=[w], orders=[[x, y], [z, w], [z, x]]),
    all_c('rC+', ['lrA-', 'lrB-'], left=[w], right=[y], orders=[[x, y], [z, x, w]]),
    all_nc('C+', ['lrA-', 'lrB-'], left=[w], right=[y], orders=[[x, y], [z, x, w]]),  # TODO spurious
    # rlB-
    all_c('rC+', ['lrA-', 'rlB-'], right=[z], orders=[[x, y], [z, w], [w, x]]),
    all_nc('C+', ['lrA-', 'rlB-'], right=[z], orders=[[x, y], [z, w], [w, x]]),
    # lC-
    all_c('lB+', ['lrA-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    all_nc('B+', ['lrA-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    all_c('lB+', ['lrA-', 'lC-'], left=[z], orders=[[z, x, y], [z, w]]),
    all_nc('B+', ['lrA-', 'lC-'], left=[z], orders=[[z, x, y], [z, w]]),  # TODO spurious
    # lrC-
    all_c('lB+', ['lrA-', 'lC-'], left=[w], orders=[[x, y], [z, w], [z, x]]),
    all_nc('B+', ['lrA-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, x]]),
    # A+
    # TODO Superceded
    # all_ordered_rules(W, ['lrA-', 'A+'], [x, y], [z, w], [z, w, y]),
    # B+
    # C+
    # A-
    # B-
    # TODO Superceded
    # all_c('rC+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    # all_nc('C+', ['rA-', 'B-'], right=[z, w], orders=[[x, y], [z, w, y]]),
    # C-
    all_c('lB+', ['lrA-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    all_nc('B+', ['lrA-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    # ==================
    # lB-
    # ==================
    # lB-
    # rB-
    # lrB-
    # rlB-
    # lC-
    all_c('lA+', ['lB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, x]]),
    all_nc('A+', ['lB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, x]]),
    # lrC-
    # TODO Superceded
    # A+
    # B+
    # C+
    # A-
    all_c('rC+', ['lB-', 'A-'], right=[x], orders=[[x, y], [x, z, w]]),
    all_nc('C+', ['lB-', 'A-'], right=[x], orders=[[x, y], [x, z, w]]),
    # B-
    # C-
    all_c('lA+', ['lB-', 'C-'], left=[x], orders=[[x, y], [z, w, x]]),
    all_nc('A+', ['lB-', 'C-'], left=[x], orders=[[x, y], [z, w, x]]),
    # ==================
    # rB-
    # ==================
    # rB-
    # lrB-
    # rlB-
    # lC-
    all_c('lA+', ['rB-', 'lC-'], left=[y], orders=[[x, y], [z, w], [z, y]]),
    all_nc('A+', ['rB-', 'lC-'], left=[y], orders=[[x, y], [z, w], [z, y]]),
    # lrC-
    # TODO Superceded
    # A+
    # B+
    # C+
    # A-
    all_c('rC+', ['rB-', 'A-'], right=[y], orders=[[x, y], [y, z, w]]),
    all_nc('C+', ['rB-', 'A-'], right=[y], orders=[[x, y], [y, z, w]]),
    # B-
    # C-
    all_c('lA+', ['rB-', 'C-'], left=[y], orders=[[x, y], [z, w, y]]),
    all_nc('A+', ['rB-', 'C-'], left=[y], orders=[[x, y], [z, w, y]]),
    # ==================
    # lrB-
    # ==================
    # lrB-
    # rlB-
    # lC-
    all_c('lA+', ['lrB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    all_nc('A+', ['lrB-', 'lC-'], left=[x], orders=[[x, y], [z, w], [z, y]]),
    # lrC-
    all_c('lA+', ['lrB-', 'lrC-'], left=[z], orders=[[x, w, y], [z, w]]),
    all_nc('A+', ['lrB-', 'lrC-'], left=[z], orders=[[x, w, y], [z, w]]),
    # A+
    # B+
    all_ordered_rules(W, ['lrB-', 'B+'], [x, z, w, y]),
    # C+
    # A-
    all_c('rC+', ['lrB-', 'A-'], right=[y], orders=[[x, y], [x, z, w]]),
    all_nc('C+', ['lrB-', 'A-'], right=[y], orders=[[x, y], [x, z, w]]),
    # B-
    # C-
    all_c('lA+', ['lrB-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    all_nc('A+', ['lrB-', 'C-'], left=[x], orders=[[x, y], [z, w, y]]),
    # ==================
    # rlB-
    # ==================
    # rlB-
    # lC-
    all_c('lA+', ['rlB-', 'lC-'], left=[y], orders=[[x, y], [z, w], [z, x]]),
    all_nc('A+', ['rlB-', 'lC-'], left=[y], orders=[[x, y], [z, w], [z, x]]),
    # lrC-
    # TODO Superceded
    # A+
    # B+
    # C+
    # A-
    all_c('rC+', ['rlB-', 'A-'], right=[x], orders=[[x, y], [y, z, w]]),
    all_nc('C+', ['rlB-', 'A-'], right=[x], orders=[[x, y], [y, z, w]]),
    # B-
    # C-
    all_c('lA+', ['rlB-', 'C-'], left=[y], orders=[[x, y], [z, w, x]]),
    all_nc('A+', ['rlB-', 'C-'], left=[y], orders=[[x, y], [z, w, x]]),
    # ==================
    # lC-
    # ==================
    # lC-
    # lrC-
    # A+
    # C+
    all_ordered_rules(W, ['lC-', 'C+'], [x, y], [x, z, w]),
    # A-
    all_c('lB+', ['lC-', 'A-'], left=[x], orders=[[x, y], [x, z, w]]),
    all_nc('B+', ['lC-', 'A-'], left=[x], orders=[[x, y], [x, z, w]]),
    # B-
    all_c('lA+', ['lC-', 'B-'], left=[z, w], orders=[[x, y], [x, z, w]]),
    all_nc('A+', ['lC-', 'B-'], left=[z, w], orders=[[x, y], [x, z, w]]),
    # C-
    # ==================
    # lrC-
    # ==================
    # lrC-
    # A+
    # C+
    # TODO Superceded
    # A-
    all_c('lB+', ['lrC-', 'A-'], left=[y], orders=[[x, y], [z, w], [x, z, w]]),
    all_nc('B+', ['lrC-', 'A-'], left=[y], orders=[[x, y], [z, w], [x, z, w]]),
    # B-
    # TODO Superceded
    # C-
]
# Refined non-terminals
# ======================

g = lambda initial_symbol: Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # ======================
    # Debugging
    # ======================
    [('_' + k, [k], [[x, y]]) for k in all_states + ['lA+', 'lB+', 'rC+', 'rA-', 'lrB-', 'lC-']],
    [('$_' + k, [k], [[x, '$', y]]) for k in all_states + ['lA+', 'lB+', 'rC+', 'rA-', 'lrB-', 'rB-', 'lC-']],

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
    all_c('lA+', ['A+'], left=[a], orders=[[x, y, b, c], [a]]),
    all_nc('A+', ['A+'], left=[a], orders=[[x, y, b, c], [a]]),
    all_c('lA+', ['A+'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('A+', ['A+'], left=[x, y], orders=[[x, y], [a, b, c]]),
    # B+
    all_c('lB+', ['B+'], left=[b], orders=[[a, x, y, c], [b]]),
    all_nc('B+', ['B+'], left=[b], orders=[[a, x, y, c], [b]]),
    all_c('lB+', ['B+'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('B+', ['B+'], orders=[[x, y], [a, b, c]], left=[x, y]),
    # C+
    all_c('rC+', ['C+'], right=[c], orders=[[a, b, x, y], [c]]),
    all_nc('C+', ['C+'], right=[c], orders=[[a, b, x, y], [c]]),
    all_c('rC+', ['C+'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('C+', ['C+'], orders=[[x, y], [a, b, c]], right=[x, y]),
    # A-
    all_c('lrA-', ['A-'], left=[b], right=[c], orders=[[a, x, y], [b, c]]),
    all_nc('A-', ['A-'], left=[b], right=[c], orders=[[a, x, y], [b, c]]),
    all_c('rA-', ['A-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('A-', ['A-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('rA-', ['A-'], right=[b, c], orders=[[a, x, y], [b, c]]),
    all_nc('A-', ['A-'], right=[b, c], orders=[[a, x, y], [b, c]]),
    # B-
    all_c('lB-', ['B-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('B-', ['B-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_c('rB-', ['B-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('B-', ['B-'], right=[x, y], orders=[[x, y], [a, b, c]]),
    # C-
    all_c('lrC-', ['C-'], left=[a], right=[b], orders=[[x, y, c], [a, b]]),
    all_nc('C-', ['C-'], left=[a], right=[b], orders=[[x, y, c], [a, b]]),
    all_c('lC-', ['C-'], left=[a, b], orders=[[x, y, c], [a, b]]),
    all_nc('C-', ['C-'], left=[a, b], orders=[[x, y, c], [a, b]]),
    all_c('lC-', ['C-'], left=[x, y], orders=[[x, y], [a, b, c]]),
    all_nc('C-', ['C-'], left=[x, y], orders=[[x, y], [a, b, c]]),

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

