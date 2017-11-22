% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

mlift := ((a\c)\c)\(b\d).
mlower := a\(b\d).
% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

molly :: np.
thinks :: (np\s)/(s/(s\s)).
someone :: s/(np\s).
left :: np\s.

needs :: (np\s)/((s/np)\s).
something :: (s/np)\s.

aa :: a/a.
bb :: b/b.

% ============================================================
% Postulaten: 'Naam' # In ---> Uit.
% ============================================================
% bijvoorbeeld:

'Ass' # (A * B) * C ---> A * (B * C).
'Ass1' # A * (B * C) ---> (A * B) * C.

% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================








