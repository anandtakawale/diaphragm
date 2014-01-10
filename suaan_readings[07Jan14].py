# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\atakawale\Documents\WinPython-64bit-2.7.5.3\settings\.spyder2\.temp.py
"""

import numpy as np
import matplotlib.pyplot as plt

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    plt.grid()
    
if __name__ == "__main__":
    plt.close('all')
    #BT6 bellows
    # force in kg
    F_bt = np.array([0, 0.54, 1.165, 2.5])
    F_bt_N = F_bt * 9.81
    #deflection in mm
    y_bt = np.array([0, 0.5, 1, 1.5])
    #mewasa corrugated bellows
    F_m = np.array([0, 0.835, 1.28, 1.72, 2.27])
    F_m_N = F_m * 9.81
    #deflection in mm
    y_m = np.array([0,2.,3.,4.,5.])
    #
    plt.figure()
    graph(F_bt, y_bt, "Force[kg]", "Deflection[mm]", "BT6 bellows- Spirax Experimental",'o-')
    graph(F_m, y_m, "Force[kg]", "Deflection[mm]", "Mewasa bellows Experimental",'o-')
    coeff_bt = np.polyfit(F_bt, y_bt, 1)
    polynomial = np.poly1d(coeff_bt)
    F_fitted = np.linspace(0, 2.5)
    y_fitted = polynomial(F_fitted)
    #graph(F_fitted, y_fitted, "Force[kg]", "Deflection[mm]", "BT6 bellows- Spirax 1st degree Curve fitted")
    coeff_bt_2 = np.polyfit(F_bt, y_bt, 2)
    polynomial = np.poly1d(coeff_bt_2)
    F_fitted = np.linspace(0, 2.5)
    y_fitted = polynomial(F_fitted)
    graph(F_fitted, y_fitted, "Force[kg]", "Deflection[mm]", "BT6 bellows- Spirax 2nd degree Curve fitted")
    coeff_m = np.polyfit(F_m, y_m, 1)
    polynomial = np.poly1d(coeff_m)
    F_fitted = np.linspace(0, 2.5)
    y_fitted = polynomial(F_fitted)
    graph(F_fitted, y_fitted, "Force[kg]", "Deflection[mm]", "Mewasa bellows- Spirax 1st degree Curve fitted")
    plt.figure()
    graph(F_bt_N, y_bt, "Force[N]", "Deflection[mm]", "BT6 bellows- Spirax Experimental")
    graph(F_m_N, y_m, "Force[N]", "Deflection[mm]", "Mewasa bellows Experimental")