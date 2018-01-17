from dyck import Grammar
from grammar_utils import *

states = {
    # 0 Symbol
    ('', ''): 'W',
    # 1 Symbol
    # ("a", ''): 'lA+',
    # ('', "a"): 'rA+',
    # ------------------
    # ("b", ''): 'lB+',
    # ('', "b"): 'rB+',
    # ------------------
    # ("c", ''): 'lC+',
    # ('', "c"): 'rC+',
    # 2 Symbols
    # ("bc", ""): 'lA-',
    # ("cb", ""): 'ulA-',
    # ("", "bc"): 'rA-',
    # ("", "cb"): 'urA-',
    # ("b", "c"): 'lrA-',
    # ("c", "b"): 'ulrA-',
    # # ------------------
    # ("ac", ""): 'lB-',
    # ("ca", ""): 'ulB-',
    # ("", "ac"): 'rB-',
    # ("", "ca"): 'urB-',
    # ("a", "c"): 'lrB-',
    # ("c", "a"): 'ulrB-',
    # # ------------------
    # ("ab", ""): 'lC-',
    # ("ba", ""): 'ulC-',
    # ("", "ab"): 'rC-',
    # ("", "ba"): 'urC-',
    # ("a", "b"): 'lrC-',
    # ("b", "a"): 'ulrC-',
    # # ------------------
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
    # # ------------------
    # # 3 Symbols
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
_states = {states[k]: k for k in states}


def all_state_pairs():
    cur = []
    for L in states:
        for R in states:
            if (R, L) not in cur:
                cur.append((L, R))
                yield (L, R)


def all_state_tuples3():
    cur = []
    for A in states:
        for B in states:
            for C in states:
                if all([(X, Y, Z) not in cur for X, Y, Z in [
                    (A, C, B),
                    (B, A, C), (B, C, A),
                    (C, A, B), (C, B, A)
                ]]):
                    yield (A, B, C)


def all_state_tuples4():
    cur = []
    for A in states:
        for B in states:
            for C in states:
                for D in states:
                    if all([(X, Y, Z, W) not in cur for X, Y, Z, W in [
                        (A, B, D, C), (A, D, B, C), (A, D, C, B), (A, C, B, D), (A, C, D, B),
                        (B, A, C, D), (B, A, D, C), (B, C, A, D), (B, C, D, A), (B, D, A, C), (B, D, C, A),
                        (C, A, B, D), (C, A, D, B), (C, B, A, D), (C, B, D, A), (C, D, A, B), (C, D, B, A),
                        (D, A, B, C), (D, A, C, B), (D, B, A, C), (D, B, C, A), (D, C, A, B), (D, C, B, A),
                    ]]):
                        yield (A, B, C, D)


# def all_state_pairs3():
#     cur = []
#     for L in states:
#         for R in states:
#             for C in states:
#                 # Exclude X-
#                 if any(map(lambda t: '-' in states[t], [L, R, C])):
#                     continue
#                 if all(map(lambda t: t not in cur, [(L, R, C), (R, L, C), (R, C, L), (C, L, R), (C, R, L)])):
#                     cur.append((L, C, R))
#                     yield (L, C, R)


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
    perms = flatten([
        all_ordered([x, y], [k], [l])
        for k in [a, b, c]
        for l in [a, b, c]])

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
        for eliminated in eliminate(perm):
            try:
                state = states[eliminated]
                rule = (state, [rhs], [_perm[0], _perm[1]])
                yield rule
            except KeyError:
                continue




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
    all_insertions = [e] # [e, [a], [b], [c], [a, b], [a, c], [b, c]]
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
        eliminated_list = list(eliminate(descriptor)) # + [descriptor] # also do not eliminate
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


# TODO make the same as prog
def prog3((_x, _y), (_z, _w), (_k, _l)):
    A = states[(_x, _y)]
    B = states[(_z, _w)]
    C = states[(_k, _l)]
    d = {x:_x, y:_y, z:_z, w:_w, k: _k, l: _l}
    for element1, element2 in all_ordered([x, y], [z, w], [k, l]):
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        eliminated_list = eliminate(descriptor)
        for eliminated in eliminated_list:
            try:
                eliminated_state = states[eliminated]
            except KeyError:
                continue
            yield (eliminated_state, [A, B, C], [element1, element2])


def prog4((_x, _y), (_z, _w), (_k, _l), (_m, _n)):
    W = states[(_x, _y)]
    A = states[(_z, _w)]
    B = states[(_k, _l)]
    C = states[(_m, _n)]
    d = {x:_x, y:_y, z:_z, w:_w, k: _k, l: _l, m: _m, n: _n}
    for element1, element2 in all_ordered([x, y], [z, w], [k, l], [m, n]):
        desc1, desc2 = "", ""
        for elem in element1:
            desc1 += d[elem]
        for elem in element2:
            desc2 += d[elem]
        descriptor = (desc1, desc2)
        eliminated_list = eliminate(descriptor)
        for eliminated in eliminated_list:
            try:
                eliminated_state = states[eliminated]
            except KeyError:
                continue
            yield (eliminated_state, [W, A, B, C], [element1, element2])

x, y, z, w, k, l, m, n = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)
automatic_rule_inference = Grammar([
    # TOP
    ('S', ['W'], [[x, y]]),

    # base
    [(v, [], [list(kk[0]), list(kk[1])]) for kk, v in states.items() if v != 'W'],

    # 2-ins
    [list(double_ins(v[0], v[1])) for v in states],
    # 3-ins
    [list(triple_ins(v[0], v[1])) for v in states],

    # 2-tuples
    [list(prog(L, R)) for L, R in all_state_pairs()],
    # 3-Tuples
    [list(prog3(L, C, R)) for L, C, R in all_state_tuples3()],
    # 4-Tuples
    [list(prog4(A, B, C, D)) for A, B, C, D in all_state_tuples4()],

])

