In dit archief de GRAIL KERNEL code, getest onder swipl 5.10.
Je zal enkele aanpassingen aan je persoonlijke situatie willen maken:

-In het install script wordt het pad voor pdflatex
gevraagd. In de computerleerzaal wellicht

PATH=$PATH:/Network/Tools/sw/teTeX/bin/powerpc-apple-darwin-current/

-In /sources/options.pl kan je een aantal instellingen veranderen.
Bijvoorbeeld: output_semantics(Flag?) staat nu op no. Kan ook yes.

Na de nodige aanpassingen draai je het install script:

./install

Dat genereert de commando's grail en testall. Klaar!

In /fragments/startfrag.pl vind je een voorbeeldfragment, met
de lexicale items van de eerste inleveropdracht. Probeer

./grail fragments/startfrag.pl "I shot the elephant in my pajamas" s



