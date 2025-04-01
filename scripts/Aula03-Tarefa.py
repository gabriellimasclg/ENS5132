# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 15:37:09 2025

@author: Gabriel
"""

#%%
import numpy as np


matRand = np.random.rand(100,100)

# método de recorte
matRandSlice = matRand[0,:]

a = matRand[99,99]
print(a)