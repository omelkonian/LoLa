/* Reference
@incollection{
year={2014},
isbn={978-3-642-54788-1},
booktitle={Categories and Types in Logic, Language, and Physics},
volume={8222},
series={Lecture Notes in Computer Science},
editor={Casadio, Claudia and Coecke, Bob and Moortgat, Michael and Scott, Philip},
doi={10.1007/978-3-642-54789-8_16},
title={A Note on Multidimensional Dyck Languages},
url={http://dx.doi.org/10.1007/978-3-642-54789-8_16},
publisher={Springer Berlin Heidelberg},
author={Moortgat, Michael},
pages={279-296}
} */


% D^3: 3-dimensional Dyck words
% Input alphabet: {a,b,c}, with a<b<c.
% Words w in D^3 satisfy: 
% 	- #a(w) = #b(w) = #c(w)
%   - for w= uv, #a(u) >= #b(u) >= #c(u)

% 2-counter machine
% counter: non-negative number in successor notation; initial stack symbol 0

dyck3(0,0) --> []. % accept: input consumed; counters zero
dyck3(S,T) --> [a], % read a
	dyck3(s(S),T). % push/increment counter 1
dyck3(s(S),T) --> [b], % read b
	dyck3(S,s(T)). % pop/decrement counter 1; push counter 2
dyck3(S,s(T)) --> [c], % read c
	dyck3(S,T). % pop counter 2 

% the same, but keeping the derivational history

dyck3(0,0,[]) --> [([],0,0)].
dyck3(S,T,[a|R]) -->
	[([a|R],S,T)],
	dyck3(s(S),T,R).
dyck3(s(S),T,[b|R]) -->
	[([b|R],s(S),T)],
	dyck3(S,s(T),R).
dyck3(S,s(T),[c|R]) -->
	[([c|R],S,s(T))],
	dyck3(S,T,R).

% The variant d/6 below splits up D^3 words
% in a well-nested a,b word and a well-nested b,c word,
% as explained in section 6, equation (24) of the paper.

% d(Counter1,Counter2,ABs,BCs,Word,Rest).
% ABs: balanced a,b string
% BCs: balanced b,c string
% Counters: cf dyck3/4 above

d(0,0,[],[]) --> [].

d(S,T,[a|Ls],[R|Rs]) --> [a],
	d(s(S),T,Ls,[R|Rs]).
d(s(S),T,[b|Ls],[b|Rs]) --> [b],
	d(S,s(T),Ls,Rs).
d(S,s(T),Ls,[c|Rs]) --> [c], % Ls can be empty
	d(S,T,Ls,Rs).

% testing
% generate all words of length 3*N:

d3(N) :- 
	M is N*3,
	length(Word,M),
	dyck3(0,0,Word,[]),
	write(Word),
	nl,
	fail.

% with derivational history:
	
d3vdash(N) :-
	M is N*3,
	length(Word,M),
	dyck3(0,0,Word,Run,[]),
	write(Run),
	nl,
	fail.

% splitting a d3 word in superposition of two d2 words:

dd3(N) :- 
	M is N*3,
	length(Word,M),
	d(0,0,L,R,Word,[]),
	write((Word,L,R)),
	nl,
	fail.

% tex output from dyck3/5

dtex3(Word) :-
	dyck3(0,0,Word,Run,[]),
	format("\\[\\begin{tikzpicture}[every node/.style={anchor=base},xscale=.25,yscale=.4]\n",[]),
	nodes(0,Word),
	tex(0,[],[],Run),
	format("\\end{tikzpicture}\\]\n",[]).


dw3(N) :-
	tell('abcdyck.tex'),
	writeln('\\documentclass[]{article}'),
	writeln('\\usepackage[pdftex,active,tightpage]{preview}'),
	writeln('\\usepackage{tikz}'),
	writeln('\\usetikzlibrary{calc}'),
	writeln('\\pagestyle{empty}'),
	writeln('\\begin{document}'),nl,
	writeln('\\PreviewEnvironment{tikzpicture}'),
	writeln('\\setlength{\\PreviewBorder}{.5in}'),nl,
	M is N*3,
	length(Word,M),
	dtex3(Word),
	fail.
dw3(_) :-
	format("\\end{document}\n",[]),
	told.

nodes(_,[]).
nodes(N,[H|T]) :-
	format("\\node (n~d) at (~d,0) {$~w$};\n",[N,N,H]),
	succ(N,N1),
	nodes(N1,T).

tex(_,[],[],[_]).
tex(N,As,Bs,[([a|R],P,Q),(R,s(P),Q)|T]) :- % read a
	succ(N,N1),
	tex(N1,[a/N|As],Bs,[(R,s(P),Q)|T]).
tex(N,[a/M|As],Bs,[([b|R],s(P),Q),(R,P,s(Q))|T]) :- % read b
	succ(N,N1),
	format("\\draw (n~d) edge [bend left=90] (n~d);\n",[M,N]),
	tex(N1,As,[b/N|Bs],[(R,P,s(Q))|T]).
tex(N,As,[b/M|Bs],[([c|R],P,s(Q)),(R,P,Q)|T]) :- % read c
	succ(N,N1),
	format("\\draw (n~d) edge [bend right=90] (n~d);\n",[M,N]),
%	format("\\draw (n~d) edge [bend left=90] (n~d);\n",[M,N]),
	tex(N1,As,Bs,[(R,P,Q)|T]).
