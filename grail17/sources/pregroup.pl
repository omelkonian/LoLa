:-[inputcat,mm_common_tex].

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% t(Polarity,Formula:Term,NegationStack)

t(1,A*B:T,L)-->
	t(1,A:fst(T),L),
	t(1,B:snd(T),L).

t(1,A/B:T,L)-->
	{push(l,L,L1)},
	t(1,A:appl(T,U),L),
	t(0,B:U,L1).

t(1,B\A:T,L)-->
	{push(r,L,L1)},
	t(0,B:U,L1),
	t(1,A:appl(T,U),L).

t(0,A*B:pair(T,U),L)-->
	t(0,B:U,L),
	t(0,A:T,L).

t(0,A/B:lambda(V,T),L)-->
	{push(l,L,L1)},
	t(1,B:V,L1),
	t(0,A:T,L).

t(0,B\A:lambda(V,T),L)-->
	{push(r,L,L1)},
	t(0,A:T,L),
	t(1,B:V,L1).

t(1,Atom:Sem,L)-->[[Atom:Sem|L]],{atom(Atom)}.
t(0,Atom:Sem,L)-->[[Atom:Sem|L]],{atom(Atom)}.

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

tlist([Last],Sem,P,P1):-!,
	t(0,Last:Sem,[r],P,P1).

tlist([H|T],Sem,P,P1):-
	t(1,H:_,[],P,P0),
	tlist(T,Sem,P0,P1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% NPDA for pregroup cancellation

pda([],[]).
pda([[H|H1]|T],[[H,l|H1]|R]):-
	pda(T,R).
pda([[H,r|H1]|T],[[H|H1]|R]):-
	pda(T,R).
pda([H|T],R):-
	pda(T,[H|R]).

%%% Keeping track of derivational history

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

sub(Atom:Sem,Atom1:Sem) :- sub0(Atom,Atom1).

sub0(f,np).
sub0(m,np).
sub0(A,A).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
tex:-
	read(L),
	tell('pda.tex'),
	tlist(L,Sem,L1,[]),
	write('\\['),write_type_lst(L),write('\\]'),nl,
	write('\\[\\fbox{'),list_tex(L1),write('}\\]'),nl,nl,
	pda(L1,[],Proof,[]),
	tex_pda(Proof),nl,
	numbervars(Sem,1,_),
	write('\\['),
	write_sem(Sem),
	write('\\]'),
	fail.
	
tex:-told,
	shell('pdflatex proofspda > /dev/null'),
	shell('open proofspda.pdf').

test:-
	read(L),
	tlist(L,Sem,L1,[]),
	write('\\['),write_type_lst(L),write('\\]'),nl,
	write('\\[\\fbox{'),list_tex(L1),write('}\\]'),nl,nl,
	pda(L1,[],Proof,[]),
	tex_pda(Proof),nl,
	numbervars(Sem,1,_),
%	write('\['),
%	write_sem(Sem),
%	write('\]'),
	fail.
	
test.

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
	
item_tex2([H:_|T]):-
	write_a(H),
	write('^{'),
	write_lst(T),
	write('}').

write_lst([]).
write_lst([H|T]):-write(H),write_lst(T).

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

% latex :- shell('latex proofspda').
latex:-true.
% xdvi:-shell('xdvi proofspda &').
xdvi:-true.
