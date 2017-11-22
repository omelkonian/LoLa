% Logische grammatica's. Lab Week 4

% ============================================================
% Macros: Afkorting := Type.
% ============================================================

iv := np\s.
tv := iv/np.
subj := s/iv.
obj1 := tv\iv.
obj2 := tv\(subj\s).

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
% OPDRACHT I 
% ============================================================

/* Maak de gevraagde afleidingen voor de Werkcollege opdracht.

Stel in het bestand sources/options.pl de gewenste opties in.
Bijvoorbeeld: 

output_semantics(yes).
output_subst_lex_sem(no). % voor bewijsterm; 
                          % yes: vult meteen lexicale term in
output_reduced_sem(yes). % stapsgewijze beta-vereenvoudiging

Draai dan ./install om gewijzigde opties te activeren.

De gevonden afleidingen vind je in ./sources als egn.tex.
Zorg dat je de commando's hieronder in je werkcollege *.tex
document hebt

\newcommand{\bs}{\backslash}
\newcommand{\bo}{[}
\newcommand{\bc}{]}

Voor afleidingen die te breed worden voor A4 gebruik je
sidewaysfigure uit het pakket rotating.sty. Je laadt het
pakket in de preamble van je document:

\usepackage{rotating}

Een gekanteld figuur gaat dan zo:

\begin{sidewaysfigure}
\begin{center}
... hier je brede Grail derivatie ...
\end{center}
\caption{...}
\label{...}
\end{sidewaysfigure} */

% Opdracht 2.1

iedereen :: subj :: '$\\forall$'.
bewondert :: tv.
iemand1 :: obj1 :: R^X^('$\\exists$'@(Y^(R@Y@X))).
% iemand2 :: obj2 :: R^Q^Term?.

% Opdracht 2.2

lewis :: np.
thinks :: iv/s.
somebody1 :: subj :: '$\\exists$'.
somebody2 :: ((iv/s)\iv)/iv :: P^R^Y^('$\\exists$'@(X^(R@(P@X)@Y))).
left :: iv.

% Opdracht 2.3

iedereen0 :: np :: '$\\forall$'.
iemand0 :: np :: '$\\exists$'.
bewondert1 :: tv :: Q1^Q2^(Q1@(Y^(Q2@(X^(bewondert@Y@X))))).
bewondert2 :: tv :: Q1^Q2^(Q2@(X^(Q1@(Y^(bewondert@Y@X))))).

lewis1 :: np :: P^(P@lewis).
thinks1 :: iv/s :: P^Q^(Q@(X^(thinks@P@X))).
sombebody2 :: np :: '$\\exists$'.
left1 :: iv :: Q^(Q@left).


% ============================================================
% OPDRACHT II. Abstract Categorial Grammar
% ============================================================

% Voorbeeld: CFG voor gebalanceerde haakjes

c1 :: s/s :: X^I^(a@(X@(b@I))). % S -> a S b
c2 :: (s/s)/s :: X^Y^I^(X@(Y@I)). % S -> S S
c3 :: s :: I^I. % S -> epsilon

% test

"c1 c2 c1 c3 c1 c3" ===> s % vertaling: aababb

/* Hieronder de ACG encodering van een 2-MCFG voor a^n b^n c^n d^n
zoals besproken in het hoorcollege (cf Slides).
De targettaal gebruikt een type str(ing), gedefinieerd als *->*.
Vertaling van de source atomen is h(s)=str, h(a)=(str->str->str)->str.
In de lexicale vertalingen schrijven we de afkortingen uit: '+' voor string
concatenatie (=functie compositie) en epsilon (=identiteitsfunctie) voor
de lege string. Variabelen I,J hebben dus type *. De eindsymbolen
a,b,c,d hebben type str. */

0 :: s/a :: Q^(Q@(X^Y^I^(X@(Y@I)))).
1 :: a/a :: Q^F^(Q@(X^Y^((F@(I^('$a$'@(X@('$b$'@I)))))@(J^('$c$'@(Y@('$d$'@J))))))).
2 :: a :: F^((F@(J^J))@(J^J)).

% test voorbeeld:

"0 1 1 2" ===> s. % vertaling: aabbccdd

% Opdracht

% Geef een ACG voor de taal a^n b^m c^n d^m.

% Geef een afleiding voor het rijtje aabbbccddd.


