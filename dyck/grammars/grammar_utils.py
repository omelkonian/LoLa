from itertools import permutations, combinations
import numpy as np


#
# Universal constants
#
tuple_to_char = {
    # 1-MCFG
    (0, 0): 'x',
    (1, 0): 'z',
    (2, 0): 'k',
    (3, 0): 'm',
    # 2-MCFG
    (0, 1): 'y',
    (1, 1): 'w',
    (2, 1): 'l',
    (3, 1): 'n',
    # 3-MCFG
    (0, 2): 'o',
    (1, 2): 'p',
    (2, 2): 'q',
    (3, 2): 'r',
    # 4-MCFG
    (0, 3): 's',
    (1, 3): 't',
    (2, 3): 'u',
    (3, 3): 'v',
}
for key, value in tuple_to_char.items():
    globals().update({value: key})

a, b, c, S, W = 'abcSW'
e = []
A, A_, B, B_, C, C_ = 'A', 'A-', 'B', 'B-', 'C', 'C-'
AB, AC, BA, CA, BC, CB, AA, BB, CC = 'AB', 'AC', 'BA', 'CA', 'BC', 'CB', 'AA', 'BB', 'CC'
A_B_, A_C_, B_A_, C_A_, B_C_, C_B_, A_A_, B_B_, C_C_ = 'A-B-', 'A-C-', 'B-A-', 'C-A-', 'B-C-', 'C-B-', 'A-A-', 'B-B-', 'C-C-'
AC_, C_A, A_A, AA_, CC_, CA_, A_C, BA_, C_B, B_C, AB_, BB_, BC_ = 'AC-', 'C-A', 'A-A', 'AA-', 'CC-', 'CA-', 'A-C', 'BA-', 'C-B', 'B-C', 'AB-', 'BB_', 'BC_'
all_singles = [A, A_, B, B_, C, C_]
all_doubles = [AA, AA_, AB, AB_, AC, AC_, BA_, BB, BB_, BC, BC_, CC, CC_, A_A_, A_B_, A_C_, B_B_, B_C_, C_C_]


#
# Meta-grammar utilities
#
def flatten(l):
    return sum(l, [])


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


def ordered_pairs(orders, splits=1, **symmetries):
    return [tuple([np_arr.tolist() for np_arr in np.split(list(perm), indices)])
            for indices in combinations(range(len(symbols_from_orders(orders))), splits)
            for perm in ordered_permutations(orders, **symmetries)]


def post_process(orders, splits=1, **symmetries):
    p = ordered_pairs(orders, splits=splits, **symmetries)
    return [map(post_process_single, tuple) for tuple in ordered_pairs(orders, splits=splits, **symmetries)]


def post_process_single(order):
    return [globals()[ch] for ch in order]


def pre_process(symbols):
    return [pre_process_single(s) for s in symbols]


def pre_process_single(symbols):
    return ''.join([tuple_to_char.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(orders, splits=1, **symmetries):
    return post_process(pre_process(orders), splits=splits, **symmetries)


def all_o(lhs, rhs, orders, splits=1, **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(orders, splits=splits, **symmetries)]


def all_c(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    return [(lhs, rhs, order) for order in all_ordered(orders, **symmetries)
            if all(map(lambda l: l in order[0], left))
            if all(map(lambda r: r in order[1], right))]


def all_nc(lhs, rhs, left=[], right=[], orders=[], **symmetries):
    allOrd = all_ordered(orders, **symmetries)
    allCon = [o for o in allOrd
              if all(map(lambda l: l in o[0], left))
              if all(map(lambda r: r in o[1], right))]
    return [(lhs, rhs, o) for o in allOrd if o not in allCon]


def remove_symmetries(words, **symmetries):
    ret = []
    for w in words:
        if [translate(w, **symmetries)] not in ret:
            ret += [[w]]
    return flatten(ret)


def translate(word, **symmetries):
    symmetries = {k: (tuple_to_char[v] if isinstance(v, tuple) else v) for k, v in symmetries.items()}
    symmetries = dict(symmetries, **{v: k for k, v in symmetries.items()})  # add inverse translations
    return ''.join([symmetries.get(c, c) for c in word])
