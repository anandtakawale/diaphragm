# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 16:44:38 2013

@author: rndengg2
"""
class Material():
    """
    Material class with follwoing properties
    
    Syt: Yield strength/tensile strength
    mu: Poissons ratio
    Sut: Ultimate tensile strength
    E: Youngs modulus
    G: Modulus of rigidity
    """
    def __init__(self, Syt, Sut, mu, E):
        self.Syt = Syt
        self.Sut = Sut
        self.mu = mu
        self.E = E
        self.G = E / (2.0 * (1 + mu))


class Diaphragm():
    """
    Diaphragm class specifying its dimensions
    """
    def __init__(self, D, h, material, name, b = 0):
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
        self.Syt = material.Syt
        self.Sut = material.Sut
        self.E = material.E
        self.mu = material.mu
        self.G = material.G
        self.name = name
        self.b = b/2.0 * 1e-3
    
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
        self.b = other.b
    
    def __str__(self):
        return self.name
        
class DiaphragmCorrugated(Diaphragm):
    """
    Corrugated diaphragm class inherited from Diaphragm class
    """
    def __init__(self, FlatDiaph, H, s, l):
        """
        Constructor for corrugated diaphragm object
        
        FlatDiaph: Corresponding flap diaphragm with its properties as that of
                    corrugated diaphragm
        H: Dept of corrugation [mm]
        s: Developed length [mm]
        l: wavelength of corrugations [mm]
        """
        self.assignProp(FlatDiaph)
        self.H = H * 1e-3
        self.s = s * 1e-3
        self.l = l * 1e-3
    

#setting material SS304
SS304 = Material(Syt = 1150 * 1e6, Sut = 475738 * 1e6, mu = 0.29, E = 193 * 1e9)
#cosidering 5mm outer dia for clamping
diaphNB40_50 = Diaphragm(203.2 - 12, 0.25, SS304, "NB 40 and 50")
diaphNB15_20 = Diaphragm(133.5 - 12, 0.1524, SS304, "NB 15 and 20")
diaphNB25 = Diaphragm(155.6 - 12, 0.1524, SS304, "NB 25")

#two diaphragms assuming double thickness
diaphNB40_50_double = Diaphragm(203.2 - 12, 0.50, SS304, "NB 40 and 50")

#diaphragms with rigid centres
diaphNB40_50_rigid = Diaphragm(203.2 - 12, 0.25, SS304, "NB 40 and 50 with rigid center", 90)
diaphNB25_rigid = Diaphragm(155.6 - 12, 0.1524, SS304, "NB 15 and 20 with rigid center", 80)
diaphNB15_20_rigid = Diaphragm(133.5 - 12, 0.1524, SS304, "NB 25 with rigid center", 60)

#corrugated diaphragms
diaphNB40_50_corrug = DiaphragmCorrugated(diaphNB40_50, H = 1.2, s= 1, l = 1 )
diaphNB15_20_corrug = DiaphragmCorrugated(diaphNB15_20, H = 1.2, s = 1, l = 1)
diaphNB25_corrug = DiaphragmCorrugated(diaphNB25, H = 1, s = 1.2, l = 1)

BPTdiaph = Diaphragm(32.6, 0.1, SS304, "BPT diaphragm")
BPTCorrug = DiaphragmCorrugated(BPTdiaph, H = 0.25, s = 4.3, l = 4.28)
BPT_rigid = Diaphragm(32.6, 0.1, SS304, "BPT diaphragm with rigid center", b = 7.14)
BPTCorrug_rigid = DiaphragmCorrugated(BPT_rigid, H = 0.25, s = 4.3, l =4.28)

premade_corrug = DiaphragmCorrugated(diaphNB40_50,H = 2.25,s = 18.76 ,l = 18)

