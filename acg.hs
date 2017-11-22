--2-MCFG for a^n b^n c^n d^n

--Mock-up of the ACG construction, using the built-in String datatype.
--Rule constants are defined by a term/program of the *target* language.
--The type synomym for the source atoms (here: S,A) realizes the map
--from source to target types.

type S = String
type A = (String -> String -> String) -> String

--c0 :: ((String -> String -> String) -> String) -> String
c0 :: A -> S
c0 = \ q -> q (\ x y -> x++y)

--c1 :: ((String -> String -> String) -> String) -> (String -> String -> String) -> String
c1 :: A -> A
c1 = \ q f -> q (\ x y -> f ("a"++x++"b") ("c"++y++"d"))

--c2 :: (String -> String -> String) -> String
c2 :: A
c2 = \ f -> f "" ""

--Example: abstract term c0 (c1 (c1 c2)) evaluates as "aabbccdd"

--TAG for a^n b^n c^n d^n

--The encoding above is in G(2,4): source atom A is blown up 
--to 4th order target type (String -> String -> String) -> String.
--The language a^n b^n c^n d^n can be handled in the lower
--complexity class G(2,3) corresponding to Tree Adjoing Grammars.

type Sa = String -> String -- order 3

k0 :: Sa -> S -- initial tree
k0 = \ f -> f ""

k1 :: Sa -> Sa -- auxiliary tree
k1 = \ g x -> "a"++g ("b"++x++"c")++"d"

k2 :: Sa -- stop adjunction
k2 = \ x -> x

--Example: abstract term k0 (k1 (k1 k2)) evaluates as "aabbccdd"
