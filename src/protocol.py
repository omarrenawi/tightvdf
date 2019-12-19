from prover import *
from verifier import *
from utils import *
import gensafeprime

ACCEPT=1
REJECT=-1
ERROR=-2


class Protocol():

    def __init__(self,T,x,N,s):
        self.T=T
        self.x=x
        self.s=s #statistical security parameter
        self.gen_N()


    def gen_N(self,b=4096):
        p=gensafeprime.generate(b//2)
        q=gensafeprime.generate(b//2)
        self.N=p*q


    def run(self): 
        self.prover=Prover(self.N,self.T,self.x)
        self.y=self.prover.solve()
        self.verifier=Verifier(self.N,self.x,self.T,self.y,self.s)
        
        return self.halving_protocol()

   
    def halving_protocol(self):
        
        """
        with big value of T it could be 
        problematici(for the memory) to use a
        recursion, therefore I'll use a normal loop
        """
      
        while not self.T == 1:
            m = self.prover.get_m()
           
            verifier.set_m(m)

            r = verifier.gen_rand()

            prover.set_rand(r)

            out_v= self.verifier.halve()

            out_p= self.prover.halve()

            if not out_p == out_b:
                return ERROR

        self.N, self.x, self.T, self.y = out_v

        return verifier.check()
        
