from pprint import pprint
from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c, e = 'a', 'b', 'c', ''
x, y, z, w, l, m = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)
tuple_to_char = {
    (0, 0): 'x',
    (0, 1): 'y',
    (1, 0): 'z',
    (1, 1): 'w',
    (2, 0): 'l',
    (2, 1): 'm',
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


def ordered_permutations(orders):
    return ([
            ''.join(s)
            for s in permutations(symbols_from_orders(orders))
            if is_ordered(s, orders)])


def ordered_pairs(orders):
    return [(perm[:n1], perm[n1:])
            for n1 in range(0, len(symbols_from_orders(orders)) + 1)
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
        [tuple_to_char.get(s, 'e' if s == [] else s) for s in symbols])


def all_ordered(*orders):
    return post_process(pre_process(orders))

def all_o(lhs, rhs, *orders):
    return [(lhs, rhs, order) for order in all_ordered(*orders)]

# Grammar
g = lambda initial_symbol: Grammar(
[
    # TOP
    ('S', ['W'], [[x, y]]),

    # base
    [(v, [], [list(k[0]), list(k[1])]) for k, v in states.items() if v != 'W'],

    # 2-ins
    # [list(double_ins(v[0], v[1])) for v in states],
    # 3-ins
    # [list(triple_ins(v[0], v[1])) for v in states],

    [list(prog(L, R)) for L, R in all_state_pairs()],

], topdown=True, filtered=True, initial_symbol=initial_symbol)


def all_state_pairs():
    cur = []
    for L in states:
        for R in states:
            if (R, L) not in cur:
                cur.append((L, R))
                yield (L, R)


states = {
    # 0 Symbol
    ('', ''): 'W',
    # 1 Symbol
    ("a", ''): 'lA+',
    ('', "a"): 'rA+',
    # ------------------
    ("b", ''): 'lB+',
    ('', "b"): 'rB+',
    # ------------------
    ("c", ''): 'lC+',
    ('', "c"): 'rC+',
    # 2 Symbols
    ("bc", ""): 'lA-',
    ("", "bc"): 'rA-',
    ("b", "c"): 'lrA-',
    # ------------------
    ("ac", ""): 'lB-',
    ("", "ac"): 'rB-',
    ("a", "c"): 'lrB-',
    # ------------------
    ("ab", ""): 'lC-',
    ("", "ab"): 'rC-',
    ("a", "b"): 'lrC-',
}
all_states = states.values()


def eliminate((l, r)):
    lr = l + '%' + r
    a_choices = [i for i, ch in enumerate(lr) if ch == 'a']
    b_choices = [i for i, ch in enumerate(lr) if ch == 'b']
    c_choices = [i for i, ch in enumerate(lr) if ch == 'c']

    choices = [(a_i, b_i, c_i) for a_i in a_choices for b_i in b_choices for c_i in c_choices]
    valid_choices = filter(lambda (k, l, m): k < l < m, choices)
    if not valid_choices:
        yield tuple(lr.split('%'))
    for (a_i, b_i, c_i) in valid_choices:
        temp = list(lr)
        temp[a_i] = '$'
        temp[b_i] = '$'
        temp[c_i] = '$'
        lr2 = "".join(temp)
        eliminated = "".join([ch for ch in lr2 if ch != '$'])
        rule = tuple(eliminated.split('%'))
        yield rule # W <- ....
        if rule == (e, e):
            yield (l, r)


def double_ins(_x, _y):
    # _x: "b"
    # _y: "a"
    d = {x:_x, y:_y}
    rhs = states[(_x, _y)]
    perms = sum([
        all_ordered([x, y], [k], [l])
        for k in [a, b, c]
        for l in [a, b, c]]
        , [])

    def transform(l):
        return ''.join(map(lambda elem: d[elem] if isinstance(elem, tuple) else elem, l))

    perms2 = map(lambda (l1, l2): (transform(l1), transform(l2)), perms)
    for perm, _perm in zip(perms2, perms):
        eliminated = list(eliminate(perm))[0]
        try:
            state = states[eliminated]
            rule = (state, [rhs], [_perm[0], _perm[1]])
            yield rule
        except KeyError:
            continue


def triple_ins(_x, _y):
    # _x: "b"
    # _y: "a"
    d = {x:_x, y:_y}
    rhs = states[(_x, _y)]
    perms = all_ordered([x, y], [a], [b], [c])

    def transform(l):
        return ''.join(map(lambda elem: d[elem] if isinstance(elem, tuple) else elem, l))

    perms2 = map(lambda (l1, l2): (transform(l1), transform(l2)), perms)
    for perm, _perm in zip(perms2, perms):
        eliminated = list(eliminate(perm))[0]
        try:
            state = states[eliminated]
            rule = (state, [rhs], [_perm[0], _perm[1]])
            yield rule
        except KeyError:
            continue


def flatten(l):
    return sum(l, [])


def prog((_x, _y), (_z, _w), insertions=[], repetitions=0):
    L = states[(_x, _y)]
    R = states[(_z, _w)]
    """e.g.
    _x: a
    _y: b
    _z: b
    _w: c
    """
    d = {x: _x, y: _y, z: _z, w: _w}
    all_insertions = [e, [a], [b], [c], [a, b], [a, c], [b, c]]
    all_combinations = flatten([
        all_ordered([x, y], [z, w], *[[el] for el in to_insert])
        for to_insert in all_insertions
    ])
    for element1, element2 in all_combinations:
        """e.g.
        element1 = [x, z, a]
        element2 = [y, b, w]
        """
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem] if isinstance(elem, tuple) else elem
        for elem in element2:
            desc2 += d[elem] if isinstance(elem, tuple) else elem
        descriptor = (desc1, desc2)
        """e.g.
        descriptor = ("abA", "bcB")
        """
        eliminated_list = eliminate(descriptor)
        """e.g.
        eliminatedList = [
            (e, "b"),
            ("b", e)
        ]
        """
        for eliminated in eliminated_list:
            """e.g.
            eliminated = (e, "b")
            """
            try:
                eliminated_state = states[eliminated]
            except KeyError:
                continue
            """e.g.
            eliminated_state = "rB+"
            """
            yield (eliminated_state, [L, R], [element1, element2])
