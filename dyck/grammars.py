from pprint import pprint
try:
    from dyck import Grammar
except:
    pass
from itertools import permutations


#
# Universal constants
#
a, b, c, e = 'a', 'b', 'c', []
x, y, z = (0, 0), (0, 1), (0, 2)
k, l, m = (1, 0), (1, 1), (1, 2)
tuple_to_char = {
    x: 'x',
    y: 'y',
    z: 'z',
    k: 'k',
    l: 'l',
    m: 'm',
}


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
    return [(perm[:i1], perm[i1:i2], perm[i2:])
            for i1 in range(0, len(symbols_from_orders(orders)) + 1)
            for i2 in range(i1, len(symbols_from_orders(orders)) + 1) or [len(symbols_from_orders(orders))]
            for perm in ordered_permutations(orders, **symmetries)]


def post_process(orders, **symmetries):
    return [(post_process_single(l), post_process_single(c), post_process_single(r))
            for l, c, r in ordered_pairs(orders, **symmetries)]


def post_process_single(order):
    return [globals()[c] for c in order]


def pre_process(symbols):
    return [pre_process_single(s) for s in symbols]


def pre_process_single(symbols):
    return ''.join(
        [tuple_to_char.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(*orders, **symmetries):
    return post_process(pre_process(orders), **symmetries)


def all_o(lhs, rhs, *orders, **symmetries):
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


# pprint(all_o('W', e, [a, b, c]))

g = lambda initial_symbol: Grammar(
[
    # TOP
    ('S', ['W'], [[x, y, z]]),
    # Base
    # ('W', e, [[], [], []]),
    # Concatenation
    all_o('W', ['W', 'W'], [x, y, z], [k, l, m], x=k, y=l, z=m),
    # 3-ins
    # all_o('W', ['W'], [x, y, z], [a, b, c]),

    all_o('W', e, [a, b, c])

], topdown=True, filtered=True, initial_symbol=initial_symbol)

