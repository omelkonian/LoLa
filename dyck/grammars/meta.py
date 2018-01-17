from dyck import Grammar
from grammar_utils import *


########################################################################################################################
# Meta-grammar
########################################################################################################################
meta = Grammar([
    # TOP
    (S, [W], [[x, y]]),
    # W: Base
    [(W, e, order) for order in all_ordered([a, b, c])],
    (W, e, [[a, b, c], e]),
    # W: Concatenation
    [(W, [W, W], order) for order in all_ordered([x, y], [z, w])],
    # W: Triple insertion
    [(W, [W], order) for order in all_ordered([x, y], [a, b, c])],
    [(W, [W, W], order) for order in all_ordered([x, y], [z, w], [a, b, c])],

    # A-: Base
    [('A-', e, order) for order in all_ordered([b, c])],
    # A-: Double insertion (b, c)
    [('A-', [W], order) for order in all_ordered([x, y], [b, c])],
    # A-: Triple insertion
    [('A-', ['A-'], order) for order in all_ordered([x, y], [a, b, c])],
    # A- -> W
    [(W, ['A-'], order) for order in all_ordered([a, x, y])],

    # C-: Base
    [('C-', e, order) for order in all_ordered([a, b])],
    # C-: Double insertion (a, b)
    [('C-', [W], order) for order in all_ordered([x, y], [a, b])],
    # C-: Triple insertion
    [('C-', ['C-'], order) for order in all_ordered([x, y], [a, b, c])],
    # C- -> W
    [(W, ['C-'], order) for order in all_ordered([x, y, c])],

    # A+: Base
    [('A+', e, order) for order in all_ordered([a])],
    # A+: Single insertion (a)
    [('A+', [W], order) for order in all_ordered([x, y], [a])],
    # A+: Triple insertion
    [('A+', ['A+'], order) for order in all_ordered([x, y], [a, b, c])],
    # A+ -> W
    [(W, ['A+'], order) for order in all_ordered([x, y, b, c])],

    # B+: Base
    [('B+', e, order) for order in all_ordered([b])],
    # B+: Single insertion (a)
    [('B+', [W], order) for order in all_ordered([x, y], [b])],
    # B+: Triple insertion
    [('B+', ['B+'], order) for order in all_ordered([x, y], [a, b, c])],
    # B+ -> W
    [(W, ['B+'], order) for order in all_ordered([a, x, y, c])],

    # C+: Base
    [('C+', e, order) for order in all_ordered([c])],
    # C+: Single insertion (a)
    [('C+', [W], order) for order in all_ordered([x, y], [c])],
    # C+: Triple insertion
    [('C+', ['C+'], order) for order in all_ordered([x, y], [a, b, c])],
    # C+ -> W
    [(W, ['C+'], order) for order in all_ordered([a, b, x, y])],

    #
    # Combinations
    #

    # A- /\ C- => W
    [(W, ['A-', 'C-'], order) for order in all_ordered([a, x, y], [z, w, c])],

    # A+ /\ A- => W
    [(W, ['A+', 'A-'], order) for order in all_ordered([x, y, z, w])],

    # C- /\ C+ => W
    [(W, ['C-', 'C+'], order) for order in all_ordered([x, y, z, w])],

    # A+ /\ B+ => C-
    [('C-', ['A+', 'B+'], order) for order in all_ordered([x, y, z, w])],

    # B+ /\ C+ => A-
    [('A-', ['B+', 'C+'], order) for order in all_ordered([x, y, z, w])],
])
