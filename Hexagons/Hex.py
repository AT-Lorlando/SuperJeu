class Hex:
    def __init__(self, q=0,r=0, s=None) :
        self.q=q
        self.r=r
        self.s= (s if s!=None else int(-q-r))
        assert self.s+self.q+self.r==0 , "La somme des trois coordonnées doit valoir 0 !"

a=Hex(1,2)
print(f"{a.q} {a.r} {a.s}")