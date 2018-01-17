from dyck import Grammar
from grammar_utils import *

std, std_abc = [[x, y], [z, w]], [[a, x, y], [b, z, w, c]]

n5 = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W BASE
    (W, e, [[a, b, c], e]),
    (W, e, [[a, b], [c]]),
    (W, e, [[a], [b, c]]),
    # W PERMUTATIONS
    (W, [W, W], [[x, y], [z, w]]),
    (W, [W, W], [[x, z], [y, w]]),
    (W, [W, W], [[x, z], [w, y]]),
    (W, [W, W], [[z, x], [y, w]]),
    (W, [W, W], [[z, x], [w, y]]),
    (W, [W, W], [[z, w], [x, y]]),
    (W, [W, W], [[x, y, z], [w]]),
    (W, [W, W], [[x], [y, z, w]]),
    # W TRIPLE INSERTION (BASE)
    # (W, [W], [[a, x, b, y, c], e]),
    # (W, [W], [[a, x, b, y], [c]]),
    (W, [W], [[a, x, b], [y, c]]),
    # (W, [W], [[a, b, x], [y, c]]),
    # (W, [W], [[a, x], [b, y, c]]),
    # (W, [W], [[a], [x, b, y, c]]),
    # (W, [W], [[], [x, b, y, c]]),
    # W TRIPLE INSERTION (COMB)
    (W, [W, W], [[a, x, b], [z, c, y, w]]),
    (W, [W, W], [[a, x, b], [z, c, w, y, ]]),
    (W, [W, W], [[x, z, a, y, b], [w, c]]),
    (W, [W, W], [[x, z, a, w, b], [y, c]]),
    # A+, B+, C+
    [[
        (l.upper(), e, [[l], e]),
        (l.upper(), e, [e, [l]]),
        (l.upper(), [W], [[l, x], [y]]),
        (l.upper(), [W], [[x, l], [y]]),
        (l.upper(), [W], [[x], [y, l]]),
    ] for l in "abc"],
    # NEGATIVES (BASE)
    (C_, [A, B], [[x, y], [z, w]]),
    (A_, [B, C], [[x, y], [z, w]]),
    (B_, [A, C], [[x, y], [z, w]]),
    # NEGATIVES (COMB)
    [[
        (W, [l, r], [[x, y, z, w], e]),
        (W, [l, r], [[x, y, z], [w]]),
        (W, [l, r], [[x, y], [z, w]]),
        # (W, [l, r], [[x],          [y, z, w]]),
    ] for l, r in [(C_, C), (A, A_)]],
    # NEGATIVES (COMB')

    # DOUBLES (INVERSE)
    [(k + l, [l + k], [[x], [y]]) for k in all_singles for l in all_singles],
    # DOUBLES (BASE)
    [(k + l, [k, l], [[x, y], [z, w]]) for k in all_singles for l in all_singles],
    # DOUBLES (REDUCTION)
    [[
        (k + l, [k + A, A_ + l], std),
        (k + l, [k + C_, C + l], std),
        (l, [A, A_ + l], std),
        (k, [k + A, A_], std),
        (l, [C_, C + l], std),
        (k, [k + C_, C], std),
    ] for k in all_singles for l in all_singles],
    # DOUBLES (K/L)
    [[
        # POSITIVE
        (k + C_, [k + A, B], std),
        (k + C_, [A, k + B], std),
        (k + A_, [k + B, C], std),
        (k + A_, [B, k + C], std),
    ] for k in all_singles],
    # AD-HOC
    (A_C_, [AB, BC], std),

    (W, [AA, A_A_], std),
    (W, [C_C_, CC], std),

    (BA, [C_, A_A], std),
    (BB, [C_B, A_], std),

    (C_C_, [AA, BB], std),
    (A_A_, [BB, CC], std),

    (CC, [B_, A_C], std),
    (B_C, [A, CC], std),
    (CC, [B_C, A_], std),

    # DOUBLES (TRIPLE INSERTION)

    #
    # Aggregated
    #
    [[
        (d, [d], [[a, x, b], [y, c]]),
        (d, [d], [[a, b, x], [y, c]])
    ] for d in all_doubles],
    [[
        (d, [A_A, d], std_abc),
    ] for d in all_doubles],
    [[
        (d, [d, CC_], std_abc),
    ] for d in all_doubles],
    [[
        (C_ + r, [A + r, A_C_], std_abc),
    ] for r in all_singles],
    [[
        (l + A_, [A_C_, l + C], std_abc),
    ] for l in all_singles],

    #
    # Exhaustive
    #
    (BA, [AB, A_A], std_abc),
    (BA, [AB, A_A], std_abc),
    (AA, [C_C_, B_B_], std_abc),
    (CC, [B_B_, A_A_], std_abc),

    (W, [AA, A_A_], std_abc),
    (W, [C_C_, CC], std_abc),
    (W, [C_A, A_C], std_abc),

    (W, [A_A, CC_], std_abc),

    # AA
    (AA, [AA, AA_], std_abc),
    (C_, [AA, BA_], std_abc),
    (C_C_, [AA, BB], std_abc),
    (B_B_, [AA, CC], std_abc),
    (B_B_, [AA, CC], std_abc),
    (AA, [AA, CC_], std_abc),
    (W, [AA, A_A_], std_abc),
    (AB_, [AA, A_B_], std_abc),
    (AC_, [AA, A_C_], std_abc),
    # AA_
    (A_, [AA_, BC], std_abc),
    (W, [AA_, CC_], std_abc),
    # AB
    (AB, [AB, AA_], std_abc),
    (C_C_, [AB, AB], std_abc),
    (A, [AB, AC], std_abc),
    (AB, [AB, BB_], std_abc),
    (B, [AB, BC], std_abc),
    (A_, [AB, CA_], std_abc),
    (C, [AB, CC], std_abc),
    (C_, [AB, CC_], std_abc),
    (BA_, [AB, A_A_], std_abc),
    (AA_, [AB, A_B_], std_abc),
    (BC_, [AB, A_C_], std_abc),
    (AB_, [AB, B_B_], std_abc),
    (AC_, [AB, B_C_], std_abc),
])

