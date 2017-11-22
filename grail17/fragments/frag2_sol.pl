% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

iv := np\s.		% intransitief/onovergankelijk ww: 'dreams' ...
tv := iv/np.		% transitief/overgankelijk ww: 'teases' ...
subj := s/(np\s).
obj := tv\iv. % ((np\s)/np)\(np\s).

% ============================================================
% Lexicon: je woordenboek
% ============================================================

% Woord :: Formule.
% Beperk je tot de volgende atomaire formules:
% s (zin), np (naam: "Alice"), n (zelfstandig naamwoord: "girl").

alice :: np.
tweedledum :: np.
tweedledee :: np.
jim :: np.
noam :: np.

queen :: n.
hatter :: n.
book :: n.
girl :: n.
mathematician :: n.
linguist :: n.

dreams :: iv.
snores :: iv.
left :: iv.

% De woorden hieronder hebben nog geen type gekregen. Bedenk een
% geschikte formule, en vul die in waar nu een vraagteken staat.
% Haal het commentaarteken weg om de woorden in het lexicon te
% stoppen. Onderaan het document vind je de voorbeeldzinnen
% die je af wil kunnen leiden. 

the :: np/n.
a :: np/n.

mad :: n/n.
red :: n/n.
nice :: n/n.
boring :: n/n.

teases :: (np\s)/np. % afkorting: tv
irritates :: tv.
saw :: tv.
hit :: tv.
hits :: tv
wrote :: tv.

% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================
% Als je oplossingen kloppen, kan je nu de zinnen
% hieronder afleiden, maar kan je geen slechte zinnen
% produceren.

"Alice dreams" ===> s.
"The Red Queen snores" ===> s.
"Alice teases the Mad Hatter" ===> s.

% Voor de persoonlijke voornaamwoorden hieronder wil je formules die
% ervoor zorgen dat je wel "she teases him" maar niet
% "him teases she" kan afleiden!

he :: subj. % afkorting voor s/(np\s)
she :: subj.
him :: obj. % afkorting voor ((np\s)/np)\(np\s)
her :: obj.

"She irritates Tweedledee" ===> s.
"Tweedledee irritates her" ===> s.

% Betrekkelijke voornaamwoorden. Bedenk eerst een goede formule
% voor de betrekkelijke bijzin: dat is een bepaling bij een naamwoord,
% net zoals een bijvoeglijk naamwoord, alleen: de bijzin volgt op het
% naamwoord, het adjectief gaat eraan vooraf. Als je een type hebt
% voor de betrekkelijke bijzin is het makkelijk om daaruit weer het
% type voor het betrekkelijk voornaamwoord af te leiden.

that :: (n\n)/(np\s).
	% subject relativisering
	% zoals in "the song that irritates Alice"
	
% In de basislogica NL zal je voor objectrelativisering
% een ander type voor "that" nodig hebben. Bijvoorbeeld:

%that :: ((n\n)/tv)/np. 
	% zoals in "the tarts that Alice stole"
	
% Die dubbele typeringen zijn  niet echt bevredigend.
% Wat doe je bijvoorbeeld met: "the tarts that she stole" ..

song :: n.
tarts :: n.
stole :: tv.

that :: (n\n)/(s/np).

"the song that irritates the Red Queen" ===> np.
"the tarts that Alice stole" ===> np.
"the tarts that she stole" ===> np.

% ============================================================
% Ambiguiteit
% ============================================================

% De zin hieronder kan op twee manieren begrepen worden: is
% "with the telescope" een werkwoordelijke of een naamwoordelijke
% bepaling. De betekenis van "sees"/"hits" maakt telkens een van
% beide lezingen meer waarschijnlijk. Breid je lexicon uit: je
% zal voor "with" op twee verschillende typen uitkomen. Test
% dan de zinnen hieronder.

man :: n.
telescope :: n.
with :: (n\n)/np. 
	% voor "man with the telescope"
with :: (iv\iv)/np.
	% voor "hits the man with the telescope"

"Alice saw the man with the telescope" ===> s.
"Alice hit the man with the telescope" ===> s.

% ============================================================
% Postulaten
% ============================================================

% Structurele regels: Naam # In ---> Uit.
% De postulaten P1 en P2 maken van '*' een associatieve operatie.
% Als je deze activeert, kan je de haakjesstructuur van een zin veranderen. 
% P3 declareert '*' als een commutatieve operatie.
% L = NL + P1,P2
% LP = L + P3

'P1' # (A * B) * C ---> A * (B * C).
%'P2' # A * (B * C) ---> (A * B) * C.
%'P3' # A * B ---> B * A.

% Hieronder enkele nieuwe testzinnen.

"She likes herself" ===> s.
"*Herself likes Alice" ===> s. % geen oplossing!
"Alice cares about herself" ===> s.

% Vul ontbrekende typeringen in waarmee je de voorbeeldzinnen kan
% afleiden. Check dat "herself likes Alice" geen oplossing heeft.
% Activeer een van de Associativiteitsregels (P1 of P2)
% en laat zien dat je met een enkele typering voor "herself"
% zowel "She likes herself" als "Alice cares about herself"
% kan afleiden.

likes :: tv.
cares :: iv/pp.
		% pp: voorzetselgroep (prepositional phrase)
about :: pp/np.
herself :: tv\iv.

% Hieronder enkele nieuwe woorden met hun type.

knows :: (np\s)/w. % w: ingebedde wh-np
who :: w/(np\s).

"Tweedledum knows who left" ===> s.

% Geef een type voor "what" waarmee de testzinnen
% hieronder afleidbaar worden, gegeven de Associativiteitsregel
% die je eerder hebt geactiveerd.

what :: w/(s/np).

"Tweedledum knows what Alice likes" ===> s.
"Tweedledum knows what Alice cares about" ===> s.



