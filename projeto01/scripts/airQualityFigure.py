# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:53:27 2025

@author: Gabriel
"""

import matplotlib.pyplot as plt
import os

def airQualityList(aqData,stations, uf, repoPath):
    os.makedirs(repoPath+';figuras/'+uf+exist_ok=True)
    for st in stations:
        fig, ax = plt.subplots
        aqData[aqData.Estacao==st].hist("Valor",by'Poluente',ax=ax)