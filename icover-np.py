#!/usr/bin/env python

def binary_gadget_a(n):
    return "".join(['11']+['0*' for i in xrange(2*n)])

def binary_gadget_b(n,i):
    return "".join(
        ["11"] +
        ['0*' for j in xrange(2*n-2)] +
        ["****"] +
        ['0*' for j in xrange(2*i-2)] +
        ['00'] +
        ['0*' for j in xrange(2*n-2*i)]
    )+"**"+"".join(['0*' for i in xrange(2*n)])

def binary_gadget_c(n,c):
    mu = ["0*" for i in xrange(2*n)]
    for i in xrange(1,n+1):
        if i in c:
            mu[2*n-2*i+1] = '**'
        if -i in c:
            mu[2*n-2*i] = '**'
    return "11" + "".join(mu) + "01" + "**"*(2*n+2)

def binary_instance(n,cl):
    return (
        [binary_gadget_a(n)] +
        list(binary_gadget_b(n,i) for i in xrange(1,n+1)) +
        list(binary_gadget_c(n,c) for c in cl)
    )

def binary_solution(v):
    def bin_val(x):
        assert x in [0,1]
        if x==1:
            return "0100"
        else:
            return "0001"
    return "".join(["11"]+[bin_val(x) for x in v])


def occ(t, w):
    for x in w:
        assert x in ["0","1"]
    for x in t:
        assert x in ["0","1","*"]
    def match(w1,w2):
        if len(w1)!=len(w2):
            return False
        for i in xrange(len(w1)):
            if w1[i]!=w2[i] and w1[i]!='*' and w2[i]!='*':
                return False
        return True
    n = len(t)
    m = len(w)
    res = []
    for i in xrange(n-m+1):
        if match(t[i:i+m], w):
            res.append(i)
    return res

def main():
    ins = binary_instance(
            3,
            [
                (1,2,-3),
                (-1,-2,3)
            ]
          )
    sol = binary_solution([1,0,1])
    ins_str = "".join(ins)
    o = occ(ins_str, sol)
    print "Instance(list):", ins
    print "Instance(str):", ins_str, "length", len(ins_str)
    print "Solution:", sol, "length", len(sol)
    print "Occurrences:", o, "max delta:", max([o[i+1]-o[i] for i in xrange(len(o)-1)])
    print "Occurrences diffs:", [o[i+1]-o[i] for i in xrange(len(o)-1)]

if __name__ == "__main__":
    main()