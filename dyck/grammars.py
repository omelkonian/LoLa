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

# def pp(s):
#     print(s.replace('(0, 0)', 'x').replace('(0, 1)', 'y').replace('(1, 0)', 'z').replace('(1, 1)', 'w'))
#
# Grammar
#
g = lambda initial_symbol: Grammar(
[
    # TOP
    ('S', ['W'], [[x, y]]),

    # base
    [(v, [], [list(k[0]), list(k[1])]) for k, v in states.items() if v != 'W'],

    # 3-ins
    [list(triple_ins(v[0], v[1])) for v in states],

    [list(prog(L, R)) for L, R in all_state_pairs()],
    # [list(prog3(L, C, R)) for L, C, R in all_state_pairs3()],

    # all_o('W', ['lABC'], [x, y]),
    # all_o('W', ['lArBC'], [x, y]),
    # all_o('W', ['lABrC'], [x, y]),
    # all_o('W', ['rABC'], [x, y]),

    all_o('W', ['W']*3, [x, y], [z, w], [l, m]),

    # DEBUG
    [('_' + k, [k], [[x, y]]) for k in all_states],
    [('$_' + k, [k], [[x, '$', y]]) for k in all_states],

], topdown=True, filtered=True, initial_symbol=initial_symbol)


def all_state_pairs():
    cur = []
    for L in states:
        for R in states:
            if (R, L) not in cur:
                cur.append((L, R))
                yield (L, R)


def all_state_pairs3():
    cur = []
    for L in states:
        for R in states:
            for C in states:
                # Exclude X-
                if any(map(lambda t: '-' in states[t], [L, R, C])):
                    continue
                if all(map(lambda t: t not in cur, [(L, R, C), (R, L, C), (R, C, L), (C, L, R), (C, R, L)])):
                    cur.append((L, C, R))
                    yield (L, C, R)


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
    ("cb", ""): 'ulA-',
    ("", "bc"): 'rA-',
    ("", "cb"): 'urA-',
    ("b", "c"): 'lrA-',
    ("c", "b"): 'ulrA-',
    # ------------------
    ("ac", ""): 'lB-',
    ("ca", ""): 'ulB-',
    ("", "ac"): 'rB-',
    ("", "ca"): 'urB-',
    ("a", "c"): 'lrB-',
    ("c", "a"): 'ulrB-',
    # ------------------
    ("ab", ""): 'lC-',
    ("ba", ""): 'ulC-',
    ("", "ab"): 'rC-',
    ("", "ba"): 'urC-',
    ("a", "b"): 'lrC-',
    ("b", "a"): 'ulrC-',
    # ------------------
    # ("aa", ""): 'lA++',
    # ("a", "a"): 'lrA++',
    # ("", "aa"): 'rA++',
    # # ------------------
    # ("bb", ""): 'lB++',
    # ("b", "b"): 'lrB++',
    # ("", "bb"): 'rB++',
    # # ------------------
    # ("cc", ""): 'lC++',
    # ("c", "c"): 'lrC++',
    # ("", "cc"): 'rC++',
    # ------------------
    # 3 Symbols
    # ("abc", ""): 'lABC',
    # ("ab", "c"): 'lABrC',
    # ("a", "bc"): 'lArBC',
    # ("", "abc"): 'rABC',
    # # ------------------
    # ("acb", ""): 'lACB',
    # ("ac", "b"): 'lACrB',
    # ("a", "cb"): 'lArCB',
    # ("", "acb"): 'rACB',
    # # ------------------
    # ("bac", ""): 'lBAC',
    # ("ba", "c"): 'lBArC',
    # ("b", "ac"): 'lBrAC',
    # ("", "bac"): 'rBAC',
    # # ------------------
    # ("bca", ""): 'lBCA',
    # ("bc", "a"): 'lBCrA',
    # ("b", "ca"): 'lBrCA',
    # ("", "bca"): 'rBCA',
    # # ------------------
    # ("cab", ""): 'lCAB',
    # ("ca", "b"): 'lCArB',
    # ("c", "ab"): 'lCrAB',
    # ("", "cab"): 'rCAB',
    # # ------------------
    # ("cba", ""): 'lCBA',
    # ("cb", "a"): 'lCBrA',
    # ("c", "ba"): 'lCrBA',
    # ("", "cba"): 'rCBA',
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


def prog((_x, _y), (_z, _w)):
    L = states[(_x, _y)]
    R = states[(_z, _w)]
    """e.g.
    _x: a
    _y: b
    _z: b
    _w: c
    """
    d = {x:_x, y:_y, z:_z, w:_w}
    for element1, element2 in all_ordered([x, y], [z, w]):
        """e.g.
        element1 = [x, z]
        element2 = [y, w]
        """
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        """e.g.
        descriptor = ("ab", "bc")
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


def prog3((_x, _y), (_z, _w), (_l, _m)):
    L = states[(_x, _y)]
    C = states[(_z, _w)]
    R = states[(_l, _m)]
    """e.g.
    _x: a
    _y: b
    _z: b
    _w: c
    _l: e
    _m: a
    """
    d = {x:_x, y:_y, z:_z, w:_w, l: _l, m: _m}
    for element1, element2 in all_ordered([x, y], [z, w], [l, m]):
        """e.g.
        element1 = [x, z, l]
        element2 = [y, w, m]
        """
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        """e.g.
        descriptor = ("ab", "bc")
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
            yield (eliminated_state, [L, C, R], [element1, element2])
