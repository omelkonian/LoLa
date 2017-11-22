% Natuurlijke taalverwerking 2013. Week 3

% Stel in het bestand sources/options.pl de gewenste opties in.
% Bijvoorbeeld: 

% output_semantics(yes).
% output_subst_lex_sem(no). % voor bewijsterm; 
%                           % yes: vult meteen lexicale term in
% output_reduced_sem(yes).

% Draai dan ./install om die opties te activeren.

% ============================================================
% Macros: Afkorting := Type.
% ============================================================

iv := np\s.
tv := iv/np.
subj := s/iv.
obj := tv\iv.
qp := s/(np\s).
obj2 := tv\(qp\s).


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
% Slides 2/12
% ============================================================

% Niet-logische constanten

alice :: np.
poet :: n.
student :: n.
song :: n.
dreams :: iv.
admires :: tv.
pleases :: tv.
knows :: tv.
hurt :: obj.

% Vergelijk de lexicale termen hieronder met de slides.
% Je kan, tussen ' .. ', latex symbolen gebruiken voor de
% logische kwantificeerders. Kijk bovenaan voor de 
% afkortingen subj, obj, iv, tv.

every :: subj/n :: P^Q^('$\\forall$'@(X^((P@X) >> (Q@X)))).
%              of: P^Q^(all@(X^((P@X) >> (Q@X)))).

some :: subj/n :: P^Q^('$\\exists$'@(X^((P@X) /\ (Q@X)))).
no :: subj/n :: P^Q^(-('$\\exists$'@(X^((P@X) /\ (Q@X))))).


everyone :: subj :: Q^('$\\forall$'@(X^((person@X) >> (Q@X)))).
someone :: subj :: Q^('$\\exists$'@(X^((person@X) /\ (Q@X)))).

everything :: subj :: Q^('$\\forall$'@(X^((thing@X) >> (Q@X)))).
something:: subj :: Q^('$\\exists$'@(X^((thing@X) /\ (Q@X)))).

herself :: obj :: R^X^(R@X@X). % obj afkorting voor tv\iv

everyone :: obj :: R^X^('$\\forall$'@(Y^((person@Y) >> (R@Y@X)))).
someone :: obj :: R^X^('$\\exists$'@(Y^((person@Y) /\ (R@Y@X)))).	

everything :: obj :: R^X^('$\\forall$'@(Y^((thing@Y) >> (R@Y@X)))).
something:: obj :: R^X^('$\\exists$'@(Y^((thing@Y) /\ (R@Y@X)))).

that :: (n\n)/iv :: P^Q^X^((P@X) /\ (Q@X)).

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"every poet dreams" ===> s.
"no student knows everything" ===> s.
"Alice admires herself" ===> s.
"Alice admires someone" ===> s.

% grail wil een atomair doeltype.
% Maar dat mag wel een macro afkorting zijn.

"every song that pleases Alice" ===> subj.

% ============================================================
% Opdrachten 4 december
% ============================================================

% Hieronder, naar het Engelse voorbeeld, type+term voor
% Nederlands 'iedereen, iemand, niemand, alle' in hun rol als onderwerp
% van de zin (subject). Vul de ontbrekende termen in voor
% 'iets, iemand, alles, geen' in hun rol van lijdend voorwerp (object).

%iedereen :: subj :: Q^('$\\forall$'@(X^((persoon@X) >> (Q@X)))).
iedereen :: subj :: '$\\forall$'.

iemand :: subj :: Q^('$\\exists$'@(X^((persoon@X) /\ (Q@X)))).
niemand :: subj :: Q^(-('$\\exists$'@(X^((persoon@X) /\ (Q@X))))).
alle :: subj/n :: P^Q^('$\\forall$'@(X^((P@X) >> (Q@X)))).

iets :: obj :: R^X^('$\\exists$'@(Y^((ding@Y) /\ (R@Y@X)))).
iemand:: obj :: R^X^('$\\exists$'@(Y^((persoon@Y) /\ (R@Y@X)))).
iedereen:: obj :: R^X^('$\\forall$'@(Y^((persoon@Y) >> (R@Y@X)))).
alles :: obj :: R^X^('$\\forall$'@(Y^((ding@Y) >> (R@Y@X)))).
geen :: obj/n :: N^R^X^(-('$\\exists$'@(Y^((N@Y) /\ (R@Y@X))))).

iemand1 :: obj :: R^X^('$\\exists$'@(Y^(R@Y@X))).
iemand2 :: obj2 :: R^Q^('$\\exists$'@(Y^(Q@(X^(R@Y@X))))).

% Check je oplossingen met de testzinnen hieronder.

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"Alice kent geen dichters" ===> s.
"Iedereen weet iets" ===> s.
"Niemand weet alles" ===> s.

tweedledum :: np.
dichters :: n.
dromen :: iv.
danst :: iv.
zingt :: iv.
kent :: tv.
weet :: tv.
bewondert :: tv.
jent :: tv.
sart :: tv.
vond :: tv.
zocht :: (np\s)/(s/(np\s)).

% ============================================================
% Opdrachten, vervolg
% ============================================================

% Kameleon woorden zoals 'niet, en, of') hebben een type
% X/X, (X\X)/X dat zich aanpast aan de context, zie Slides 7, 8.
% Vul hieronder de goede typen en/of termen aan die je nodig
% hebt voor de gegeven voorbeeldzinnen.

niet :: subj/subj :: Q^P^(-(Q@P)). % voor: niet alle dichters dromen
niet :: obj/obj :: Obj^R^X^(-(Obj@R@X)). % voor: Tweedledum weet niet alles
of :: (s\s)/s :: P^Q^(Q \/ P). % voor: Iedereen danst of iedereen zingt
of :: (iv\iv)/iv :: P^Q^X^((Q@X) \/ (P@X)). % voor: Iedereen danst of zingt
en :: (tv\tv)/tv :: V1^V2^Y^X^((V2@Y@X) /\ (V1@Y@X)). % voor:  Alice jent en sart Tweedledum
%en :: (tv\tv)/tv :: V1^V2^Y^X^((V2@Y@X) /\ (V1@Y@X)). % voor: Alice zocht en vond iemand
%  zelfde type/term als de vorige: (np\s)/(s/(np\s)) (zocht) kan 'verlaagd' tot (np\s)/np

% Check je oplossingen met de testzinnen hieronder.

% ============================================================
% Test voorbeelden: Example ===> GoalType.
% ============================================================

"Niet alle dichters dromen" ===> s.
"Tweedledum weet niet alles" ===> s.
"Iedereen danst of iedereen zingt" ===> s.
"Iedereen danst of zingt" ===> s.
"Alice zocht iemand" ===> s.
"Alice vond iemand" ===> s.
"Alice jent en sart Tweedledum" ===> s.
"Alice zocht en vond iemand" ===> s.


