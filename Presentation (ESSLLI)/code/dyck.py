from dyck import *
G3 = Grammar(initial='W',
  # Base Cases
  O('W', {(a, b, c)}),
  O('A-', {(b, c)}), O('B-', {(a, c)}), O('C-', {(a, b)}),
  O('A+', {(a,)}),   O('B+', {(b,)}),   O('C+', {(c,)}),
  # Combinations
  O('C- <- A+, B+', {(x, y, z, w)}),
  O('B- <- A+, C+', {(x, y, z, w)}),
  O('A- <- B+, C+', {(x, y, z, w)}),
  O('C+ <- B-, A-', {(x, y, z, w)}),
  O('B+ <- C-, A-', {(x, y, z, w)}),
  O('A+ <- C-, B-', {(x, y, z, w)}),
  forall(all_states, lambda K: O('K <- K, W', {(x, y), (z, w)})),
  # Closures
  O('W <- A+, A-', {(x, y, z, w)}),
  O('W <- C-, C+', {(x, y, z, w)}),
  # Universal Triple Insertion
  forall(all_states, lambda K: O('K <- K', {(x, y), (a, b, c)})))
