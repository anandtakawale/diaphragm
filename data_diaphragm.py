
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 16:44:38 2013

@author: rndengg2
"""
import numpy as np

class Material():
    """
    Material class with follwoing properties
    
    Syt: Yield strength/tensile strength
    mu: Poissons ratio
    Sut: Ultimate tensile strength
    E: Youngs modulus
    G: Modulus of rigidity
    """
    def __init__(self, Syt, Sut, mu, E, name):
        self.Syt = Syt
        self.Sut = Sut
        self.mu = mu
        self.E = E
        self.G = E / (2.0 * (1 + mu))
        self.Se_dash = 0.5 * self.Sut
        self.name = name


class Diaphragm():
    """
    Diaphragm class specifying its dimensions
    """
    def __init__(self, D, h, material, name):
        """
        Constructor for Diaphragm object with following properties
        
        D: Diameter of diaphragm[mm]
        a: Radius of diaphragm [m]
        h: Thickness of diaphragm
        material: Material of construction
        name: Name of the diaphragm object
        b: Rigid center radius if any
        """
        self.a = D/2.0 * 1e-3
        self.h = h * 1e-3
        self.material = material
        self.Syt = self.material.Syt
        self.Sut = self.material.Sut
        self.E = self.material.E
        self.mu = self.material.mu
        self.G = self.material.G
        self.Se_dash = self.material.Se_dash
        self.name = name
    
    def assignProp(self, other):
        """
        Assigns the property of other diaphragm to current diaphragm
        """
        self.a = other.a
        self.h = other.h
        self.Syt = other.Syt
        self.Sut = other.Sut
        self.E = other.E
        self.mu = other.mu
        self.G = other.G
    
    def __str__(self):
        return self.name

class DiaphragmRigid(Diaphragm):
    """
    Defines class for rigid flat diaphragm
    """
    def __init__(self, D, h, material, name, b):
        Diaphragm.__init__(self, D, h, material, name)
        self.b = b / 2.0 * 1e-3
        self.c = self.a / float(self.b)
        self.Ap = 3*(1-self.mu**2)/ 16.0 * (1 - (self.b/self.a)**4 - 4 * (self.b/self.a)**2 * np.log(self.a/self.b))
        self.Bp = ((7.0 - self.mu)/ 3.0 * (1.0 + (self.b/self.a)**2 + (self.b/self.a)**4) +\
                   (3.0 - self.mu)**2 / (1.0 + self.mu) * (self.b/ self.a)**2) / (1.0 - self.mu) / (1.0 - (self.b/ self.a)**4) / (1.0 - (self.b/ self.a)**2)**2
        #factor used in the calculation of diaphragm loaded by a force
        self.Af = 3.0*(1.0 - self.mu**2) / np.pi * ((self.c**2 - 1.)/(4. * self.c**2) - (np.log(self.c))**2 / (self.c**2 - 1.0))

class Bellows(DiaphragmRigid):
    """
    Defines class for bellows object
    """
    def __init__(self, D, h, material, name ,b , no_of_diaph):
        DiaphragmRigid.__init__(self, D, h, material, name, b)
        self.n = no_of_diaph
        
class DiaphragmCorrugated(Diaphragm):
    """
    Corrugated diaphragm class inherited from Diaphragm class
    """
    def __init__(self, FlatDiaph, H, s, l, name):
        """
        Constructor for corrugated diaphragm object
        
        FlatDiaph: Corresponding flap diaphragm with its properties as that of
                    corrugated diaphragm
        H: Dept of corrugation [mm]
        s: Developed length [mm]
        l: wavelength of corrugations [mm]
        q: profile factor []
        Ap: dimensionless stiffness coefficient for linear term
        Bp: dimensionless stiffness coefficient for non-linear term
        Ks: Tangential stress factor []
        Kr: Radial stress factor []
        """
        self.assignProp(FlatDiaph)
        self.H = H * 1e-3
        self.s = s * 1e-3
        self.l = l * 1e-3
        self.q = (1.5 * (self.H / self.h)**2 + 1)**0.5
        self.Ap = 2*(3 + self.q)*(1 + self.q)/(3 * (1 - (self.mu/self.q)**2))
        self.Bp = 32.0 / (self.q**2 - 9) * (1.0/6  - (3 - self.mu)/((self.q - self.mu) * (self.q + 3)))
        self.Ks = (3 + np.sqrt(6 * (self.q**2  - 1)))/((self.q - 1)*(self.q + 3)) * (2.0 / (self.q - 1))**(2.0 / (self.q -3))
        self.Kr = (6.0/(self.q * (self.q -1)))**(1.0 / (self.q -3))
        self.G = 1 + 0.025 * ((self.H * self.l)/(self.h * self.a))**2
        self.name = name
    

class DiaphragmConvex(Diaphragm):
    """
    Class for specifying convex diaphragm
    """
    def __init__(self, FlatDiaph, A, name):
        """
        Constructor for convex diaphragm
        
        FlatDiaph: Corresponding flat diaphtagm with its properties as that of
                    convex diaphragm
        A: amount of initial deflection from neutral surface [mm]
        name: name of the flat diaphragm
        """
        self.assignProp(FlatDiaph)
        self.A = A * 1e-3
        self.name = name
    
#setting material SS304
SS304 = Material(Syt = 250e6, Sut = 1150e6, mu = 0.29, E = 200e9, name = "SS304")
"""
Properties of SS304 summerized as follows:
Density: 8027 kg/m^3
Specific heat: 0.5 kJ/kg.K
"""
HastelloyC276 = Material(Syt = 275e6, Sut = 696e6, mu = 0.3, E = 205e9, name = "HastealloyC276")
"""
Properties of Hastelloy C276 are summerized as follows:
Specific weight at 25C: 8.94 g/cm**3
Hardness Rockwell B: 91
"""
SS316 = Material(Syt = 225e6, Sut = 590e6, mu = 0.3, E = 193e9, name = "SS316")




#cosidering 5mm outer dia for clamping
diaphNB40_50 = Diaphragm(203.2 - 12, 0.25, SS304, "NB 40 and 50")
diaphNB15_20 = Diaphragm(133.5 - 12, 0.1524, SS304, "NB 15 and 20")
diaphNB25 = Diaphragm(155.6 - 12, 0.1524, SS304, "NB 25")
diaphPilot = Diaphragm(57 - 4, 0.1524, SS304, "Pilot diaphragm")
diaph170 = Diaphragm(170, 0.25, SS304, "170 mm diaphragm")

#derived diaphragm with lower thickness
diaphNB40_50_lowerguage = Diaphragm(203.2 - 12, 0.1524, SS304, "NB 40 and 50")
#two diaphragms assuming double thickness
diaphNB40_50_double = Diaphragm(203.2 - 12, 0.50, SS304, "NB 40 and 50 double thickness")
diaphNB15_20_double = Diaphragm(133.5 - 12, 0.3048, SS304, "NB 15 and 20 double thickness")
diaphNB25_double = Diaphragm(155.6 - 12, 0.3048, SS304, "NB 25 double thickness")

#diaphragms with rigid centres
diaphNB40_50_rigid = DiaphragmRigid(203.2 - 12, 0.25, SS304, "NB 40 and 50 with rigid center", 90)
diaphNB25_rigid = DiaphragmRigid(155.6 - 12, 0.1524, SS304, "NB 15 and 20 with rigid center", 80)
diaphNB15_20_rigid = DiaphragmRigid(133.5 - 12, 0.1524, SS304, "NB 25 with rigid center", 60)
diaphPilot = DiaphragmRigid(57 - 4.0, 0.1524, SS304, "Pilot diaphragm", 16)
BT6diaph = DiaphragmRigid(31.8 - 0.6 , 0.1, SS304, "BT6 bellows single diaphragm", 19.13)
BT6Bellow = Bellows(31.8 - 0.6, 0.1, SS304, "BT6 bellows", 19.13, 10.0)
BT6Bellow_hastealloy = Bellows(31.8 - 0.6, 0.1, HastelloyC276, "BT6 Hastealloy bellows", 19.13, 10.0)

#corrugated diaphragms
diaphNB40_50_corrug = DiaphragmCorrugated(diaphNB40_50, H = 1.2, s= 1, l = 1, name = diaphNB40_50.name + " corrugated")
diaphNB15_20_corrug = DiaphragmCorrugated(diaphNB15_20, H = 1.2, s = 1, l = 1, name = diaphNB15_20.name + " corrugated")
diaphNB25_corrug = DiaphragmCorrugated(diaphNB25, H = 1, s = 1.2, l = 1, name = diaphNB25.name + " corrugated")

BPTdiaph = Diaphragm(32.6, 0.1, SS304, "BPT diaphragm")
BPTCorrug = DiaphragmCorrugated(BPTdiaph, H = 0.25, s = 4.3, l = 4.28, name = BPTdiaph.name + " corrugated")
BPT_rigid = DiaphragmRigid(32.6, 0.1, SS304, "BPT diaphragm with rigid center", b = 7.14)
BPTCorrug_rigid = DiaphragmCorrugated(BPT_rigid, H = 0.25, s = 4.3, l =4.28, name = BPT_rigid.name + " corrugated")


premade_corrug = DiaphragmCorrugated(diaphNB40_50,H = 2.25,s = 18.76 ,l = 18, name = "Premade corrugated")
try1 = Diaphragm(180.0, 0.7112, SS304, "Design 1")
try1_corrug = DiaphragmCorrugated(try1, H  = 3.14, s = 22.23, l = 21, name = try1.name + " corrugated")

try2 = Diaphragm(120, 0.7112, SS304, "Design 2")
try2_corrug = DiaphragmCorrugated(try2, H = 3.43, s = 19.69, l = 18, name = try2.name + " corrugated")

try3 = Diaphragm(100, 0.5, SS304, "Design 3")
try3_corrug = DiaphragmCorrugated(try3, H = 4.06, s= 22.13, l = 20.0, name = try3.name + " corrugated")
#convex diaphragm
diaphNB40_50_convex = DiaphragmConvex(diaphNB40_50, 1.8, "40 an 50NB convex flat diaphragm")
diaphNB20_convex = DiaphragmConvex(diaphNB15_20, 0.5, "20NB convex single flat diaphragm")
diaphNB25_convex = DiaphragmConvex(diaphNB25, 0.7, "25NB convex flat diaphragm")
diaphNB40_convex = DiaphragmConvex(diaphNB40_50, 0.7, "40NB convex flat diaphragm")
diaphNB40_50_convex_double = DiaphragmConvex(diaphNB40_50_double, 1.8, "50NB convex flat double thickness diaphragm")
diaphNB20_double_convex = DiaphragmConvex(diaphNB15_20_double, 0.5, "20NB convex flat double thickness diaphragm")
diaphNB25_double_convex = DiaphragmConvex(diaphNB25_double, 0.7, "25NB convex flat double thickness diaphragm")
diaphragmNB40_double_convex = DiaphragmConvex(diaphNB40_50_double, 1.5, "40NB convex flat double thickness diaphragm")

minami_advice = DiaphragmRigid(30 - 0.6, 0.2, SS304, "KUZE adv", 16)
minami_bellow = Bellows(30 - 0.6, 0.2, SS304, "KUZE adv", 16, 52)

#pilot batch
K1630_diaphragm = DiaphragmRigid(30 - 0.6, 0.1, SS316, "KUZE K1630 diaphragm", 16)
K1630_bellow = Bellows(30 - 0.6, 0.1, SS316, "Kuze K1630 6 convolutions", 16, 12)

#KUSHAL
dsdp80NB = Diaphragm(283.5, 0.25, SS304, "DSDP 143 80NB")

#DP143
DP143_1520NB = Diaphragm(124.8 - 12.0, 0.1524, SS304, "DP143 15 and 20 NB")
DP143_25NB = Diaphragm(165.8 - 12.0, 0.2134, SS304, "DP143 25NB")
DP143_4050NB = Diaphragm(229.8 - 12.0, 0.254, SS304, "DP143 40 and 50NB")
DP143_80NB = Diaphragm(229.5 - 12.0, 0.254, SS304, "DP143 80NB")