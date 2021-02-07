#!/usr/bin/env python
import itertools


def lcp(s1, s2):
    res = 0
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if len(set(c1).intersection(set(c2))) == 0:
            break
        res += 1
    return res


def lcp3(s1, s2, s3):
    res = 0
    for i, (c1, c2, c3) in enumerate(zip(s1, s2, s3)):
        if len(set(c1).intersection(set(c2)).intersection(set(c3))) == 0:
            break
        res += 1
    return res


def lcp_word(s1, s2):
    res = []
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        c = set(c1).intersection(set(c2))
        if len(c) == 0:
            break
        res.append(c)
    return res


def maxgap(s):
    assert len(s) >= 2
    x = list(sorted(s))
    return max([x[i+1]-x[i] for i in xrange(len(x)-1)])


def iword(w):
    if w is None:
        return "None"

    def r(x):
        if len(x) == 1:
            for xx in x:
                return xx
        else:
            return "{"+",".join(x)+"}"

    return "".join([r(x) for x in w])


def is_solid(w):
    if len(w)==0:
        return True
    return max([len(x) for x in w]) == 1


def alg_shortest_cover_fpt_sigma_k(T):
    """algorithm with time complexity O(\sigma^k/2 n)"""
    n = len(T)
    nn = n//2

    def shortest_cover(S):
        res = None
        L = set(range(0,n+1))
        dist = [min(lcp(S, T[i:]), nn) for i in xrange(n)]
        LL = {}
        for i,d in enumerate(dist):
            if not d in LL:
                LL[d] = []
            LL[d].append(i)
        for j in range(1,nn+1):
            for x in LL.get(j-1,[]):
                L.remove(x)
            if maxgap(L) <= j:
                res = S[:j]
                break
        print "shortest_cover(%s, %s) = %s" % (iword(T), iword(S), iword(res))
        return res

    non_solid_left = 0
    non_solid_right = 0
    for i in xrange(n):
        if len(T[i])>1:
            if i<nn:
                non_solid_left += 1
            else:
                non_solid_right += 1
    if non_solid_left > non_solid_right:
        return alg_shortest_cover_fpt_sigma_k(T[::-1])[::-1]

    res = None
    for S in itertools.product(*T[:nn]):
        c = shortest_cover(S)
        if c is not None:
            if res is None or len(c) < len(res):
                res = c
    print "shortest_cover(%s) = %s" % (iword(T), iword(res))
    return res


def alg_shortest_cover_from_unambiguous_borders(T):
    n = len(T)
    nn = n//2

    H = set([x for x in range(n) if not is_solid(lcp_word(T, T[x:]))])
    E = set(range(n)).difference(H)
    print "WARNING! positions are 0-indexed"
    print "T=%s" % (iword(T))
    print "hard positions H=%s" % (H)
    print "easy positions E=%s" % (E)
    EE = {0:E}
    for j in xrange(1, nn+1):
        EE[j] = [x for x in E if len(lcp_word(T, T[x:x+j])) >= j]
    print "EE=%s" % EE

    res = None
    L = [set(range(n))]
    for j in xrange(1,nn+1):
        if len(T[j-1])==1: # solid
            E_diff = set(EE.get(j-1, [])).difference(set(EE.get(j,[])))
            print "step %d, removing %s from L" % (j, E_diff)
            for LL in L:
                LL.difference_update(E_diff)
        else:
            # recompute!
            tmp = {}
            for x in EE.get(j, []):
                xx = lcp_word(T, T[x:x+j])
                print j, x, xx
                assert is_solid(xx)
                if not iword(xx) in tmp:
                    tmp[iword(xx)] = set([])
                tmp[iword(xx)].add(x)
            L = [LL.union(H) for LL in tmp.values()]
            print "step %d, recomputing L = %s" % (j, L)

        b_j = lcp_word(T[:j], T[-j:])[:j]
        if len(b_j) == j and is_solid(b_j):
            print "unambiguous border %d: %s" % (j, iword(b_j))
            assert len([LL for LL in L if n-j in LL]) == 1
            for LL in L:
                if n-j in LL:
                    L1 = LL.difference(set(x for x in H if lcp3(T, T[n-j:], T[x:]) < j))
                    print "L1=%s, maxgap=%d" % (L1, maxgap(L1))
                    if maxgap(L1) < j:
                        res = b_j
                        break
            if res is not None:
                break

    print "shortest_cover(%s) = %s" % (iword(T), iword(res))
    return res


def main():
    T = (['b'], ['b'], ['a', 'b'], ['a', 'b'], ['a'], ['b'], ['b'], ['a', 'b'], ['a', 'b'], ['b'], ['a'], ['a', 'b'])
    alg_shortest_cover_fpt_sigma_k(T)
    alg_shortest_cover_from_unambiguous_borders(T)

if __name__ == "__main__":
    main()