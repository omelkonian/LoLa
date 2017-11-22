:-[inputcat].

%:-[myfragment].

%% You can consult a file with lexical type declations here. 
%% You can use types for the syntactic calculus L (Lambek 1958)

dreams :: np\s.

%% Or pregroup types: product (list) of literals [Atom|Negations]

she :: [[s],[s,l],[np]].

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Translation: L types -> pregroup types

%%% t(Polarity,Formula:Term,NegationStack)

t(1,A*B:T,L)-->
	[link(par)],
	t(1,A:fst(T),L),
	t(1,B:snd(T),L).

t(1,A/B:T,L)-->
	{push(l,L,L1)},
	[link(times)],
	t(1,A:appl(T,U),L),
	t(0,B:U,L1).

t(1,B\A:T,L)-->
	{push(r,L,L1)},
	[link(times)],
	t(0,B:U,L1),
	t(1,A:appl(T,U),L).

t(0,A*B:pair(T,U),L)-->
	[link(times)],
	t(0,B:U,L),
	t(0,A:T,L).

t(0,A/B:lambda(V,T),L)-->
	{push(l,L,L1)},
	[link(par)],
	t(1,B:V,L1),
	t(0,A:T,L).

t(0,B\A:lambda(V,T),L)-->
	{push(r,L,L1)},
	[link(par)],
	t(0,A:T,L),
	t(1,B:V,L1).

t(1,Atom:Sem,L)-->[[Atom:Sem|L]],{atom(Atom)}.
t(0,Atom:Sem,L)-->[[Atom:Sem|L]],{atom(Atom)}.

%%% With depth counter

t(1,K,A*B:T,L)-->
	{K1 is K+1},
	[link(par)],
	t(1,K1,A:fst(T),L),
	t(1,K1,B:snd(T),L).

t(1,K,A/B:T,L)-->
	{K1 is K+1,
	push(l,L,L1)},
	[link(times)],
	t(1,K1,A:appl(T,U),L),
	t(0,K1,B:U,L1).

t(1,K,B\A:T,L)-->
	{K1 is K+1,
	push(r,L,L1)},
	[link(times)],
	t(0,K1,B:U,L1),
	t(1,K1,A:appl(T,U),L).

t(0,K,A*B:pair(T,U),L)-->
	{K1 is K+1},
	[link(times)],
	t(0,K1,B:U,L),
	t(0,K1,A:T,L).

t(0,K,A/B:lambda(V,T),L)-->
	{K1 is K+1,
	push(l,L,L1)},
	[link(par)],
	t(1,K1,B:V,L1),
	t(0,K1,A:T,L).

t(0,K,B\A:lambda(V,T),L)-->
	{K1 is K+1,
	push(r,L,L1)},
	[link(par)],
	t(0,K1,A:T,L),
	t(1,K1,B:V,L1).

t(1,K,Atom:Sem,L)-->[[Atom-K:Sem|L]],{atom(Atom)}.
t(0,K,Atom:Sem,L)-->[[Atom-K:Sem|L]],{atom(Atom)}.



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% push(Negation,NegStack,NewNegStack) pushes a Negation
%%% on the NegStack, performing simplifications on the way.

push(Neg,OldList,NewList):-
	(OldList=[Dual|List],cancel(Neg,Dual))
	->NewList=List
	;
	NewList = [Neg|OldList].

cancel(l,r).	% [l,r|T]=T
cancel(r,l).	% [r,l|T]=T

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Parsing is done by a non-deterministic PDA.

%%% NPDA, keeping track of derivational history

pda([],[])-->[([],[])].
pda([[H|H1]|T],[[Hs,l|H1]|R])-->	% reduce: l
	{substar([H|H1],[Hs,l|H1])},
	[([[H|H1]|T],[[Hs,l|H1]|R])],
	pda(T,R).
