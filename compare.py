
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 17:59:35 2013

@author: rndengg2
"""
import corrugated
import rigid_corrugated
import membrane
import rigid_membrane
from data_diaphragm import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    plt.close('all')
    P_max = 4 * 10**5
    P = np.arange(0,P_max + P_max/1000.0,P_max/1000.0 )
    #considering of tensile and bending stresses
    # for NB40 and 50
    plt.figure("P vs. y(tensile + bending) for corrugated and flat diaphragm NB40 and 50")
    corrugated.plotPvsyTensileBending(P, diaphNB40_50_corrug, 
                                      "Corrugated with H = %s mm" %(diaphNB40_50_corrug.H * 1.e3))
    corrugated.plotPvsyTensileBending(P, premade_corrug, 
                                      "Corrugated with H = %s mm" %(premade_corrug.H * 1.e3))
    membrane.plotPvsyTensileBending(P, diaphNB40_50, "Flat diaphragm")
    plt.show()
    # for NB40 and 50
    plt.figure("P vs. y(tensile + bending) for corrugated and flat diaphragm NB25")
    corrugated.plotPvsyTensileBending(P, diaphNB25_corrug, 
                                      "Corrugated with H = %s mm" %(diaphNB25_corrug.H * 1.e3))
    membrane.plotPvsyTensileBending(P, diaphNB25, "Flat diaphragm")
    plt.show()
    # for NB40 and 50
    plt.figure("P vs. y(tensile + bending) for corrugated and flat diaphragm NB15 and 20")
    corrugated.plotPvsyTensileBending(P, diaphNB15_20_corrug, 
                                      "Corrugated with H = %s mm" %(diaphNB15_20_corrug.H * 1.e3))
    membrane.plotPvsyTensileBending(P, diaphNB15_20, "Flat diaphragm")
    #comparing with premade
    
    membrane.plotPvsyTensileBending(P, diaphNB40_50, "Flat diaphragm")
    
    #comparing stresses
    plt.figure("Stress")
    membrane.plotPvssigmaR(P, diaphNB40_50, "50NB radial stress")
    corrugated.plotPvssigmaR(P, premade_corrug, "Premade Corrugated radial stress")
    corrugated.plotPvssigmaT(P, premade_corrug, "Premade Corrugated tangential stress")    
    plt.show()
    