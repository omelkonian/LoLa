% Logische grammatica's. Lab Week 3

% ============================================================
% Lexicon: Woord :: Type :: Term
% ============================================================

% Voor Term kan je een lambda term invullen. 
% Notatie:

% Applicatie: M@N; lambda abstractie: X^M.

% De Term component is optioneel in je lexicale declaraties.
% Als hij ontbreekt, wordt de woordvorm Woord zelf gebruikt
% als constante.

% ============================================================
% Opdracht 1
% ============================================================

% Check je uitwerking van de Werkcollege opdrachten.

% 1.1

something :: s/(np\s).
ismissing :: (s/(np\s))\s.

% 1.2. Activeer postulaten P1/P2 hieronder voor Opgave 1.2

iedereen :: s/(np\s). % subject
iedereen :: (s/np)\s. % object
niemand :: s/(np\s). % subject
niemand :: (s/np)\s. % object
iets :: s/(np\s). % subject
iets :: (s/np)\s. % object
alles :: s/(np\s). % subject
alles :: (s/np)\s. % object
weet :: (np\s)/np.
kent :: (np\s)/np.

% ============================================================
% Postulaten
% ============================================================

% Structurele regels: Naam # In ---> Uit.
% De postulaten P1 en P2 maken van '*' een associatieve operatie.
% Als je deze activeert, kan je de haakjesstructuur van een zin veranderen. 
% P3 declareert '*' als een commutatieve operatie.
% L = NL + P1,P2
% LP = L + P3

%'P1' # (A * B) * C ---> A * (B * C).
%'P2' # A * (B * C) ---> (A * B) * C.
%'P3' # A * B ---> B * A.

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"something ismissing" ===> s. % Opg 1.1
"iedereen kent iemand" ===> s. % Opg 1.2, activeer P1,P2
"niemand weet alles" ===> s.

% ============================================================
% Opdracht 2
% ============================================================

/* Er is een standaard manier om strings te coderen als
lineaire lambda termen. String is een functietype *->*
(voor een willekeurig primitief type *). Concatenatie is
dan functiecompositie, en de lege string de identiteitsfunctie.
Voorbeeld: lambda term encodering voor "ababab" wordt dan
J^(a@(b@(a@(b@(a@(b@J)))))), met J de gebonden staart
variabele van type *.

Hieronder typeringen voor de gebalanceerde haakjestaal (Week 1,
haakje openen: 0; haakje sluiten: 1). Voeg lambda termen toe
waarmee je de omzetting van de testvoorbeelden hieronder
bereikt: de afleiding voor "000111" wordt omgezet in "ababab"
enzovoort.  

Deze opdracht laat zien dat compositionele interpretatie niet
beperkt is tot syntax->semantiek. In de opdracht vertaal je
strings over alfabet 0,1 op compositionele manier in strings
over alfabet a,b. */

%0 :: s/b :: Term?.
%0 :: (s/b)/s :: Term?.
%0 :: (s/s)/b :: Term?.
%0 :: ((s/s)/b)/s :: Term?.
1 :: b :: b. % of J^(b@J)

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"0 0 0 1 1 1" ===> s. % ababab
"0 1 0 1 0 1" ===> s. % aaabbb
"0 0 1 1 0 1" ===> s. % abaabb
"0 1 0 0 1 1" ===> s. % aababb
"0 0 1 0 1 1" ===> s. % aabbab

/* Uitwerking:

0 :: s/b :: B^J^(a@(B@J)).
0 :: (s/b)/s :: S^B^J^(S@(a@(B@J))).
0 :: (s/s)/b :: B^S^J^(a@(S@(B@J))).
0 :: ((s/s)/b)/s :: S1^B^S2^J^(S1@(a@(S2@(B@J)))).
1 :: b :: b. */