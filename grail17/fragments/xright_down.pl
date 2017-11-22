% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

%iv := ( <> np)\s.
iv := np\s.
tv := iv/np.
sv := s/ <> '[ ]' np.
tvin := <> '[ ]' (s/(np*np)).
test := tv*(np*np). 

% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

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

needs :: iv/((s/np)\s).

something :: (s/ <> '[ ]' np)\s.

game :: n.
book :: n.
poem :: n.
chess :: np.
about :: (n\n)/np.
wrote :: tv.
read :: tvin.
carroll :: np.
a :: np/n.

sellswell :: iv.
and :: ((np*np)\(np*np))/<> (np*np).

in :: (iv\iv)/np.
during :: ( '[ ]' (iv\iv) )/np.

that :: (n\n)/iv :: P^Q^X^((Q@X) /\ (P@X)). % girl that dreams
that :: (n\n)/(s/ <> '[ ]'np) :: P^Q^X^((Q@X) /\ (P@X)).
which :: (n\n)/(s/ <> '[ ]'np) :: P^Q^X^((Q@X) /\ (P@X)).


% ============================================================
% Postulaten
% ============================================================

% xright: gecontroleerde extractie uit rechtertakken

%'P1' # A * (B * <> C) ---> (A * B) * <> C.
%'P2' # (A * <> C) * B ---> (A * B) * <> C.
	
'L1' # (<> C * B) * A ---> <> C * (B * A).
'L2' # B * (<> C * A) ---> <> C * (B * A).