pda([[Hs,r|H1]|T],[[H|H1]|R])-->	% reduce: r
	{substar([H|H1],[Hs,r|H1])},
	[([[Hs,r|H1]|T],[[H|H1]|R])],
	pda(T,R).
pda([H|T],R)-->				% shift
	[([H|T],R)],
	pda(T,[H|R]).

%%% substar/2: generalized subsumption

%%% substar([Lit|Negs],[Lit1,Neg|Negs]) if
%%%	sub(Lit,Lit1) and Negs even
%%%	sub(Lit1,Lit) and Negs odd

substar([A],[A1,_]):-
	sub(A,A1).

substar([A,H|T],[A1,_,H|T]):-
	substar([A1|T],[A,_|T]).

%%% sub/2: subtyping at the literal level
%%% add nontrivial clauses for sub0/2

sub(Atom-_:Sem,Atom1-_:Sem) :- sub0(Atom,Atom1).

sub0(f,np).
sub0(m,np).
sub0(A,A).

%%%%%%%%%%%%%%%%%%%%%%%% Input/ Output %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% read/1 below expects a list of words and/or types.
% Last element of the input list is the goal type.
% The goal is right-negated.
% The NPDA checks whether the input contracts to 1.

tlist([Last],Sem,[tree|P],P1):-
	t(0,0,Last:Sem,[r],P,P1).

tlist([H|T],Sem,[tree|P],P1):-
	((H::Type)					% Type: type declaration for word H
		-> ((is_list(Type) -> 	% pregroup type (product of literals)
					l2diff(Type,P,P0)) ; 
					t(1,0,Type:_,[],P,P0)) % Type: syntactic calculus type
		; t(1,0,H:_,[],P,P0)		% H is syntactic calculus type
	),
	tlist(T,Sem,P0,P1).

nlist(L,L1,L2):-nlist(0,0,0,L,L1,L2). % add an index to the occurrences of literals

nlist(K,M,N,[[A-D:S|R]|T],[[A-K:S|R]|T1],[[A-(D/K):S|R]|T2]) :- 
	K1 is K+1,
	nlist(K1,M,N,T,T1,T2).
nlist(K,M,N,[link(Link)|T],[link(Link)-M|T1],T2) :- 
	M1 is M+1,
	nlist(K,M1,N,T,T1,T2).
nlist(K,M,N,[tree|T],[tree-N|T1],T2) :- 
	N1 is N+1,
	nlist(K,M,N1,T,T1,T2).
nlist(_,_,_,[],[],[]).

l2diff([],X,X). % list to diff list, for pregroup type input
l2diff([[H|Negs]|T],[[H:_|Negs]|R],S):-l2diff(T,R,S).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% pg_pda/0 prints out the steps of the automaton.

pda:-
	read(L),
	tell('pda.tex'),
	tlist(L,Sem,L1,[]),
	nlist(L1,L2),
	write('\\['),write_type_lst(L),write('\\]'),nl,
	write('\\[\\fbox{'),list_tex(L2),write('}\\]'),nl,nl,
	pda(L2,[],Proof,[]),
	tex_pda(Proof),nl,
	fail.
	
pda:-told,
	tell('proofspda.tex'),
	write('\\documentclass[12pt,a4paper]{article}'),nl,
	write('\\usepackage{proof}'),nl,
	write('\\usepackage{graphicx}'),nl,
	write('\\usepackage{amssymb}'),nl,
	write('\\usepackage{a4wide}'),nl,
	write('\\newcommand{\\bs}{\\backslash}'),nl,
	write('\\newcommand{\\ra}{\\rule{0pt}{7pt} \\Rightarrow}'),nl,
	write('\\newcommand{\\M}[1]{\\mbox{$#1$}}'),nl,
	write('\\begin{document}'),nl,
	write('\\input{pda}'),nl,
	write('\\end{document}'),nl,
	told,
	shell('pdflatex proofspda > /dev/null'),
	shell('open proofspda.pdf').

