#!/usr/bin/env python
import random
import itertools

def random_word(n, alph):
    sigma = len(alph)
    sigma2 = 2**sigma
    w = []
    for i in xrange(n):
        if random.randint(1,10)==1:
            x = random.randint(1,sigma2-1)
        else:
            x = 2**random.randint(0,sigma-1)
        c = []
        for j in xrange(sigma):
            if x%2==1:
                c.append(alph[j])
            x = x//2
        assert(len(c)>0)
        w.append(c)
    return w

def imatch(w1,solid_p):
    if len(w1)!=len(solid_p):
        return False
    for c1,c in zip(w1,solid_p):
        if c not in c1:
            return False
    return True

def is_cover(t, c):
    n = len(t)
    m = len(c)
    if not imatch(t[0:m], c):
        return False
    if not imatch(t[-m:], c):
        return False
    occ = [i for i in xrange(n-m+1) if imatch(t[i:i+m], c)]
    assert(len(occ)>=2)
    if max([occ[i+1]-occ[i] for i in xrange(len(occ)-1)]) > len(c):
        return False
    return True


def find_covers(w, alph):
    res = set()
    sigma = len(alph)
    n = len(w)
    for ww in itertools.product(*w[0:n//2]):
        for i in xrange(1,1+n//2):
            if is_cover(w, ww[0:i]):
                res.add(ww[0:i])
    return res

def example2():
    """A partial word with several covers, at least two of the same length, with a figure."""
    random.seed(42)
    n = 12
    alph = ['a','b']
    while True:
        w = random_word(n, alph)
        if len([x for x in w if len(x)!=1]) not in [3,4,5]:
            continue
        c = find_covers(w, alph)
        if len(c)>3 and len(set([len(x) for x in c]))!=len(c):
            print "WORD", ",".join([str(x) for x in w])
            print "COVERS", sorted(["".join(x) for x in c])

def main():
    example2()

if __name__ == "__main__":
    main()