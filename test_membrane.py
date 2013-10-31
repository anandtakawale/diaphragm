# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 16:11:40 2013

@author: anand
"""
from membrane import *

def test_tensileBendingDeflect():
    """
    Prints values for deflection as specified in the example
    """
    #code testing for deflection using example on page 149
    a = 0.4
    h = 0.02
    E = 28.5 * 10**6
    mu = 0.272
    P = 322.587
    print tensileBendingDeflect(P, a, E ,h, mu)
    
    
if __name__ == "__main__":
    print test_tensileBendingDeflect()