net:-
	read(L),
	tell('pgwires.tex'),
	tlist(L,Sem,L1,[]),
	nlist(L1,Trees,Literals),
	pda(Literals,[],Proof,[]),
	tikz(Literals,Trees,Proof),nl,
	fail.
	
net:-
	told,
	tell('wires.tex'),
	write('\\documentclass[]{beamer}'),nl,
%	write('\\usepackage[a4paper,landscape]{geometry}'),nl,
%	write('\\usepackage{tikz}'),nl,
	write('\\usepackage{tikz-qtree}'),nl,
	write('\\begin{document}'),nl,
	write('\\input{pgwires}'),nl,nl,
	write('\\vspace{1in}'),
	write('\\end{document}'),nl,
	told,
	shell('pdflatex wires > /dev/null'),
	shell('open wires.pdf').
	

tikz(Proof):-
	write('\\begin{frame}{Derivation}'),nl,
	write('\\[\\begin{tikzpicture}[node distance=20pt,text height=-2ex,text depth=.25ex,auto]'),
	nl,nl,
	write_literals(Proof),
	nl,nl,
	write_strings(Proof),
	nl,
	write('\\end{tikzpicture}\\]'),nl,
	write('\\end{frame}'),nl.
	
tikz(Literals,Trees,Proof):-
	write('\\begin{frame}[b]{Derivation}'),nl,
	write('\\[\\begin{tikzpicture}[scale=.8,grow\'=up]'),
	nl,nl,
	write_trees(Trees),
	nl,nl,
	write('\\pause'),
	nl,nl,
	write_strings(Literals,Proof),
	nl,
	write('\\end{tikzpicture}\\]'),nl,
	write('\\end{frame}'),nl.
	
write_trees(L):-
	append([[tree-0|Tree],[tree-1|Trees]],L),
	!,
	write('\\Tree '),
	write_tree(Tree),
%	write(' ]'),
	nl,
	write_trees([tree-1|Trees]).

write_trees(L):-
	append([[tree-I|Tree],[tree-J|Trees]],L),
	I>0,
	!,
	write('\\begin{scope}[shift={('),
	write(I),
	write('in,0in)}]'),nl,
	write('\\Tree '),
	write_tree(Tree),
%	write(' ]'),
	nl,
	write('\\end{scope}'),nl,
	write_trees([tree-J|Trees]).	

write_trees([tree-I|Tree]):-
	I>0,
	\+ (member(tree-_,Tree)),
	!,
	write('\\begin{scope}[shift={('),
	write(I),
	write('in,0in)}]'),nl,
	write('\\Tree '),
	write_tree(Tree),
%	write(' ]'),
	nl,
	write('\\end{scope}'),nl,nl.

% write_tree(L) :- write_lst(L).

write_tree([[Atom-I:_|Negs]]):-
	write('[.\\node('),
	write(n-I),
	write('){$'),
	write(Atom),
	write('^{'),
	write_neg(Negs),
	write('}$}; ] ').
write_tree([link(times)-I|R]):-
	write('[.\\node('),
	write(q-I),
	write('){$\\times$}; '),
	append(Left,Right,R),
	type(Left),type(Right),
	write_tree(Left),
	write_tree(Right),	
	write(' ] ').
write_tree([link(par)-I|R]):-
	write('[.\\node('),
	write(q-I),
	write('){$+$}; '),
	append(Left,Right,R),
	type(Left),type(Right),
	write_tree(Left),
	write_tree(Right),	
	write(' ] ').
	
write_neg(L) :- length(L,K),
	P is K mod 2,
	P=1 -> write('\\perp') ; true.

type(List):-type(List,[]).

type-->[[Atom-_:_|_]].
type-->[link(times)-_],type,type.
type-->[link(par)-_],type,type.

write_literals([(Literals,[])|_]):-list_literals(Literals).

