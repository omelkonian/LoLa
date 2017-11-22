% meanings.pl: examples for the Week 3 session.

% ============================================================
% Macros: Abbreviation := Type.
% ============================================================

iv := np\s.
tv := iv/np.
subj := s/(np\s).
obj := tv\iv.

% ============================================================
% Lexicon: Word :: Type (:: Meaning)
% ============================================================

% The Meaning component is optional. If you do not specify
% it, the word form itself will be used for meaning assembly.
% You will typically use this for non-logical constants.
% You can formulate a lexical lambda term, using the following
% notational conventions:
%
% application: M@N, abstraction: Var^Term
% pairing: (M,N), first/second projection: fst(M), snd(M)
% and: M/\N, or: M\/N, implies: M>>N, negation: -M
%
% As you see in the examples, you can omit brackets under the
% convention that abstraction associates to the right, and
% application to the left.

alice :: np.
lewis :: np.
dreams :: iv.
dream :: iv.
sleeps :: iv.
left :: iv.
girl :: n.
rabbit :: n.
poet :: n.
poets :: n.
book :: n.
irritates :: tv.
pleases :: tv.
reads :: tv.

everyone :: subj :: '$\\forall$'.
someone :: subj :: '$\\exists$'.
nobody :: subj :: P^(-('$\\exists$'@P)).

% If you want to distinguish 'someone'/'something',
% replace the above by:

%everyone :: subj :: Q^('$\\forall$'@(X^((person@X) >> (Q@X)))).
%someone :: subj :: Q^('$\\exists$'@(X^((person@X) /\ (Q@X)))).
%nobody :: subj :: Q^(-('$\\exists$'@(X^((person@X) /\ (Q@X))))).

%everything :: subj :: Q^('$\\forall$'@(X^((thing@X) >> (Q@X)))).
%something:: subj :: Q^('$\\exists$'@(X^((thing@X) /\ (Q@X)))).
%nothing :: subj :: Q^(-('$\\exists$'@(X^((thing@X) /\ (Q@X))))).

% Kwantificational determiners (subject)

some :: subj/n :: P^Q^('$\\exists$'@(X^((P@X) /\ (Q@X)))).
every :: subj/n :: P^Q^('$\\forall$'@(X^((P@X) >> (Q@X)))).
all :: subj/n :: P^Q^('$\\forall$'@(X^((P@X) >> (Q@X)))).
no :: subj/n :: P^Q^(-('$\\exists$'@(X^((P@X) /\ (Q@X))))).

alle :: subj/n :: P^Q^('$\\forall$'@(X^((P@X) >> (Q@X)))).
dichters :: n.
dromen :: iv.
geen :: obj/n :: D^R^A^(-('$\\exists$'@(X^((D@X) /\ (R@X@A))))).
kent :: tv.
bewondert :: tv.

iedereen :: subj :: '$\\forall$'.
	% Q^('$\\forall$'@(X^((persoon@X) >> (Q@X)))).
%iemand :: subj :: Q^('$\\exists$'@(X^((persoon@X) /\ (Q@X)))).
niemand :: subj :: Q^(-('$\\exists$'@(X^((persoon@X) /\ (Q@X))))).
weet :: tv. 
alles :: obj :: R^A^('$\\forall$'@(X^((ding@X) >> (R@X@A)))).
%iets :: obj :: R^A^('$\\exists$'@(X^((ding@X) /\ (R@X@A)))).
niet :: subj/subj :: Q^P^(-(Q@P)).
niet :: iv\iv :: P^X^(-(P@X)).

% Higher-order direct object NPs

%iets :: ob :: R^X^('$\\exists$'@(Y^(R@Y@X))).
iemand :: tv\(subj\s) :: R^Q^('$\\exists$'@(Y^(Q@(X^(R@Y@X))))).
 
% Reflexive pronouns (combinators: pure lambda term!)

herself :: obj :: R^X^(R@X@X). 
himself :: obj :: R^X^(R@X@X). 

% QPs in direct object position

somebody :: obj :: R^X^('$\\exists$'@(Y^(R@Y@X))).
everybody :: obj :: R^X^('$\\forall$'@(Y^(R@Y@X))).

something :: tv\(subj\s).
needs :: iv/subj.

isneeded :: subj\s.

% Relative pronoun: subject relativisation

%that :: (n\n)/(np\s) :: X^Y^Z^( (X@Z) /\ (Y@Z) ).

that :: (n\n)/(s/ <> '[ ]'np) :: P^Q^X^((Q@X) /\ (P@X)).

%that :: ((n\n)/tv)/np :: Subj^TV^N^X^( (TV@X@Subj) /\ (N@X) ).
% ============================================================
% Test examples: Example ===> GoalType.
% ============================================================

"All poets dream" ===> s.
"No poet sleeps" ===> s.
"Alice irritates herself" ===> s.
"Alice irritates everybody" ===> s.
"Everyone irritates himself" ===> s.
"Everyone irritates everybody" ===> s.

% ./grail at the command line accepts only atomic goals
% But you can use a macro definition for a complex goal formula

"some book that pleases Alice" ===> subj.

% xright: gecontroleerde extractie uit rechtertakken

'P1' # (A * B) * <> C ---> A * (B * <> C).
'P2' # (A * B) * <> C ---> (A * <> C) * B.


