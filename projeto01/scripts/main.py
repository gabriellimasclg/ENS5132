# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 15:32:17 2025

@author: Gabriel
"""

from airQualityAnalysis import airQualityAnalysis
from airQualityFigure import airQualityFigure
import os

repoPath = os.path.dirname(os.getcwd())
dataPath = repoPath + '/inputs'

#lista pastas dentro de dataPath
ufs = os.listdir(dataPath)

for uf in ufs:
    aqData, stations = airQualityAnalysis(uf) 
    