% Natuurlijke taalverwerking 2013. Week 3

% ============================================================
% Macros: Afkorting := Type.
% ============================================================


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
% Opdracht 27/11
% ============================================================

% Hieronder drie propositieletters (p, q, r) en de boolese
% operaties (and, or, not). Syntactisch type s correspondeert
% met t (waarheidswaarden).

% Voeg lambda termen toe voor and, or en not, zo dat
% de afleiding voor de testzinnen vertaald worden
% naar de gebruikelijke propositielogische vorm. 

p :: s.
q :: s.
r :: s.
% and :: (s\s)/s :: Term?.
% or :: (s\s)/s :: Term?.
% not :: s/s :: Term?.

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"p and not q" ===> s.
"not p or q" ===> s. % twee afleidingen
"not p and not p" ===> s. % twee afleidingen


