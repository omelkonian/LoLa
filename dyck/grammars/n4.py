from dyck import Grammar
from grammar_utils import *

std = [[x, y], [z, w]]
n4_grammar = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W BASE
    (W, e, [[a, b, c], e]),
    (W, e, [[a, b], [c]]),
    (W, e, [[a], [b, c]]),
    # W PERMUTATIONS
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    (W, [W, W], std),
    # W TRIPLE INSERTION (BASE)
    (W, [W], [[a, x, b], [y, c]]),
    # W TRIPLE INSERTION (COMBINATIONS)
    (W, [W, W], [[a, x, b], [z, c, y, w]]),
    (W, [W, W], [[a, x, b], [z, c, w, y]]),
    (W, [W, W], [[x, z, a, y, b], [w, c]]),
    (W, [W, W], [[x, z, a, w, b], [y, c]]),

    # A+, B+, C+
    [[(l.upper(), e, [[l], e]),
      (l.upper(), e, [e, [l]]),
      (l.upper(), [W], [[l, x], [y]]),
      (l.upper(), [W], [[x, l], [y]]),
      (l.upper(), [W], [[x],    [y, l]]),
      ] for l in "abc"],

    [[
        # COMBINATIONS
        (W, [l, r], [[x, y, z, w], e]),
        (W, [l, r], [[x, y, z], [w]]),
        (W, [l, r], [[x, y], [z, w]]),
        # (W, [l, r], [[x],          [y, z, w]]),
    ] for l, r in [(C_, C), (A, A_)]],

    # A-, B-, C-
    ('C-', [A, B], std),
    ('A-', [B, C], std),
    ('B-', [A, C], std),

    # INVERSE DOUBLES
    [(k + l, [l + k], [[x], [y]]) for k in all_singles for l in all_singles],

    # DOUBLES (BASE)
    [(k + l, [k, l], [[x, y], [z, w]]) for k in all_singles for l in all_singles],

    # DOUBLES (REDUCTION)
    (C_C_, [AC_, B], std),
    (C_A, [C_C_, C_A], std),
    (A_A, [BA, C], std),
    (C_A, [C_A, A_A], std),
    (A,   [C_A, C], std),
    (CC_, [AC, B], std),
    (AC_, [C_A, CC_], std),
    (C_, [AC_, A_], std),
    (C, [A, CA_], std),
    (A_C, [BA, C], std),
    (A_C, [A_A, CA_], std),
    (C_A_, [C_C_, A_C], std),
    (C_, [A, C_A_], std),
    (CA_, [CC_, A_C], std),
    (C, [A, CA_], std),
    (AA, [C_A, AC], std),
    (BA_, [C_B, A_C], std),
    (A_A_, [BA_, C], std),
    (W, [AA, A_A_], std),
])

