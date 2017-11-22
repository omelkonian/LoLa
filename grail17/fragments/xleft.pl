% Logische grammatica's Week 5. xleft.pl: extracie uit linkertakken

% Kies in sources/options.pl voor output_sr(no) als je de
% structurele stappen in stilte wil uitvoeren (zoals in
% de (xleft) regel van de slides.

% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.
tv := np\iv.
rel := n\n.

relpro := rel/(<> '[ ]'np \ s).

% ============================================================
% Lexicon: je woordenboek
% ============================================================

alice :: np.
lakei :: n.
resultaat :: n.

de :: np/n.
het :: np/n.
dit :: np/n.

plaagt :: tv.
rekent :: pp\iv.
op :: pp/np.
niet :: iv/iv :: P^X^(-(P@X)).

dat :: relpro :: P^Q^X^((Q@X) /\ (P@X)).
die :: relpro :: P^Q^X^((Q@X) /\ (P@X)).

% Voeg de volgende woorden toe aan het lexicon:

% waar :: Type? :: Term?.
% er :: Type? :: Term?.

% ============================================================
% Postulaten
% ============================================================

% xleft: gecontroleerde extractie uit linkertakken

'L1' # <> C * (B * A) ---> (<> C * B) * A.
'L2' # <> C * (B * A) ---> B * (<> C * A).
	
% ============================================================
% Voorbeelden
% ============================================================

% Type s staat hier voor bijzin: werkwoord achteraan.
% Je kan de s voorbeelden laten voorafgaan met "Ik weet dat ..."

"Alice de lakei plaagt" ===> s.
"Alice op dit resultaat rekent" ===> s.
"Alice er op rekent" ===> s.
"de lakei die Alice plaagt" ===> np.
"het resultaat waar Alice op rekent" ===> np.
"het resultaat dat Alice op rekent" ===> np.
"Alice er niet op rekent" ===> s.




