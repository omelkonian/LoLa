% 3D Dyck words and A2 webs

/* Reference:

@ARTICLE{2008arXiv0804.3375P,
   author = {{Petersen}, T.~K. and {Pylyavskyy}, P. and {Rhoades}, B.},
    title = "{Promotion and cyclic sieving via webs}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {0804.3375},
 primaryClass = "math.CO",
 keywords = {Mathematics - Combinatorics},
     year = 2008,
    month = apr,
   adsurl = {http://adsabs.harvard.edu/abs/2008arXiv0804.3375P},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
} */

:- [d3pda].

/* To build a web for a 3D Dyck word, we start with a list of
dangling wires (the border vertices, with outgoing arcs). We
reduce the list by means of (a subset of) the growth rules
of Fig 3 in Petersen et al. */

% notation: vertex with downarrow N-1, uparrow: N-0

% initialize: border vertices are sources

f([a-1|R]) --> [a],f(R).
f([b-1|R]) --> [b],f(R).
f([c-1|R]) --> [c],f(R).
f([]) --> [].

% Main predicate h/3: h(DerivationSteps,Input,Output)
% One-step reduction g/3: g(GrowthRule,Input,Output)

h([D|R],In,Out) :- 
	g(D,In,Out0), % one-step
	!,
	h(R,Out0,Out).
h([],[],[]). 

/* Growth rules

The rules of Fig 3 introduce spurious ambiguity: 
alternative ways of building one and the same web.
For the purpose of D3, one can do with a subset. */

% reduce input

g(r1(c-0,c-1),[c-0,c-1|R],R).

g(s1(a-1,b-1,c-0),[a-1,b-1|R],[c-0|R]).
g(s2(a-1,c-1,b-0),[a-1,c-1|R],[b-0|R]).

g(t3(c-0,b-0,a-1),[c-0,b-0|R],[a-1|R]).

% structural: swap adjacent vertices

g(st3(a-1,b-0,b-0,a-1),[a-1,b-0|R],[b-0,a-1|R]).
g(ts3(c-0,b-1,b-1,c-0),[c-0,b-1|R],[b-1,c-0|R]).

% skip an input vertex before applying a growth rule

g(skip(F),[H|R],[H|S]) :- g(F,R,S).

% test (using d3pda.pl)

web(N) :- 
	M is N*3,
	length(Word,M),
	dyck3(0,0,Word,[]),
	f(Border,Word,[]),
	h(D,Border,[]),
	format("~w\t~w~n",[Word,D]),
	fail.
	
webword(Word,D) :-
	dyck3(0,0,Word,[]),
	f(Border,Word,[]),
	h(D,Border,[]),
	maplist(writeln,D).
	

/* The full set of growth rules:

g(r1(c-0,c-1),[c-0,c-1|R],R).
%g(r2(a-1,a-0),[a-1,a-0|R],R).

g(s1(a-1,b-1,c-0),[a-1,b-1|R],[c-0|R]).
g(s2(a-1,c-1,b-0),[a-1,c-1|R],[b-0|R]).
%g(s3(b-1,c-1,a-0),[b-1,c-1|R],[a-0|R]).
%g(t1(b-0,a-0,c-1),[b-0,a-0|R],[c-1|R]).
%g(t2(c-0,a-0,b-1),[c-0,a-0|R],[b-1|R]).
g(t3(c-0,b-0,a-1),[c-0,b-0|R],[a-1|R]).

%g(st1(b-1,b-0,a-0,a-1),[b-1,b-0|R],[a-0,a-1|R]).
%g(st2(b-1,a-0,a-0,b-1),[b-1,a-0|R],[a-0,b-1|R]).
g(st3(a-1,b-0,b-0,a-1),[a-1,b-0|R],[b-0,a-1|R]).
%g(ts1(b-0,b-1,c-1,c-0),[b-0,b-1|R],[c-1,c-0|R]).
%g(ts2(b-0,c-1,c-1,b-0),[b-0,c-1|R],[c-1,b-0|R]).
g(ts3(c-0,b-1,b-1,c-0),[c-0,b-1|R],[b-1,c-0|R]). */



	

