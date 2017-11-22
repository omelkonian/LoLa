% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.		% intransitief/onovergankelijk ww: 'dreams' ...
tv := iv/np.		% transitief/overgankelijk ww: 'teases' ...

% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

alice :: np.
tweedledum :: np.
tweedledee :: np.

queen :: n.
rabbit :: n.
hatter :: n.
gryphon :: n.
song :: n.

dreams :: iv.

% De woorden hieronder hebben nog geen type gekregen. Bedenk een
% geschikte formule, en vul die in waar nu een vraagteken staat.
% Haal het commentaarteken weg om de woorden in het lexicon te
% stoppen. Onderaan het document vind je de voorbeeldzinnen
% die je af wil kunnen leiden. 

the :: np/n.
nikkei :: n.
rises :: iv.

% a :: ?.

% mad :: ?.
% red :: ?.

% likes :: ?.
% teases :: ?.
% irritates :: ?.

% never :: ?.
% of :: ?.

% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================
% Als je oplossingen kloppen, kan je nu de zinnen
% hieronder afleiden, maar kan je geen slechte zinnen
% produceren.

"Alice dreams" ===> s.
"The rabbit never dreams" ===> s.
"Tweedledum irritates Tweedledee" ===> s.
"The Mad Hatter teases the Red Queen" ===> s.
"Alice likes the song of the Gryphon" ===> s.

% Voor de persoonlijke voornaamwoorden hieronder wil je formules die
% ervoor zorgen dat je wel "she teases him" maar niet
% "him teases she" kan afleiden!

% he :: ?.
% she :: ?.
% him :: ?.
% her :: ?.

"She likes Tweedledee" ===> s.
"Tweedledee likes her" ===> s.

% ============================================================
% Ambiguiteit
% ============================================================

i :: s/(np\s).
shot :: tv.
elephant :: n.
in :: (n\n)/np.
in :: (iv\iv)/np.
my :: np/n.
pajamas :: n.

% Groucho ("How he got in my pajamas, I'll never know.")

"I shot the elephant in my pajamas" ===> s.







