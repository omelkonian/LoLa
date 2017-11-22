% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.


% ============================================================
% Lexicon: abstract constants
% ============================================================

beer :: (s/ <> '[ ]' b)\ s :: Q^I^((Q@(J^J))@(b@I)).
peer :: (s/ <> '[ ]' c)\ s :: Q^I^((Q@(J^J))@(p@I)).

%beer :: (s/ <> '[ ]' b)\ s :: Q^(Q@b).
%peer :: (s/ <> '[ ]' c)\ s :: Q^(Q@p).

beer :: ((s/s)/ <> '[ ]' b)\ (s/s) :: Q^S^I^((Q@b)@(S@I)).
peer :: ((s/s)/ <> '[ ]' c)\ (s/s) :: Q^S^I^((Q@p)@(S@I)).


be :: b :: I^(b@I).
pe :: c :: I^(p@I).

de :: s/b :: S^I^(d@(S@I)).
de :: (s/s)/b :: S1^S2^I^(d@(S1@(S2@I))).
de :: (s/b)/s :: S1^S2^I^(d@(S1@(S2@I))).
de :: ((s/s)/b)/s :: S1^S2^S3^I^(d@(S1@(S2@(S3@I)))).

qu :: s/c :: S^I^(q@(S@I)).
qu :: (s/s)/c :: S1^S2^I^(q@(S1@(S2@I))).
qu :: (s/c)/s :: S1^S2^I^(q@(S1@(S2@I))).
qu :: ((s/s)/c)/s :: S1^S2^S3^I^(d@(S1@(S2@(S3@I)))).


% ============================================================
% Postulates
% ============================================================

% xright

'P1' # (A * B) * <> C ---> A * (B * <> C).
'P2' # (A * B) * <> C ---> (A * <> C) * B.

% ============================================================
% Examples
% ============================================================

"de de de be be be" ===> s.
"de de qu be be pe" ===> s.
"de de qu be pe be" ===> s.
"de de qu pe be be" ===> s.
"de de be de be be" ===> s.
"de de be qu be pe" ===> s.
"de de be qu pe be" ===> s.
"de de be be de be" ===> s.
"de de be be qu pe" ===> s.
"de qu de be be pe" ===> s.
"de qu de be pe be" ===> s.
"de qu de pe be be" ===> s.
"de qu qu be pe pe" ===> s.
"de qu qu pe be pe" ===> s.
"de qu qu pe pe be" ===> s.
"de qu be de be pe" ===> s.
"de qu be de pe be" ===> s.
"de qu be qu pe pe" ===> s.
"de qu be pe de be" ===> s.
"de qu be pe qu pe" ===> s.
"de qu pe de be be" ===> s.
"de qu pe qu be pe" ===> s.
"de qu pe qu pe be" ===> s.
"de qu pe be de be" ===> s.
"de qu pe be qu pe" ===> s.
"de be de de be be" ===> s.
"de be de qu be pe" ===> s.
"de be de qu pe be" ===> s.
"de be de be de be" ===> s.
"de be de be qu pe" ===> s.
"de be qu de be pe" ===> s.
"de be qu de pe be" ===> s.
"de be qu qu pe pe" ===> s.
"de be qu pe de be" ===> s.
"de be qu pe qu pe" ===> s.
"qu de de be be pe" ===> s.
"qu de de be pe be" ===> s.
"qu de de pe be be" ===> s.
"qu de qu be pe pe" ===> s.
"qu de qu pe be pe" ===> s.
"qu de qu pe pe be" ===> s.
"qu de be de be pe" ===> s.
"qu de be de pe be" ===> s.
"qu de be qu pe pe" ===> s.
"qu de be pe de be" ===> s.
"qu de be pe qu pe" ===> s.
"qu de pe de be be" ===> s.
"qu de pe qu be pe" ===> s.
"qu de pe qu pe be" ===> s.
"qu de pe be de be" ===> s.
"qu de pe be qu pe" ===> s.
"qu qu de be pe pe" ===> s.
"qu qu de pe be pe" ===> s.
"qu qu de pe pe be" ===> s.
"qu qu qu pe pe pe" ===> s.
"qu qu pe de be pe" ===> s.
"qu qu pe de pe be" ===> s.
"qu qu pe qu pe pe" ===> s.
"qu qu pe pe de be" ===> s.
"qu qu pe pe qu pe" ===> s.
"qu pe de de be be" ===> s.
"qu pe de qu be pe" ===> s.
"qu pe de qu pe be" ===> s.
"qu pe de be de be" ===> s.
"qu pe de be qu pe" ===> s.
"qu pe qu de be pe" ===> s.
"qu pe qu de pe be" ===> s.
"qu pe qu qu pe pe" ===> s.
"qu pe qu pe de be" ===> s.
"qu pe qu pe qu pe" ===> s.



