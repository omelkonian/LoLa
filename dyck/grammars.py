from pprint import pprint
from dyck import Grammar
from itertools import permutations


#
# Universal constants
#
a, b, c, e = 'a', 'b', 'c', ''
x, y, z, w, k, l, m, n = (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)
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
            for n1 in range(1, len(symbols_from_orders(orders)))
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

    # 2-Tuples
    [list(prog(L, R)) for L, R in all_state_pairs()],
    # 3-Tuples
    [list(prog3(L, C, R)) for L, C, R in all_state_tuples3()],
    # 4-Tuples
    [list(prog4(W, L, C, R)) for W, L, C, R in all_state_tuples4()],

    # DEBUG
    [('_' + k, [k], [[x, y]]) for k in all_states],
    [('$_' + k, [k], [[x, '$', y]]) for k in all_states],

], topdown=True, filtered=True, initial_symbol=initial_symbol)

all_state_pairs = lambda: ((_states['W'], X) for X in states)

def all_state_tuples3():
    for A in ['lA+', 'rA+']:
        for B in ['lB+', 'rB+']:
            for C in ['lC+', 'rC+']:
                yield _states[A], _states[B], _states[C]

def all_state_tuples4():
    for S in ['W']:
        for A in ['lA+', 'rA+']:
            for B in ['lB+', 'rB+']:
                for C in ['lC+', 'rC+']:
                    yield _states[S], _states[A], _states[B], _states[C]

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
}
_states = {states[k]: k for k in states}
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


def prog((_x, _y), (_z, _w)):
    L = states[(_x, _y)]
    R = states[(_z, _w)]
    d = {x:_x, y:_y, z:_z, w:_w}
    for element1, element2 in all_ordered([x, y], [z, w]):
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
            yield (eliminated_state, [L, R], [element1, element2])


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
