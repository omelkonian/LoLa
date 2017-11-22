% Logische grammatica's 2015. Lab Week 3

% ============================================================
% Lexicon: Woord :: Type :: Term
% ============================================================

% Voor Term kan je een lambda term invullen. Het type van
% Term is het semantisch type corresponderend met het
% syntactisch type Type.

% Notatie:

% Applicatie: M@N; lambda abstractie: X^M.

% In het abstractie geval is X de door lambda gebonden
% variabele. Dit is de Prolog conventie: hoofdletter
% betekent variabele.

% In de lambda calculus staat de functie voor zijn argument.
% Voor boolese operaties is er wat syntactische suiker:
% die kan je als infix schrijven:

% P en Q: P/\Q; 
% P of Q: P\/Q;
% P impliceert Q: P>>Q;
% niet P: -(P)
%
% De Term component is optioneel in je lexicale declaraties.
% Als hij ontbreekt, wordt de woordvorm Woord zelf gebruikt
% als constante.

% ============================================================
% Opdracht 1
% ============================================================

% Hieronder enkele propositieletters (p, q) en de boolese operaties
% (and, or, implies, not). Syntactisch type s correspondeert met
% t (waarheidswaarden).

% Voeg lambda termen toe voor and, or, implies en not, zo dat
% de afleiding voor de testzinnen vertaald worden
% naar de gebruikelijke propositielogische vorm. 

p :: s.
q :: s.
and :: (s\s)/s :: Q^P^(P /\ Q).
or :: (s\s)/s :: Q^P^(P \/ Q).
implies :: (s\s)/s :: Q^P^(P >> Q).
not :: s/s :: P^(-(P)).

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

%"p and not q" ===> s.
%"not p or q" ===> s. % twee afleidingen
%"not p and not p" ===> s. % twee afleidingen (T1)
%"p implies q implies not q implies not p" ===> s. % zeven afleidingen (T2)

% ============================================================
% Opdracht 2
% ============================================================

% Om de afleidingen hierboven ondubbelzinnig te maken, kan je
% haakjes toevoegen aan de syntax. Hieronder schrijven we 'd'
% voor haakje openen en 'b' voor haakje sluiten. De haakjes
% krijgen syntactisch type l (open) en r (sluit). Corresponderend
% semantisch type is telkens t->t. De interpretatie voor de
% haakjes is de identiteitsfunctie.

% Geef typeringen voor 'en' en 'impliceert' die ervoor zorgen
% dat er haakjes om een conjunctie/implicatie komen te staan.
% Geef bijpassende lambda termen. Schrijf de voorbeeldzinnen
% T1 en T2 hierboven zo dat de afleiding met de tautologische
% interpretatie wordt verbonden.

% Afkorting:

bs := (l\s)/r.

d :: l :: P^P.
b :: r :: P^P.
en :: (s\bs)/s :: Q^P^R^L^(R@(L@(P /\ Q))).
impliceert :: (s\bs)/s :: Q^P^R^L^(R@(L@(P >> Q))).
niet :: s/s :: P^(-(P)).

% ============================================================
% Opdracht 3
% ============================================================

% Een andere manier om dubbelzinnigheid te vermijden, is de
% Poolse notatie. In de Poolse prefix notatie staat een
% operatie voor zijn argumenten, in de postfix notatie erachter.

% Geef postfix typeringen voor de operaties hieronder, en
% lambda termen waarmee je een afleiding vertaalt naar de
% gebruikelijke propositielogische infix notatie. Geef de
% postfixnotatie voor de tautologische lezing van T1 en T2.

neg :: s\s :: P^(-(P)).
conj :: s\(s\s) :: Q^P^(P /\ Q).
disj :: s\(s\s) :: Q^P^(P \/ Q).
impl :: s\(s\s) :: Q^P^(P >> Q).

% ============================================================
% Opdracht 4
% ============================================================

Hieronder typeringen voor de gebalanceerde haakjestaal (Week 1,
haakje openen: 0; haakje sluiten: 1). Voeg lambda termen toe
waarmee je de omzetting van de testvoorbeelden hieronder
bereikt: de afleiding voor "000111" wordt omgezet in "ababab"
enzovoort. 

Gebruik de h_string vertaling (Slides 4/5, p33): atomaire
typen s, b worden vertaald in type string. String is een
functietype *->*, concatenatie is functie compositie.
De lambda term encodering voor "ababab" is dus
J^(a@(b@(a@(b@(a@(b@J)))))), met J de gebonden staart
variabele van type *. 

0 :: s/b :: B^J^(a@(B@J)).
0 :: (s/b)/s :: S^B^J^(S@(a@(B@J))).
0 :: (s/s)/b :: B^S^J^(a@(S@(B@J))).
0 :: ((s/s)/b)/s :: S1^B^S2^J^(S1@(a@(S2@(B@J)))).
1 :: b :: J^(b@J).

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"0 0 0 1 1 1" ===> s. % ababab
"0 1 0 1 0 1" ===> s. % aaabbb
"0 0 1 1 0 1" ===> s. % abaabb
"0 1 0 0 1 1" ===> s. % aababb
"0 0 1 0 1 1" ===> s. % aabbab
