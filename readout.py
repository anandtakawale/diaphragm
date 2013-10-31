# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 09:26:49 2013

@author: anand
"""
import xlrd

def readout(FILENAME, sheet_no, column):
    """
    Reads the data from xls file in the given sheet
    FILENAME: Name of the file to be read
    sheet_no: Sheet number of the file to be read
    column: the column to be read
    sheet: The sheet name to be read
    
    convention: First row of the file is not read as it contains the labels of columns
    e.g of first line
        Pressure    |    Deflection
        
        0           |   0
        
        0.1         |   1.5
    """
    book = xlrd.open_workbook(FILENAME)
    sheet = book.sheet_by_index(sheet_no)
    num_rows = sheet.nrows - 1
    curr_row = 0
    l = []
    while curr_row < num_rows:
        curr_row += 1
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        cell_value = sheet.cell_value(curr_row, column)
        l.append(cell_value)
    return l
    

# the following fucntion is not to be used in future, it to be used for first experiement only
def convertRead(readings):
    """(list) -> list
    
    Returns the readings in the dial gauge into mm
    """
    # y has deflection values[mm]
    y = []
    # interim has dial gauge readings difference in [mm]
    interim = []
    for i in range(len(readings) - 1):
        if readings[i + 1] > readings[i]:
            interim.append((readings[i+1] - readings[i]) * 0.01)
        else:
            interim.append((readings[i+1] - readings[i] + 100.0) * 0.01)
    y.append(0.0)
    for i in range(len(interim)):
        y.append(interim[i] + y[i])
    return y    
    