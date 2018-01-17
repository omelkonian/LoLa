from functools import partial

from dyck import Grammar
from grammar_utils import *

all_o = partial(all_o, splits=3)
mcfg3 = Grammar(
[
    # TOP
    ('S', ['W'], [[x, y, o, s]]),
    # Base
    all_o('W', e, [[a, b, c]]),
    # Concatenation
    all_o('W', ['W', 'W'], [[x, y, o, s], [z, w, p, t]], x=z, y=w, o=p, s=t),
    # 3-ins
    # all_o('W', ['W'], [[x, y, o, s], [a, b, c]]),
])
