from pprint import pprint
from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c, e = 'a', 'b', 'c', ''
x, y, z, w = (0, 0), (0, 1), (1, 0), (1, 1)
tuple_to_char = {
    (0, 0): 'x',
    (0, 1): 'y',
    (1, 0): 'z',
    (1, 1): 'w',
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
g = lambda _: Grammar(
[
    # TOP
    ('S', ['W'], [[x, y]]),

    # base
    [(v, [], [list(k[0]), list(k[1])]) for k, v in states.items() if v != 'W'],

    # 3-ins
    [all_o(v, [v], [x, y], [a, b, c]) for v in all_states],

    [list(prog(L, R)) for L, R in all_state_pairs()],
])


def all_state_pairs():
    cur = []
    for L in states:
        for R in states:
            if (R, L) not in cur:
                cur.append((L, R))
                yield (L, R)


all_states = []
states = {
    (e, e): 'W',

    (a, e): 'lA+',
    (e, a): 'rA+',

    (b, e): 'lB+',
    (e, b): 'rB+',

    (c, e): 'lC+',
    (e, c): 'rC+',

    (b + c, e): 'lA-',
    (c + b, e): 'ulA-',
    (e, b + c): 'rA-',
    (e, c + b): 'urA-',
    (b, c): 'lrA-',
    (c, b): 'ulrA-',

    (a + c, e): 'lB-',
    (c + a, e): 'ulB-',
    (e, a + c): 'rB-',
    (e, c + a): 'urB-',
    (a, c): 'lrB-',
    (c, a): 'ulrB-',

    (a + b, e): 'lC-',
    (b + a, e): 'ulC-',
    (e, a + b): 'rC-',
    (e, b + a): 'urC-',
    (a, b): 'lrC-',
    (b, a): 'ulrC-',
}


def eliminate((l, r)):
    lr = l + '%' +  r
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
        yield tuple(eliminated.split('%'))


def prog((_x, _y), (_z, _w)):
    # try:
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
            except (KeyError, TypeError):
                continue
            """e.g.
            eliminated_state = "rB+"
            """
            # TODO map(lambda t: t.replace(e, '')
            yield (eliminated_state, [L, R], [element1, element2])
    # except KeyError as e:
    #     print(e)
    #     yield []

# pprint(list(prog((a, e), (b, e))))