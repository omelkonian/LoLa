% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.		% intransitief/onovergankelijk ww: 'dreams' ...
tv := iv/np.		% transitief/overgankelijk ww: 'teases' ...
subj := s/iv.  % onderwerp: 'I', 'he',...
adv := iv\iv.
% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

i :: s/(np\s). % kleine letters voor prolog atomen!
shot :: tv.
the :: np/n.
elephant :: n.
in :: (n\n)/np. % modificeerder bij n
in :: (iv\iv)/np.  % mod bij gezegde: lexicale ambiguiteit
my :: np/n.
pajamas :: n.
put :: (iv/adv)/np.
groucho :: np.

% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================

% Groucho ("How he got in my pajamas, I'll never know.")

"I shot the elephant" ===> s.
"I shot the elephant in my pajamas" ===> s.







