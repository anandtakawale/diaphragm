# -*- coding: utf-8 -*-
"""
Created on Fri Sep 06 11:38:25 2013

@author: anand
"""
import membrane
import rigid_membrane
import flat_plate
import flat_plate_rigid
import numpy as np
from data_diaphragm import *
import xlwt

def writeout(book, l, label, column, sheet):
    """
    Writes the data in  xls file in the given sheet
    l: list of values to be written
    column: the column to be written
    sheet: The sheet name to be written in
    """
    sheet.write(1, column, label)
    for i in range(len(l)):
        sheet.write(i + 2, column, l[i])
        
def kgcm2toPa(P):
    """(list) -> list
    
    Returns a list of pressure converted from kg/cm2 to Pa
    P: list of pressures in kg/cm2
    
    """
    return [p * 9.81 * 1e4 for p in P]

def convertTomm(l, number):
    """
    Returns a list by multiplying each element of the list by given number.
    
    """
    return [value * number for value in l]
    
def main(P_kgcm2, exptvals = None):
    #maximum pressure exerted to diaphragm
    #P_max = 3 * 10**5
    #P = np.arange(0,P_max, P_max/1000.0)
    #creating the workbook
    P = kgcm2toPa(P_kgcm2)
    book = xlwt.Workbook()
    #creating a sheet for a given diaphragm size
    diaph = [diaphNB40_50, diaphNB15_20, diaphNB25]
    rigid = [diaphNB40_50_rigid, diaphNB15_20_rigid, diaphNB25_rigid]
    sheet = []
    for i in range(3):
        sheet.append(book.add_sheet(diaph[i].name, cell_overwrite_ok = True))
        #writing title for the sheet
        sheet[i].write(0,0, "%s pressure deflection values" %diaph[i].name)
        #writing pressure values in kg/cm2
        writeout(book, P_kgcm2, "Pressure[kg/cm2]", 0, sheet[i])
        #writing pressure values to file
        writeout(book, P, "Pressure[Pa]", 1, sheet[i])
        #writing values using flat plate theory
        deflection = flat_plate.detDeflect(P, diaph[i])
        flat_plate_deflection = convertTomm(deflection, 1e3)
        writeout(book, flat_plate_deflection, "Flat plate theory[mm]", 2, sheet[i])
        #writing values using flat plate theory with rigid center
        deflection = flat_plate_rigid.detDeflect(P, rigid[i])
        flat_rigid_deflection = convertTomm(deflection, 1e3)
        writeout(book, flat_rigid_deflection, "Flat plate with rigid center[mm]", 3, sheet[i])
        #writing values using membrane theory without rigid center
        deflection = membrane.detDeflectTensile(P, diaph[i])
        membrane_deflection = convertTomm(deflection, 1e3)
        writeout(book, membrane_deflection, "Membrane theory[mm]", 4, sheet[i])
        #writing values using membrane theory with rigid center
        deflection = rigid_membrane.detDeflectTensile(P, rigid[i])
        membrane_rigid_deflection = convertTomm(deflection, 1e3)
        writeout(book, membrane_rigid_deflection, "Membrane with rigid center[mm]", 5, sheet[i])
        if exptvals and diaph[i].name == "NB 40 and 50":
            #writing experimental values
            writeout(book, exptvals, "Experimental values[mm]", 6, sheet[i])
            #writing error as compared to membrane with rigid center
            error = [x - y for (x,y) in zip(membrane_rigid_deflection, exptvals)]
            writeout(book, error, "Error", 7, sheet[i])
            #writing %error with respect to membrane with rigid center
            error_percent = [x/y * 1e2 for (x,y) in zip(error, membrane_rigid_deflection)]
            writeout(book, error_percent, "% Error", 8, sheet[i])
            
    book.save("Pvsy.xls")

if __name__ == "__main__":
    P_max_kgcm2 = 4
    P_kgcm2 = np.arange(0, P_max_kgcm2, 0.1)
    main(P_kgcm2)
    