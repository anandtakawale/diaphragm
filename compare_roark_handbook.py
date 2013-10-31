# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 15:32:23 2013

@author: Admin
"""

from data_diaphragm import *
import roark_membrane
import membrane

if __name__ == "__main__":
    P_max = 6e5
    P = np.arange(0, P_max, P_max/1000.0)
    diaphUsed = diaphNB40_50
    membrane.plotPvssigmaR(P, diaphNB40_50, "Diaphragm 40 and 50 NB radial stress")
    roark_membrane.plotPvsSigmaRmax(P, diaphUsed)