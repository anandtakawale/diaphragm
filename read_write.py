# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:21:19 2013

@author: anand
"""
import numpy as np
import matplotlib.pyplot as plt
import readout
import data_diaphragm
import writeout
import rigid_membrane
import membrane
import corrugated
import convex_diaphragm

def graph(x, y, xlabel = "", ylabel = "", legend = "", color = ""):
    """
    Plots graph of x vs y with given parameters
    """
    plt.plot(x, y, color, label = legend)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc = 'best')
    
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
    graph(P * 1e-5, y, "Pressure[bar]", "Deflection[mm]", label, '-o')

if __name__ == "__main__":
    plt.close('all')
    #writeout.main(P_kgcm2, y)
    P_max = 2e5
    P = np.arange(0, P_max + P_max/1000.0, P_max/1000.0)
    plt.figure("Single diaphragm")
#    rigid_membrane.plotPvsy(P, data_diaphragm.diaphNB40_50_rigid, "Theoretical rigid")
    membrane.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50, "Theoretical")
#    graphit("../expt/Pvsy/Expt_27sept_single_flat.xls", 0, 0, 4, "27th sept Properly fitted without LD pad")
#    graphit("../expt/Pvsy/Expt_27sept_single_flat.xls", 1, 0, 4, "27th sept improperly fitted without LD pad")
#    graphit("../expt/Pvsy/Expt_26sept_single_flat.xls", 0, 0, 4, "26th sept- deformed diaphragm without LD pad")
    graphit("../expt/Pvsy/Expt_28sept_single_flat.xls", 0, 0, 4, "28th sept- fresh single diaphragm with LD pad")
#    graphit("../expt/Pvsy/Expt_30sept_single_flat_oldused.xls", 0, 0, 4, "30th sept- old diaphragm with LD pad")
    graphit("../expt/Pvsy/Expt_30sept_single_flat_2kgcm2.xls", 0, 0, 4, "30th sept- new single diaphragm with LD pad")
#    graphit("../expt/Pvsy/Expt_1Oct_single_flat_oldused.xls", 0, 0, 4, "1st oct - old diaphragm with LD pad")
#    plt.figure("Double diaphragm")
    membrane.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_double, "Theoretical considering double thickness")
    graphit("../expt/Pvsy/Expt_1Oct_double_flat.xls", 0, 0, 4, "1st oct - double fresh w/o LD pad")
#    graphit("../expt/Pvsy/Expt_1Oct_double_flat.xls", 1, 0, 4, "2nd oct - old used w/o LD pad")
#    graphit("../expt/Pvsy/Expt_09Oct_double_flat_withLD.xls", 0, 0, 4, "9th oct- double fresh with LD pad", "bar")
#    graphit("../expt/Pvsy/Expt_09Oct_double_flat_withLD.xls", 1, 0, 4, "9th oct- old used with LD pad", "bar")
    graphit("../expt/Pvsy/Expt_10Oct_double_flat_withLD.xls", 0, 0, 4, "10th oct- double fresh with LD pad", "bar")
#    graphit("../expt/Pvsy/Expt_10Oct_double_flat_withLD.xls", 1, 0, 4, "10th oct- old used with LD pad", "bar")
    plt.figure()
    graphit("../../EXPT/readings/21Oct_single_DP50_LDadjust.xls", 0, 0, 4, "Single flat diaphragm", "bar")
    graphit("../../EXPT/readings/21Oct_single_DP50_LDadjust.xls", 0, 0, 5, "Single flat diaphragm reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    plt.figure()
    graphit("../../EXPT/readings/23Oct_double_DP50_LDadjust.xls", 0, 0, 4, "Double diaphragm", "bar")
    graphit("../../EXPT/readings/23Oct_double_DP50_LDadjust.xls", 0, 0, 5, "Double diaphragm reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex_double, data_diaphragm.diaphNB40_50_convex_double.name)    
    plt.figure()
    graphit("../../EXPT/readings/30Oct_single_corrugated_DP50.xls", 0, 0, 4, "Single corrugated diaphragm", "bar")
    graphit("../../EXPT/readings/30Oct_single_corrugated_DP50.xls", 0, 0, 5, "Single corrugated diaphragm reverse", "bar")
    plt.figure()
    graphit("../../EXPT/readings/23Oct_double_DP50_LDadjust.xls", 0, 0, 4, "Double flat diaphragm", "bar")
    graphit("../../EXPT/readings/23Oct_double_DP50_LDadjust.xls", 0, 0, 5, "Double flat diaphragm reverse", "bar")
    plt.figure()
    graphit("../../EXPT/readings/12Nov_double_corrugated_DP50.xls", 0, 0, 4, "Double corrugated diaphragm", "bar")
    graphit("../../EXPT/readings/12Nov_double_corrugated_DP50.xls", 0, 0, 5, "Double corrugated diaphragm reverse", "bar")
    
    plt.figure()
    graphit("../../EXPT/readings/28Oct_single_corrugated_LDchamber.xls", 0, 0, 4, "Single premade corrugated", "bar")
    corrugated.plotPvsyTensileBending(P, data_diaphragm.premade_corrug, "Theoretical")
    plt.figure()
    membrane.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50, "Theoretical")
    graphit("../../EXPT/readings/11Nov_single_inspacer_withoutLD.xls", 1, 0, 4, "Experimental")
    plt.figure("Single Flat in DP23 50NB, with spring extended stroke(about 6mm) [28Nov13]")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[28Nov13].xls", 0, 0, 4, "Single Flat trial 1", "bar")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[28Nov13].xls", 1, 0, 4, "Single Flat trial 2", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    plt.figure("Double Flat in DP23 50NB, with spring extended stroke(about 6mm) [29Nov2013]")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/double_flat[29Nov13].xls", 0, 0, 4, "Double Flat trail 1", "bar")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/double_flat[29Nov13].xls", 1, 0, 4, "Double Flat trail 2", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex_double, data_diaphragm.diaphNB40_50_convex_double.name)
    plt.figure("Double Flat in DP23 50NB, with spring extended stroke(about 6mm) [04Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/double_flat[04Dec13].xls", 0, 0, 4, "Double Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/double_flat[04Dec13].xls", 0, 0, 5, "Double Flat reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex_double, data_diaphragm.diaphNB40_50_convex_double.name)
    plt.figure("Single Flat in DP23 50NB, with spring extended stroke(about 6mm) trial 1 [04Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[04Dec13].xls", 0, 0, 4, "Single Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[04Dec13].xls", 0, 0, 5, "Single Flat reverse", "bar")    
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    plt.figure("Single Flat in DP23 50NB, with spring extended stroke(about 6mm) trial 2 [04Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[04Dec13].xls", 1, 0, 4, "Single Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/6mm_stroke/single_flat[04Dec13].xls", 1, 0, 5, "Single Flat reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    plt.figure("Double Flat in DP23 50NB, with spring extended stroke(about 8mm) trial 1 [16Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/double_flat[16Dec13].xls", 0, 0, 4, "Double Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/double_flat[16Dec13].xls", 0, 0, 5, "Double Flat reverse", "bar")    
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex_double, data_diaphragm.diaphNB40_50_convex_double.name)
    plt.figure("Single Flat in DP23 50NB, with spring extended stroke(about 8mm) trial 1 [17Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/single_flat[17Dec13].xls", 0, 0, 4, "Single Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/single_flat[17Dec13].xls", 0, 0, 5, "Single Flat reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    plt.figure("Single Flat in DP23 50NB, with spring extended stroke(about 8mm) trial 2 [17Dec2013]")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/single_flat[17Dec13].xls", 1, 0, 4, "Single Flat forward", "bar")
    graphit("../../EXPT/readings_extended_stroke/8mm_stroke/single_flat[17Dec13].xls", 1, 0, 5, "Single Flat reverse", "bar")
    convex_diaphragm.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_convex, data_diaphragm.diaphNB40_50_convex.name)
    #non-convex diaphragm double
    plt.figure()
    graphit("../../EXPT/readings/Double_flat_DP23_non_convex[08Jan14].xls", 0, 0, 4, "Double Flat forward non convex", "bar")
    graphit("../../EXPT/readings/Double_flat_DP23_non_convex[08Jan14].xls", 1, 0, 5, "Double Flat reverse non convex", "bar")
    membrane.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50_double, "Theoretical")
    #non-convex diaphragm single
    plt.figure()
    graphit("../../EXPT/readings/Single_flat_DP23_non_convex[09Jan14].xls", 0, 0, 4, "Single Flat forward non convex", "bar")
    graphit("../../EXPT/readings/Single_flat_DP23_non_convex[09Jan14].xls", 1, 0, 5, "Single Flat reverse non convex", "bar")
    membrane.plotPvsyTensileBending(P, data_diaphragm.diaphNB40_50, "Theoretical")
    plt.show()