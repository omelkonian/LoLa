% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.		% intransitief/onovergankelijk ww: 'dreams' ...
tv := iv/np.		% transitief/overgankelijk ww: 'teases' ...
subj := s/iv.  % onderwerp: 'I', 'he',...
obj := tv\iv. % lijdend voorwerp, reflexief pronomen
adv := iv\iv.

% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

alice :: np.
tweedledum :: np.
hurt :: tv.
herself :: obj.
looks :: iv/pp.
after :: pp/np.
thinks :: iv/s.
that :: s/s.
likes :: tv.
knows :: iv/wh.
what :: wh/(s/np).
found :: tv.
there :: adv.

treasure :: n.
that :: (n\n)/(s/np).

1 :: np.
2 :: tv.
3 :: obj.
4 :: iv/pp.
5 :: pp/np.

% ============================================================
% Postulaten
% ============================================================

'Ar' # (A * B) * C ---> A * (B * C).
'Cr' # (A * B) * C ---> (A * C) * B.
	
% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================

"Alice hurt herself" ===> s.
"Alice looks after herself" ===> s.
"Alice thinks that Tweedledum likes herself" ===> s.
"Tweedledum knows what Alice found" ===> s.
"Tweedledum knows what Alice found there" ===> s.







