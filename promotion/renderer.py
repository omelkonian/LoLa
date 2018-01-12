import taquin


#
# Dyck generation
#
def ishuffle(l,r):
    if not (l and r):
        yield l+r
    else:
        yield from ((l, r)[i][0]+w for i in range(2) if not i or r[0] < l[0] for w in ishuffle(l[(i+1) % 2:], r[i % 2:]))


def idyck(k,n):
    sigma = ''.join([chr(97+i) for i in range(k)]) # a,b,c,... (k letters)
    if n < 2:
        yield sigma*n
    else:
        yield from it.chain.from_iterable((ishuffle(sigma, w) for w in idyck(k, n-1)))


#
# conversion tableaux <-> words
#
def yamanouchi(tbl):
    """Young tableau --> Yamanouchi word"""
    word = np.arange(tbl.size)
    for i, j in np.ndindex(tbl.shape):
        word[tbl[i, j]-1] = i+1
    return word


def tableau(y):
    """Yamanouchi word --> Young tableau"""
    elist = [ j+1 for _,j in sorted(list(zip(y,range(len(y))))) ]
    tbl = np.array(elist).reshape(max(y),len(y)//max(y))
    return tbl


#
# translation to alphabetic form
#
def t2w(tbl):
    return ''.join([ chr(96+i) for i in yamanouchi(tbl) ])

def w2t(word):
    return tableau([ ord(i)-96 for i in word ])
