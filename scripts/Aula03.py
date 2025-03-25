# -*- coding: utf-8 -*-
"""
Spyder Editor

Este script foi criado na terceira aula da disciplina ENS 5132. Nesta aula, 
trabalharemos com:
    - array numpy
    - pandas dataframe
    - matplotlib

This is a temporary script file.
"""
#%% Importação de pacotes

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%% relembrando listas

listA = [1,2,3,'texto',20.5]
listB = [1,2,3,20.5]

print(listA)

#%% trabalhando com numpy

# criando um array numpy

arr = np.array([0.7,0.75,1.05])

arr2 = np.array(listA) #reconhece td como txt pq array tem q ser do msm tipo
                        # de variavel
                        
arr3 = np.array(listB) #aqui vai reconhecer td como float pq tem um float
                        # só vai reconhecer como array of int se tudo for int
                        
# criando uma matriz
precip = np.array([[1.07,0.44,1.50],[0.27,1.33,1.72]])

#acessando o valor da primeira linha e primeira coluna [linha,coluna]
print(precip[0,0])

#acessando tds os valores da primeira linha ":"
print(precip[0,:])

#acessando tds os valores da primeira coluna ":"
print(precip[:,0])
prepSlice=precip[:,0]
print(prepSlice)

# extraindo os dois primeiros valores da primeira linha
print(precip[0,0:1]) #inclui o 0 mas n inclui o 1
print(precip[0,0:2]) #inclui o 0 e o 1 mas n inclui o 2

#extraindo o último valor da última coluna
print(precip[-1,-1])

#------------------------------------------------------------------------------
#Criando matrizes com múltiplas dimensões

# criar um arranj de dados com início, fim e passo
#de 1 a 16 de um em um; muda-se o shape/dimensão deste
x = np.arange(1,16,1).reshape(3,5)

# transposta
print(x.transpose())

# criando matriz de números aleatórios (tempo,x,y), por ex
# o tempo é a primeira dimensão da minha matriz
matRand = np.random.rand(10,100,100)

# método de recorte
matRandSlice = matRand[0,:,:]

# matriz 4D
matRand4D = np.random.rand(3,10,100,100)

#dimensão da matriz
print(matRand4D.ndim)

#shape da matriz
print(matRand4D.shape)

#numero de elementos
print(matRand4D.size)

#multiplicação escalar
print(matRand4D*3,9)

print(np.arange(1,16,1).reshape(1,15))

dataSample = np.loadtxt(r"C:\Users\Gabriel\OneDrive\GitHub\ENS5132\data\dataSample.txt")
dataSample = np.loadtxt(r"C:\Users\Gabriel\OneDrive\GitHub\ENS5132\data\dataSample2.csv",
                        delimiter=',')

# média da matriz 4d
print(matRand4D.mean())
print(matRand4D.max(axis=0))
maxMat4D = matRand4D.max(axis=0) #encontrar a máxima

#%%

#df.describe faz toda a esttística