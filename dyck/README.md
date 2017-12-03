To run:
```bash
> python dyck.py -h
usage: dyck.py [-h] [-n [N]] [-w [W]] [-ws [WS]] [-p [P]] [-minp [MINP]]
               [-ps [PS]] [-g [G]] [--rules] [--check] [--gen] [--reverse]
               [--half] [--time]

Check your D3 grammar.

optional arguments:
  -h, --help    show this help message and exit
  -n [N]        number of "abc" occurences
  -w [W]        single word to check
  -ws [WS]      file containing words to check
  -p [P]        single parse of a word
  -minp [MINP]  show minimal parse of a word
  -ps [PS]      multiple parses of a word
  -g [G]        grammar to use
  --rules       print all rules
  --check       check soundness
  --gen         generate dyck words
  --reverse     search in reverse
  --half        search in reverse
  --time        measure execution time
```
