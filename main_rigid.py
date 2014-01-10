# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 15:56:56 2013

@author: anand
"""
from rigid_membrane import *
import numpy as np

if __name__ == '__main__':    
    plt.close("all") # close all previous figures
    P_max = 4 * 10**5
    P = np.arange(0,P_max,P_max/1000.0)
    #Consideration of only tensile stresses
    plt.figure("Rigid diaphragm: P vs y")
    plotPvsy(P, diaphNB40_50_rigid, "Diaphragm 40 and 50NB")
    plotPvsy(P, diaphNB15_20_rigid, "Diaphragm 15 and 20NB")
    plotPvsy(P, diaphNB25_rigid, "Diaphragm 25NB")
    plt.title("Pressure vs deflection for rigid diaphragm")
    #plotting radial stresses for NB40,50,15,20,25
    plt.figure("Rigid diaphragm: Pressure vs Deflection")
    plotPvssigmaR(P, diaphNB40_50_rigid, "Diaphragm 40 and 50 NB radial stress")
    plotPvssigmaR(P, diaphNB15_20_rigid, "Diaphragm 15 and 20 NB radial stress")
    plotPvssigmaR(P, diaphNB25_rigid, "Diaphragm 25NB radial stress")
    sigma_allow = [maxShear(diaphNB25_rigid) for x in range(len(P))]
    graph(P, sigma_allow, "Pressure(Pa)", "Radial Stress(Pa)", legend = "Maximum allowable")
    plt.title("Pressure vs. maximum stress for rigid diaphragm")
    plt.figure()
    plotPvsy(P, BPT_rigid, "BPT")
    plt.show()
#    for deflect in deflection:
#        if deflect  > 4.99:
#            print 
#            break