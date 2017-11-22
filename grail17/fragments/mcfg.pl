% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

% ============================================================
% Lexicon: abstract constants and tuple interpretation
% ============================================================

% 2-MCFG for a^n b^n c^n d^n

% using linear pairs for the target

20 :: s/a :: A^I^(fst(A)@(snd(A)@I)).
21 :: a/a :: A^(I^('$a$'@(fst(A)@('$b$'@I))),J^('$c$'@(snd(A)@('$d$'@J)))).
22 :: a :: (J^J,J^J).

% modeling tuples by higher-order functions

30 :: s/a :: P^(P@(X^Y^I^(X@(Y@I)))).
31 :: a/a :: P^F^(P@(X^Y^((F@(I^('$a$'@(X@('$b$'@I)))))@(J^('$c$'@(Y@('$d$'@J))))))).
32 :: a :: F^((F@(J^J))@(J^J)).

% a^n b^m c^n d^m

a :: (s/b)/a :: PairA^PairB^I^(fst(PairA)@(fst(PairB)@(snd(PairA)@(snd(PairB)@I)))).
b :: a/a :: PairA^(I^('$a$'@(fst(PairA)@I)),J^('$c$'@(snd(PairA)@J))).
c :: a :: (I^I,J^J).
d :: b/b :: PairB^(I^('$b$'@(fst(PairB)@I)),J^('$d$'@(snd(PairB)@J))).
e :: b :: (I^I,J^J).

% par shuffle

0 :: s/a :: PairA^I^(fst(PairA)@(snd(PairA)@I)).
db :: b :: ('$a$','$\\overline{a}$').
qp :: b :: ('$b$','$\\overline{b}$').
% oo :: a :: (I^I,J^J).
1 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(snd(PairB)@I)), J^(fst(PairA)@(snd(PairA)@J))).
2 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(fst(PairA)@I)), J^(snd(PairB)@(snd(PairA)@J))).
3 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(fst(PairA)@I)), J^(snd(PairA)@(snd(PairB)@J))).
4 :: (a/a)/b :: PairB^PairA^(fst(PairB), J^(snd(PairB)@(fst(PairA)@(snd(PairA)@J)))).
5 :: (a/a)/b :: PairB^PairA^(fst(PairB), J^(fst(PairA)@(snd(PairB)@(snd(PairA)@J)))).
6 :: (a/a)/b :: PairB^PairA^(fst(PairB), J^(fst(PairA)@(snd(PairA)@(snd(PairB)@J)))).
7 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(snd(PairB)@(fst(PairA)@I))), snd(PairA)).
8 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(fst(PairA)@(snd(PairB)@I))), snd(PairA)).
9 :: (a/a)/b :: PairB^PairA^(I^(fst(PairB)@(fst(PairA)@(snd(PairA)@I))), snd(PairB)).

10 :: a/b :: PairB^(I^(fst(PairB)@(snd(PairB)@I)),J^J).
11 :: a/b :: PairB^(fst(PairB),snd(PairB)).
12 :: a/b :: PairB^(J^J,I^(fst(PairB)@(snd(PairB)@I))).

% ============================================================
% Postulates
% ============================================================


% ============================================================
% Examples
% ============================================================