list_literals([]).
list_literals([[Atom-0:_|Negs]|T]):-
	write('\\node (q-0) [label=above:$'),
	write(Atom),
	write('^{'),
	write_lst(Negs),
	write('}$] {};'),
	nl,
	list_literals(T).
	
list_literals([[Atom-I:_|Negs]|T]):-
	I>0,K is I-1,
	write('\\node (q-'),
	write(I),
	write(') [right of=q-'),
	write(K),
	write(',label=above:$'),
	write(Atom),
	write('^{'),
	write_lst(Negs),
	write('}$] {};'),
	nl,
	list_literals(T).
	
write_strings(_,[([],[])]).
write_strings(Lit,[([A|Tape],[B|Stack]),(Tape,Stack)|T]):-
	draw(Lit,A,B),nl,
	write_strings(Lit,[(Tape,Stack)|T]).
write_strings(Lit,[([A|Tape],Stack),(Tape,[A|Stack])|T]):-
	write_strings(Lit,[(Tape,[A|Stack])|T]).

draw(Lit,[_-(D/I):_|_],[_-(E/J):_|_]):-
	K is abs(I-J)-1,
	H is abs(D-E),
	h(Lit,I,J,P),
	(
	((D>=E,P>D) 
	-> P0 is P-D 
	; 
	((E>=D,P>E)
	-> P0 is P-E
	;
	P0=0
	))
	),
	M is (P0*(24/10))+(8/10)+(K*(2/10)),
	N is (P0*(24/10))+(H*(16/10))+(8/10)+(K*(2/10)),
	write('\\draw<+->[-] ('),
	write(n-I),
	write(')..controls +(north:'),
	(D=<E -> write(N) ; write(M)), 
	write(') and +(north:'),
	(E=<D -> write(N) ; write(M)),
	write(')..('),
	write(n-J),
	write(');').
	
h(Lit,I,J,0) :- 1 is abs(I-J).
h(Lit,I,J,P):-
	N is abs(I-J),N>1,
	setof(D,Atom^K^S^R^(member([Atom-(D/K):S|R],Lit),(I<J -> (I0=I,J0=J) ; (I0=J,J0=I) ),I0<K,K<J0),L),
	reverse(L,[P|_]).
	
tex_pda(Proof):-
	write('\\begin{center}\\begin{tabular}{r|l}'),nl,
	write_pda(Proof),
	write('\\end{tabular}\\end{center}'),nl.
	
write_pda([]).
write_pda([H|T]):-move_pda(H),nl,write_pda(T).

move_pda(([],[])):-!,
	write('$\\bot$ & $\\bot$').
	
move_pda((Tape,Stack)):-
	list_tex(Tape),
	write(' & '),
	list_tex(Stack),
	write('\\\\').

list_tex([]).

list_tex([H|T]):-
	item_tex1(H),
	list_tex(T).

item_tex1(Item):-
	write('\\M{'),
	item_tex2(Item),
	write('}\\ ').
	
item_tex2([H-_:_|T]):-
	write_a(H),
	write('^{'),
	write_lst(T),
	write('}').

write_lst([]).
write_lst([H|T]):-write(H),write_lst(T).

write_list([]).
write_list([H|T]):-write(H),nl,write_list(T).


write_a(A):-write(A).

write_ptype(A*B):-!,
       write('('),
       write_ptype(A),write('\\otimes '),write_ptype(B),
       write(')').
write_ptype(A/B):-!,
       write('('),
       write_ptype(A),write('\\slash '),write_ptype(B),
       write(')').
write_ptype(B\A):-!,
       write('('),
       write_ptype(B),write('\\backslash '),write_ptype(A),
       write(')').
write_ptype(Atom):-!,
	write(Atom).

write_type_lst([H1,H2]):-write_ptype(H1),write('\\Rightarrow '),write_ptype(H2).

write_type_lst([H|[H1,H2|T]]):-write_ptype(H),write(','),write_type_lst([H1,H2|T]).

%output_expl_brackets(yes).
 
