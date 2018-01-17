from dyck import Grammar
from grammar_utils import *


########################################################################################################################
# Meta-grammar { all_ordered }
########################################################################################################################
all_states = [W, 'A-', 'A+', 'B-', 'B+', 'C-', 'C+']
meta2 = Grammar([
    # TOP
    (S, [W], [[x, y]]),

    # =============
    # Meta-rules
    # =============

    # W: Base
    all_o(W, e, [a, b, c]),
    # W: Concatenation
    all_o(W, [W, W], [x, y], [z, w]),

    # A-: Base
    all_o('A-', e, [b, c]),
    # A-: Double insertion (b, c)
    all_o('A-', [W], [x, y], [b, c]),
    # A- -> W
    all_o(W, ['A-'], [a, x, y]),
    # A-, W -> A-
    all_o('A-', ['A-', W], [x, y], [z, w]),

    # B-: Base
    all_o('B-', e, [a, c]),
    # B-: Double insertion (a, c)
    all_o('B-', [W], [x, y], [a, c]),
    # B- -> W
    all_o(W, ['B-'], [a, x, y]),
    # B-, W -> B-
    all_o('B-', ['B-', W], [x, y], [z, w]),

    # C-: Base
    all_o('C-', e, [a, b]),
    # C-: Double insertion (a, b)
    all_o('C-', [W], [x, y], [a, b]),
    # C- -> W
    all_o(W, ['C-'], [x, y, c]),
    # C-, W -> C-
    all_o('C-', ['C-', W], [x, y], [z, w]),

    # A+: Base
    all_o('A+', e, [a]),
    # A+: Single insertion (a)
    all_o('A+', [W], [x, y], [a]),
    # A+ -> W
    all_o(W, ['A+'], [x, y, b, c]),
    # A+, W -> A+
    all_o('A+', ['A+', W], [x, y], [z, w]),

    # B+: Base
    all_o('B+', e, [b]),
    # B+: Single insertion (a)
    all_o('B+', [W], [x, y], [b]),
    # B+ -> W
    all_o(W, ['B+'], [a, x, y, c]),
    # B+, W -> B+
    all_o('B+', ['B+', W], [x, y], [z, w]),

    # C+: Base
    all_o('C+', e, [c]),
    # C+: Single insertion (a)
    all_o('C+', [W], [x, y], [c]),
    # C+ -> W
    all_o(W, ['C+'], [a, b, x, y]),
    # C+, W -> C+
    all_o('C+', ['C+', W], [x, y], [z, w]),

    # =============
    # Meta-meta rules
    # =============

    # General 3-ins
    [[(K, [K], order) for order in all_ordered([x, y], [a, b, c])]
     for K in all_states],
    # General 3-ins (2x)
    all_o(W, [W, W], [x, y], [z, w], [a, b, c]),
    [[(W, [K, L], order) for order in all_ordered([x, y, z, w], [a, b, c])]
     for K, L in [('C-', 'C+'), ('A+', 'A-')]],

    # =============
    # Meta-rule combinations
    # =============

    all_o(W, ['A-', 'C-'], [a, x, y], [z, w, c]),

    # A+
    all_o('C-', ['A+', 'B+'], [x, y, z, w]),
    all_o('B-', ['A+', 'C+'], [x, y, z, w]),
    all_o(W, ['A+', 'A-'], [x, y, z, w]),
    # B+
    all_o('A-', ['B+', 'C+'], [x, y, z, w]),
    # C+
    # A-
    # B-
    all_o('C+', ['B-', 'A-'], [x, y, z, w]),
    # C-
    all_o(W, ['C-', 'C+'], [x, y, z, w]),
    all_o('B+', ['C-', 'A-'], [x, y, z, w]),
    all_o('A+', ['C-', 'B-'], [x, y, z, w]),
])
