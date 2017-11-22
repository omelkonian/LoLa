% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

subj := s/iv.
rgap := s/ <>'[ ]'np.
iv := np\s.
tv := iv/np.

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

the :: np/n :: '$\\iota$'.
a :: np/n.

some :: subj/n.

mad :: n/n.
red :: n/n.

likes :: tv.
teases :: tv.
irritates :: tv.

never :: iv/iv.
of :: (n\n)/np.

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

he :: s/iv.
she :: s/iv.
him :: tv\iv.
her :: tv\iv.

"She likes Tweedledee" ===> s.
"Tweedledee likes her" ===> s.

% Betrekkelijke voornaamwoorden. Bedenk eerst een goede formule
% voor de betrekkelijke bijzin: dat is een bepaling bij een naamwoord,
% net zoals een bijvoeglijk naamwoord, alleen: de bijzin volgt op het
% naamwoord, het adjectief gaat eraan vooraf. Als je een type hebt
% voor de betrekkelijke bijzin is het makkelijk om daaruit weer het
% type voor het betrekkelijk voornaamwoord af te leiden.

that :: (n\n)/iv.
% that :: ?. % zoals in "the tarts that Alice stole"

% Je zal twee verschillende oplossingen voor "that" nodig hebben!

"the song that irritates the Red Queen" ===> np.
"the song that Alice likes" ===> np.

someone :: s/iv :: x.
ismissing :: (s/iv)\s :: y.

% ============================================================
% Postulaten
% ============================================================

% Dit is stof voor Set 3 van de Oefeningen. Je kan er alvast
% even over nadenken.

% Structurele regels: Naam # In ---> Uit.
% Voorbeeld: Associativiteit. Als je deze activeert, kan je de
% haakjesstructuur van een zin veranderen. 

%'P1' # (A * B) * <> C ---> A * (B * <> C).
%'P2' # (A * B) * <> C ---> (A * <> C) * B.
	
that :: (n\n)/(s/ <> '[ ]'np) ::P^Q^X^((Q@X) /\ (P@X)).

% ============================================================
% Ambiguiteit
% ============================================================

% De zin hieronder kan op twee manieren begrepen worden: is
% "with the telescope" een werkwoordelijke of een naamwoordelijke
% bepaling. De betekenis van "sees"/"hits" maakt telkens een van
% beide lezingen meer waarschijnlijk. Breid je lexicon uit: je
% zal voor "with" op twee verschillende typen uitkomen. Test
% dan de zinnen hieronder.

i :: s/(np\s).
shot :: tv.
elephant :: n.
in :: (n\n)/np.
in :: (iv\iv)/np.
my :: np/n.
pajamas :: n.


"I shot the elephant in my pajamas" ===> s.







