from dyck import Grammar
from grammar_utils import *

naive = Grammar([
    (S, [A], [[x, y]]),
    (A, [A], [[x], [y, a, b, c]]),
    (A, [A], [[x], [a, y, b, c]]),
    (A, [A], [[x], [a, b, y, c]]),
    (A, [A], [[x], [a, b, c, y]]),
    (A, [A], [[x, y], [a, b, c]]),
    (A, [A], [[x, a], [y, b, c]]),
    (A, [A], [[x, a], [b, y, c]]),
    (A, [A], [[x, a], [b, c, y]]),
    (A, [A], [[x, y, a], [b, c]]),
    (A, [A], [[x, a, y], [b, c]]),
    (A, [A], [[x, a, b], [y, c]]),
    (A, [A], [[x, a, b], [c, y]]),
    (A, [A], [[x, y, a, b], [c]]),
    (A, [A], [[x, a, y, b], [c]]),
    (A, [A], [[x, a, b, y], [c]]),
    (A, [A], [[x, a, b, c], [y]]),
    (A, [A, A], [[a, x, b], [z, c, y, w]]),
    (A, [A, A], [[a, x, b], [z, c, w, y]]),
    (A, [A, A], [[x, z, a, y, b],[w, c]]),
    (A, [A, A], [[x, z, a, w, b], [y, c]]),
    (A, [], [[a], [b, c]]),
    (A, [], [[a, b], [c]])
])

