
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 17:27:33 2014

@author: atakawale
"""

import numpy as np
import readout
import writeout
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#brv bellows pressure vs deflection curve
#caution the readings taken does not use very high accuracy pressure gauge and hence the reading contains errors

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color,  label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')

def funcSLinear(x, c1):
    return c1*x 
def graphit(FILENAME, sheet_no, P_col, y_col, label, P_unit = None):
    """
    Plots graph for the given diaphragm from readings in given file
    FILENAME: File to be read
    sheet_no: Sheet number to be read from
    P_col: Pressure column to be read
    y_col: Deflection column to be read
    label: Legend for the plot
    """
    P = np.array(readout.readout(FILENAME, sheet_no, P_col))
    y = np.array(readout.readout(FILENAME, sheet_no, y_col))
    if P_unit == "bar":
        #convert pressure from bar to Pa
        P = P * 1e5
    else:
        #convert pressure from Kg/cm^2 to Pa
        P = np.array(writeout.kgcm2toPa(P))
    graph(P * 1e-5, y, "Pressure[bar]", "Deflection[mm]", label, 'o')
    
if __name__ == "__main__":
    plt.close("all")
    #force vs deflection of top spring in SRV
    yspring = np.array(range(0, 11, 2))
    Fspring = np.array([0, 2.655, 5.715, 8.755, 11.8, 14.895]) * 9.81
    poptspring, pcovspring = curve_fit(funcSLinear, Fspring, yspring)
    F_spring_curvefit = np.linspace(0, max(Fspring), num = 100, endpoint = True)
    y_spring_curvefit = funcSLinear(F_spring_curvefit, poptspring[0])
    springk = 1.0/ poptspring[0]
    plt.figure("SRV top spring characteristics")
    graph(Fspring, yspring, "Force[N]", "Deflection[mm]", "Force vs deflection", '-o')
    graph(F_spring_curvefit, y_spring_curvefit, "Force[N]", "Deflection[mm]", "Fitted curve k=" + str(springk) + " N/mm")
    #Force vs deflection of bellows at Suaan
    y_f = np.array([0,2,4,6,8,10])
    F_f = np.array([0,2.13,4.45,6.945,9.765,13.1]) * 9.81 
    popt_Fvsy, pcov_Fvsy = curve_fit(funcSLinear, F_f, y_f)
    F_curveFit = np.linspace(0, max(F_f), num = 100, endpoint = True)
    y_curveFit = funcSLinear(F_curveFit, popt_Fvsy[0])
    stiffness_Fvsy = 1.0 / popt_Fvsy[0]
    plt.figure("SRV bellows Fvsy characteristics")
    graph(F_f, y_f, "Force[N]", "Deflection[mm]", "Force vs Deflection at Suaan", '-o')
    graph(F_curveFit, y_curveFit, "Force[N]", "Deflection[mm]","Fitted curve k=" + str(stiffness_Fvsy) + " N/mm")
    plt.figure()
    graphit("../../brv/bellow_Pvsdeflection_PT100.xls", 0,0, 3, "Trial1 Increasing", P_unit="bar")
    graphit("../../brv/bellow_Pvsdeflection_PT100.xls", 1,0, 3, "Trial1 Decreasing", P_unit="bar")
    graphit("../../brv/bellow_Pvsdeflection_PT100.xls", 2,0, 3, "Trial2 Increasing", P_unit="bar")
    graphit("../../brv/bellow_Pvsdeflection_PT100.xls", 3,0, 3, "Trial1 Decreasing", P_unit="bar")
    graphit("../../brv/bellow_Pvsdeflection_PT100.xls", 4,0, 3, "Trial3 Increasing", P_unit="bar")
    P = []
    y = []
    for i in range(5):
        P.extend(readout.readout("../../brv/bellow_Pvsdeflection_PT100.xls", i, 0))
        y.extend(readout.readout("../../brv/bellow_Pvsdeflection_PT100.xls", i, 3))
    P = np.array(P)
    mat = np.zeros((len(P), 2))
    mat[:,0] = P
    mat[:,1] = y
    deleteRows = []
    for i in range(len(P)):
        if mat[i,1] >= 9:
            deleteRows.append(i)
    mat = np.delete(mat, deleteRows, axis = 0)
    mat = mat[np.argsort(mat[:,0])]
    popt_Pvsy, pcov_Pvsy = curve_fit(funcSLinear, mat[:,0], mat[:,1])
    P_curveFit = np.linspace(0, mat[-1,0], num = 100, endpoint = True)
    y_curveFit = funcSLinear(P_curveFit, popt_Pvsy[0])
    stiffness_Pvsy = 1.0 / popt_Pvsy[0]
    plt.figure("SRV bellows pvsy characteristics")
    graph(mat[:,0], mat[:,1], "Pressure[bar]", "Deflection[mm]", "Pressure vs defletion bellows", 'o')
    graph(P_curveFit, y_curveFit, "Pressure[bar]", "Deflection[mm]", "Fitted curve k= " + str(stiffness_Pvsy) + " bar/mm")
    
    