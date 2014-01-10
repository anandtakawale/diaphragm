# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 17:18:39 2013

@author: anand
"""
from membrane import *
from writeout import *
import xlwt
from matplotlib.backends.backend_pdf import PdfPages


def excelwrite(P):
    """
    Writes into excel file
    """
    book = xlwt.Workbook()
    deflect_m = detDeflectTensile(P, diaphNB40_50)
    deflect_mm = [y * 10.0**3 for y in deflect_m]
    radialStress_NB4050 = [sigmaRmax(y, diaphNB40_50) for y in deflect_m]
    sh4050 = book.add_sheet("NB40_50", cell_overwrite_ok=True)
    writeout(book, P, "Pressure(Pa)", 0, sh4050)
    writeout(book, deflect_mm, "Deflection(mm)", 1, sh4050)
    writeout(book, radialStress_NB4050, "Max radial stress(Pa)", 2, sh4050)
    #writing for NB15 and 20
    sh1520 = book.add_sheet("NB15_20", cell_overwrite_ok = True)
    deflect_m = detDeflectTensile(P, diaphNB15_20)
    deflect_mm = [y * 10.0**3 for y in deflect_m]
    radialStress_NB1520 = [sigmaRmax(y, diaphNB40_50) for y in deflect_m]
    writeout(book, P, "Pressure(Pa)", 0, sh1520)
    writeout(book, deflect_mm, "Deflection(mm)", 1, sh1520)
    writeout(book, radialStress_NB1520, "Max radial stress(Pa)", 2, sh1520)
    #writing for NB25
    sh25 = book.add_sheet("NB15", cell_overwrite_ok = True)
    deflect_m = detDeflectTensile(P, diaphNB25)
    deflect_mm = [y * 10.0**3 for y in deflect_m]
    radialStress_NB1520 = [sigmaRmax(y, diaphNB40_50) for y in deflect_m]
    writeout(book, P, "Pressure(Pa)", 0, sh25)
    writeout(book, deflect_mm, "Deflection(mm)", 1, sh25)
    writeout(book, radialStress_NB1520, "Max radial stress(Pa)", 2, sh25)
    book.save("Pvsy_flat.xls")
    
if __name__ == '__main__':
    plt.close("all") # close all previous figures
    P_max = 17 * 1e5
    P = np.arange(0,P_max + P_max / 2000.0,P_max/2000.0 )
    #Consideration of only tensile stresses
#    plt.figure("Flat diaphragm:P vs. y(tensile)")
    plotPvsyTensile(P, diaphNB40_50, "Single Diaphragm 40 and 50NB")
#    plotPvsyTensile(P, diaphNB15_20, "Diaphragm 15 and 20NB")
#    plotPvsyTensile(P, diaphNB25, "Diaphragm 25NB")
#    plt.title("Pressure vs deflection considering tensile")
    #considering of tensile and bending stresses
    plt.figure("Flat diaphragm:P vs. y(tensile + bending)")
    plotPvsyTensileBending(P, diaphNB40_50, "Diaphragm 40 and 50NB")
#    plotPvsyTensileBending(P, diaphNB15_20, "Diaphragm 15 and 20NB")
#    plotPvsyTensileBending(P, diaphNB25, "Diaphragm 25NB")
#    plt.title("Pressure vs deflection considering tensile and bending")
#    #tensile and bending comparison for 40 and 50 NB diaphragm
#    plt.figure("Tensile and Tensile + bending comparison")
#    plotPvsyTensile(P, diaphNB40_50, "Diaphragm 40 and 50NB Tensile")
#    plotPvsyTensileBending(P, diaphNB40_50, "Diaphragm 40 and 50NB Tensile and Bending")
#    #plotting radial stresses for NB40,50,15,20,25
    plt.figure("Flat diaphargm Pressure vs max radial stress")
    plotPvssigmaR(P, diaphNB40_50, "Diaphragm 40 and 50 NB radial stress")
#    plotPvssigmaR(P, diaphNB15_20, "Diaphragm 15 and 20 NB radial stress")
#    plotPvssigmaR(P, diaphNB25, "Diaphragm 25NB radial stress")
#    plt.title("Pressure vs. maximum stress")
#    plt.figure()
#    plotPvsyTensileBending(P, BPTdiaph, "BPT")
    #excelwrite(P)
    plt.figure()
    plotPvsyTensileBending(P, diaphNB15_20, "Diaphragm 15 NB")
    plt.figure()
    plotPvsyTensileBending(P, diaphNB15_20_double, "Diaphragm 15NB double thickness")
    plt.show()
    
    
    
