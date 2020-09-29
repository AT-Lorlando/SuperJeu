class Hex:
    def __init__(self, q=0,r=0, s=None) :
        self.q=q
        self.r=r
        self.s= (s if s!=None else int(-q-r))
        assert self.s+self.q+self.r==0 , "La somme des trois coordonnées doit valoir 0 !"

    def __eq__(self, other) :
        return self.q==other.q and self.r==other.r and self.s==other.s

a=Hex(1,2)
b=Hex(1,2,-3)
print(f"{a.q} {a.r} {a.s}")
print(a==b)
print(a!=b)