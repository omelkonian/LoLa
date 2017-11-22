% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.
tv := np\iv.
rel := n\n.
rpro := pp/(pp/np).

relpro := rel/( ( <> '[ ]' np ) \ s).
relrpro := (n\n)/( ( <> '[ ]' rpro ) \ s).

% ============================================================
% Lexicon: je woordenboek
% ============================================================

alice :: np.
lakei :: n.
resultaat :: n.
dokter :: n.
patient :: n.

de :: np/n.
het :: np/n.
dit :: np/n.

begroette :: tv.
genas :: tv.

plaagt :: tv.
rekent :: pp\iv.
op :: pp/np.
niet :: iv/iv :: P^X^(-(P@X)).

dat :: relpro :: P^Q^X^((Q@X) /\ (P@X)).
die :: relpro :: P^Q^X^((Q@X) /\ (P@X)).

waar :: relrpro :: P^Q^X^((Q@X) /\ (P@(Y^(Y@X)))).

dr :: pp/(pp/np) :: Y^(Y@'$d$').

er :: iv/( ( <> '[ ]' rpro ) \ iv) :: P^X^(P@(Y^(Y@'$d$'))@X).

% ============================================================
% Postulaten
% ============================================================

% xleft: gecontroleerde extractie uit linkertakken

'L1' # <> C * (B * A) ---> (<> C * B) * A.
'L2' # <> C * (B * A) ---> B * (<> C * A).
	
% ============================================================
% Voorbeelden
% ============================================================

"Alice de lakei plaagt" ===> s.
"Alice op dit resultaat rekent" ===> s.
"Alice er op rekent" ===> s.
"de lakei die Alice plaagt" ===> np.
"het resultaat waar Alice op rekent" ===> np.
"het resultaat dat Alice op rekent" ===> np.
"Alice er niet op rekent" ===> s.




