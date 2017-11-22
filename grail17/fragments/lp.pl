% ============================================================
% Macros: afkortingen voor formules die je vaak gebruikt
% ============================================================

% Afkorting := Formule.

tp := (s\(s\s))\s.
qtp := (s\(s\(s\(s\s))))\s.

cabc := t/(t/vabc).
vabc := (t/kbc)/a.
kbc := t/vbc.
vbc := (t/(t/c))/b.
dosen := a\(a * (a\b)).

ca := t/(t/a).
cb := t/(t/b).
bc := (b\c)\c.

out := (((b\g)\c)\h)\e.
lr := (b\c)\f.
lrechts := (b\d)\f.


qtv := (s\c)\f.
rtv := (s\r)\r.
high := a\(((b\e)\e)\(c\e)).
% ============================================================
% Lexicon: je woordenboek
% ============================================================

atp :: tp.
btp :: tp.

q1 :: (a\r)\r.
q2 :: (b\r)\r.
tv :: (a\s)/b.
tvs :: (a\s)/s.
tvss :: (a\s)/((s\r)\r).

iv :: (b\s).

low :: a\(b\(c\e)).

left :: (a\d)\f.
right :: ((a\b)\c)\d.

lft :: (a\c)\d.
rght :: ((a\b)\d)\f.
rechts :: a\b.

l00 :: (((a\d)\c)\f)\e.
r00 :: ((((a\b)\g)\d)\h)\f.

l10 :: (((a\g)\d)\f)\e.
r10 :: ((((a\b)\d)\c)\h)\f.

l01 :: (((a\d)\c)\h)\f.
r01 :: ((((a\b)\g)\d)\f)\e.

l11 :: (((a\g)\d)\h)\f.
r11 :: ((((a\b)\d)\c)\f)\e.

f :: (c/b)/a.
app :: (bbar/abar)/abbar :: M^N^K^(M@(M1^(N@(N1^(M1@K@N1))))).

x :: (t/e)/e.
y :: e.
z :: e.

dosenin :: dosen.

0 :: (a\c)\c.
1 :: ((a\b)\c)\c.

% ============================================================
% Postulaten
% ============================================================

% Structurele regels: Naam # In ---> Uit.
% Voorbeeld: Associativiteit. Als je deze activeert, kan je de
% haakjesstructuur van een zin veranderen. 

'P1' # (A * B) * C ---> A * (B * C).
'P2' # A * (B * C) ---> (A * B) * C.

'P3' # (A * B) ---> (B * A).

% ============================================================
% Testvoorbeelden: "...." ===> Formule.
% ============================================================

% "app f c" ===> bbar.

"l00 r00" ===> out.
"l10 r10" ===> out.
"l01 r01" ===> out.
"l11 r11" ===> out.





