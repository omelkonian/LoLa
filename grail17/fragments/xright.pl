% Logische grammatica's Week 5. xright.pl: extracie uit rechtertakken

% Kies in sources/options.pl voor output_sr(no) als je de
% structurele stappen in stilte wil uitvoeren (zoals in
% de (xright) regel van de slides.

% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.
tv := iv/np.

% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.

alice :: np.

bed :: n.
speech :: n.
result :: n.
key:: n.

the :: np/n.

slept :: iv.
found :: tv.
counts :: iv/pp.

there :: iv\iv.

on :: pp/np.

in :: (iv\iv)/np.
during :: ( '[ ]' (iv\iv) )/np.

that :: (n\n)/(np\s) :: P^Q^X^((Q@X) /\ (P@X)). % girl that dreams
that :: (n\n)/(s/ <> '[ ]'np) :: P^Q^X^((Q@X) /\ (P@X)).
which :: (n\n)/(s/ <> '[ ]'np) :: P^Q^X^((Q@X) /\ (P@X)).

% Woorden voor de opgave:

carroll :: np.
wrote :: tv.
a :: np/n.
book :: n.
about :: (n\n)/np.
chess :: np.
game :: n.
sells :: iv.
well :: iv\iv.

% ============================================================
% Postulaten
% ============================================================

% xright: gecontroleerde extractie uit rechtertakken

'P1' # (A * B) * <> C ---> A * (B * <> C).
'P2' # (A * B) * <> C ---> (A * <> C) * B.
	

% ============================================================
% Voorbeelden
% ============================================================

"key that Alice found there" ===> n.
"the result that Alice counts on" ===> np.
"the speech that Alice slept during" ===> np.
"the bed that Alice slept in" ===> np.

% Opgave:

"Carroll wrote a book about chess" ===> s.
"A book about chess sells well" ===> s.
"game that Carroll wrote a book about" ===> n.
"game that sells well" ===> n.
"game that a book about sells well" ===> n.


