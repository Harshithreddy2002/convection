from file import *
re=[4,40,4000,40000,400000]
c=[0.989,0.911,0.683,0.193,0.027]
m=[0.33,0.385,0.466,0.618,0.805]
def reynoldsnum(P,U,l,M):
    return((P*U*l)/M)
def Grashofnum(b,tempdiff,length,V):
    return((9.81*b*tempdiff*(length**3))/(V*V))
class nusseltnum:
    def flatforcedlaminar(self,reynolds,Pr):
        return(0.664*(reynolds**0.5)*(Pr**0.333))
    def flatforcedturbulent(self,reynolds,Pr):
        return(2*0.0296*(reynolds**0.8)*(Pr**0.333))
    def flatfree(self,Gr,Pr):
        if(Gr*Pr<=(10**4)):
            return(1.1*((Gr*Pr)**0.143))
        elif(Gr*Pr<=(10**9)):
            return(0.59*((Gr*Pr)**0.25))
        else:
            return(0.13*((Gr*Pr)**0.333))
    def cyextforce(self,Re,Pr):
        for i in range(re):
            if(Re<=re[i]):
                return(c[i]*(Re**m[i])*(Pr**0.333))
    def cyextfree(self,Gr,Pr):
        if(Gr*Pr<=(10**8)):
            return(0.59*((Gr*Pr)**0.25))
        elif(Gr*Pr<=(10**12)):
            return(0.13*((Gr*Pr)**0.333))
    def cyintforcelaminar(self,reynolds,Pr,r):
        return(3.66+(0.068*reynolds*Pr)/(1+0.04*((reynolds*Pr*r)**0.67)))
    def cyintforceturbulent(self,Re,Pr):
        return(0.023*(Re**0.8)*(Pr**0.333))
    def spheforce(self,Re):
        return(0.37*(Re**0.6))
    def sphefree(self,Gr,Pr):
        return(2+0.43*((Gr*Pr)**0.25))
class Flatplate:
    def __init__(self,convection,x,y,z,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.length=x
        self.breadth=y
        self.thickness=z
        self.U=U
        self.temp=T
        self.reynolds=0
        self.nusselt=0
        self.Pr=Pr
        self.K=K
        self.gr=0
        self.td=t
        self.P=P
        self.M=M*(10**(-5))
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.length,self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.length,self.P/self.M)
    def dim2(self):
        if(self.convection=="forced" and self.reynolds<=5*(10**5)):
            self.nusselt=nusseltnum.flatlaminar(self,self.reynolds,self.Pr)
        elif(self.convection=="forced" and self.reynolds>5*(10**5)):
            self.nusselt=nusseltnum.flatturbulent(self,self.reynolds,self.Pr)
        elif(self.convection=="free"):
            self.nusselt=nusseltnum.flatfree(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round((self.nusselt*self.K)/self.length,2)
    def htrate(self):
        self.rate=round((self.htcoef*self.length*self.breadth*self.td),2)
    def ret(self):
        return([str(round(max(self.reynolds,self.gr),2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate)])
class Cylindrical:
    def __init__(self,convection,flow,x,D,d,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.length=x
        self.diameter=D
        self.indiameter=d
        self.reynolds=0
        self.gr=0
        self.U=U
        self.temp=T
        self.P=P
        self.M=M
        self.K=K
        self.Pr=Pr
        self.nusselt=0
        self.td=t
        self.flow=flow
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.diameter,self.P/self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.length,self.P/self.M)
    def dim2(self):
        if(self.flow=="external" and self.convection=="forced"):
            self.nusselt=nusseltnum.cyextforce(self,self.reynolds,self.Pr)
        elif(self.flow=="external" and self.convection=="free"):
            self.nusselt=nusseltnum.cyextfree(self,self.reynolds,self.Pr)
        elif(self.flow=="internal" and self.convection=="forced" and self.reynolds<=5*(10**5)):
            self.nusselt=nusseltnum.cyintforcelaminar(self,self.gr,self.Pr,(self.diameter/self.indiameter))
        elif(self.flow=="internal" and self.convection=="forced" and self.reynolds>5*(10**5)):
            self.nusselt=nusseltnum.cyintforceturbulent(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round((self.nusselt*self.K)/self.length,2)
    def htrate(self):
        self.rate=round((self.htcoef*self.length*self.breadth*self.td),2)
    def ret(self):
        return([str(round(max(self.reynolds,self.gr),2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate)])
class Sphere:
    def __init__(self,convection,d,U,T,P,M,K,Pr,t):
        self.convection=convection
        self.diameter=d
        self.U=U
        self.temp=T
        self.P=P
        self.M=M
        self.K=K
        self.Pr=Pr
        self.reynolds=0
        self.nusselt=0
        self.td=t
        self.gr=0
        self.htcoef=0
        self.rate=0
    def dim1(self):
        if(self.convection=="forced"):
            self.reynolds=reynoldsnum(self.P,self.U,self.diameter,self.P/self.M)
        else:
            self.gr=Grashofnum((1/self.temp),self.td,self.length,self.P/self.M)
    def dim2(self):
        if(self.convection=="forced"):
            self.nusselt=nusseltnum.spheforce(self,self.reynolds)
        elif(self.convection=="free"):
            self.nusselt=nusseltnum.flatfree(self,self.gr,self.Pr)
    def htcoeff(self):
        self.htcoef=round((self.nusselt*self.K)/self.length,2)
    def htrate(self):
        self.rate=round((self.htcoef*self.length*self.breadth*self.td),2)
    def ret(self):
        return([str(round(max(self.reynolds,self.gr),2)),str(round(self.nusselt,2)),str(self.htcoef),str(self.rate)])
def display(convection,velocity,typeht,shape,length,breadth,thickness,surftemp,surrtemp):
    a=values((int(surftemp)+int(surrtemp))//2)
    if(shape=="flatplate"):
        f=Flatplate(convection,float(length),float(breadth),float(thickness),float(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        f.dim1()
        f.dim2()
        f.htcoeff()
        f.htrate()
        return(f.ret())
    elif(shape=="cylinder"):
        c=Cylindrical(convection,typeht,int(length),int(breadth),int(thickness),int(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        c.dim1()
        f.dim2()
        f.htcoeff()
        f.htrate()
        return(c.ret())
    elif(shape=="sphere"):
        s=Sphere(convection,int(breadth),int(velocity),a[0],a[1],a[2],a[3],a[4],int(surftemp)-int(surrtemp))
        s.dim1()
        f.dim2()
        f.htcoeff()
        f.htrate()
        return(s.ret)