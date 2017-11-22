
% ============================================================
% Lexicon: abstract rule constants and their translation
% ============================================================

% eta(s) = x --o x (string type, abbrev: str)
% eta(a) = (str --o str --o str) --o str (encoding tuple of strings)

% Term notation: 
% application (Function Arg): Function@Argument (left associative)
% abstraction lambda X.Term: X^Term (right associative)

% Variable convention: Q :: eta(a); F :: str --o str --o str; X,Y :: str; I :: x

% Notation: Source constant :: source type :: target term.

% Language: a^n b^n c^n d^n

% rule 0: S(xy) <- A(x,y).
0 :: s/a :: Q^(Q@(X^Y^I^(X@(Y@I)))).

% rule 1: A(axb,cyd) <- A(x,y).
1 :: a/a :: Q^F^(Q@(X^Y^(F@(I^(a@(X@(b@I))))@(I^(c@(Y@(d@I))))))).

% rule 2: A(e,e).
2 :: a :: F^(F@(I^I)@(I^I)).

% Language: w^2 (terminals: a, b)

% rule 3: S(xy) <- A(x,y).
3 :: s/a :: Q^(Q@(X^Y^I^(X@(Y@I)))).

% rule 4: A(ax,ay) <- A(x,y).
4 :: a/a :: Q^F^(Q@(X^Y^(F@(I^(a@(X@I)))@(I^(a@(Y@I)))))).

% rule 5: A(bx,by) <- A(x,y).
5 :: a/a :: Q^F^(Q@(X^Y^(F@(I^(b@(X@I)))@(I^(b@(Y@I)))))).

% rule 6: A(e,e).
6 :: a :: F^(F@(I^I)@(I^I)).

% Language: a^n b^m c^n d^m

7 :: (s/b)/a :: Q^Q1^(Q@(X^Y^(Q1@(Z^W^I^(X@(Z@(Y@(W@I)))))))).
8 :: a/a :: Q^F^(Q@(X^Y^(F@(I^(a@(X@I)))@(I^(c@(Y@I)))))).
9 :: a :: F^(F@a@a).
10 :: b/b :: Q^F^(Q@(X^Y^(F@(I^(b@(X@I)))@(I^(d@(Y@I)))))).
11 :: b :: F^(F@b@b).

% ============================================================
% Examples
% ============================================================

"0 1 1 2" ===> s. % aabbccdd
"3 4 5 5 6" ===> s. % abbabb
"7 8 9 10 10 11" ===> s. % aabbbccddd
