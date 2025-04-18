# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 13:44:43 2025

@author: Gabriel
"""

#%% Importando os pacotes que utilizarei

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

#%% Revisão numpy

#criando um vetor com arranjo de dados

x = np.arange(-10,20,0.15)


#brincando com indexação (acessando os índices da matriz)

print('Essa é a quarta posição do meu vetor:',x[3])
print('Essa é a quarta posição do meu vetor: '+ str(x[3]))
print('Esses são os três primeiros valores: '+ str(x[0:3])) #não pega o valor x[3]
                                                            # pega o 0 1 2


# Substituir um valor dentro do vetor

x[9] = 99999999 #exemplo de medição errada
x[11] = -99999999 #exemplo de medição errada

# Extraindo a média

meanX = np.mean(x)
print(meanX)

# Operação booliana
#Encontrando valores errados

vecBool = (x>20) | (x<-10) # estou usando o símbolo | para or; and = &
           
#Extraindo valores errados usando ógica booleana
valErrado = x[vecBool] #ele encontra o valor errado

x2 = x.copy() # colocar copy para o x2 se tornar INDEPENDENTE de x.
x2[vecBool] = 0
print('Esta é a média de X substituindo valores errados por 0: ',np.mean(x2))

# n é o jeito certo, pq zero vai invalidar meus resultados. O idela é 
# substituir por NaN - Not a Number (no excel é qd deixa a célula vazia)

#média usando na.nanmean; existe para quase tds os valores
x3 = x.copy()
x3[vecBool] = np.nan 
print('Esta é a média de X substituindo valores errados por nan: ',np.nanmean(x3))

#Substituir os números errados pela média, útil para alguns pacotes que não 
#reconhecem o NaN

x4 = x.copy()
x4[vecBool] = np.nanmean(x3)

#%% Usando o pacote matplotlib para inspecionar o dado

fig, ax = plt.subplots(4) #o ax é uma lista com 4 gráficos dentro do fig
ax[0].plot(x)
ax[1].plot(x2)
ax[2].plot(x3)
ax[3].plot(x4)

#%% Loop em python

# loop utilizando Range

for ii in range (0,10):
    val = 2**ii
    print(val)

# loop utilizando Range e acumulando o valor de val em um vetor

vetor = []
for ii in range (0,10):
    val = 2**ii
    print(val)
    vetor.append(val)

# loop utilizando Range e acumulando o valor de val em um vetor

vetorAcumulado = []
val = 0
for ii in range (0,10):
    val = val + 2**ii
    print(val)
    vetorAcumulado.append(val)

# loop utilizando uma lista

alunas = ['Mariana','Bianca','Ana Júlia','Mariah']

for aluna in alunas:
    print('A nota da',aluna,'é',np.random.rand(1)*10)


#%% Trabalhando com o Pandas

# Criand um DataFrame manualmente

df = pd.DataFrame(columns=['date','NH3'],
                  data=[
                      ['2025/04/01',0.35],
                      ['2025/04/02',1.01]
                      ])

# Criando mais coisas dentro do df

df['NO3'] = np.nan
df['02'] = [2,10]
df['SO4'] = np.nan
df['SO4'][0] = 1

#%% Dados Reais

#criando variável com o nome do estado
uf = 'SP'

# Ajustes iniciais
dataDir= os.path.join(r'C:\Users\Gabriel\OneDrive\GitHub\ENS5132\data', uf) # Definindo o caminho para a pasta de dados
outputDir = os.path.join(dataDir, 'dados_por_estacao') # Criando subpasta para os dados processados
os.makedirs(outputDir, exist_ok=True)  # Cria a pasta se não existir

# Listar apenas arquivos CSV (ignorando diretórios)
dataList = [f for f in os.listdir(dataDir) 
           if f.endswith('.csv') and os.path.isfile(os.path.join(dataDir, f))]

#movendo para a pasta dataDir
os.chdir(dataDir)

# colocando todos os nomes dos arquivos num df
allFiles = [] #lista vazia p inserir os df

for fileInList in dataList:
    print(fileInList) #printa o nome do csv na pasta
    dfConc = pd.read_csv(fileInList, encoding='latin1') #le o csv na pasta
    allFiles.append(dfConc) #adiciona o csv lido no all files

allFiles = pd.concat(allFiles) #transforma a lista de df em um df único

#Extraindo nomes das estações sem redundância
stations = pd.unique(allFiles['Estacao'])

#Usando lógica p pegar os dados de uma só estação, a primeira da stations
stationDf = allFiles[allFiles['Estacao']== stations[0]]

# 1. Primeiro convertemos a coluna 'Data' para datetime
stationDf['Data'] = pd.to_datetime(stationDf['Data'], format = '%Y-%m-%d')

# 2. Substituímos "24:00" por "00:00" e identificamos essas linhas
mask = stationDf['Hora'] == '24:00'
stationDf.loc[mask, 'Hora'] = '00:00'

# 3. Avançamos a data em 1 dia APENAS para os casos de 24:00
stationDf.loc[mask, 'Data'] = stationDf.loc[mask, 'Data'] + pd.Timedelta(days=1)

# 4. Agora criamos a coluna datetime combinando corretamente
stationDf['datetime'] = pd.to_datetime(
    stationDf['Data'].dt.strftime('%Y-%m-%d') + ' ' + stationDf['Hora'],
    format='%Y-%m-%d %H:%M'
)

# 5. Definindo como índice
stationDf = stationDf.set_index('datetime')

# Se precisar das colunas separadas, pode extrair depois do índice
stationDf['year'] = stationDf.index.year

#%% vou fazer a mesma coisa, mas agora a tarefa 2 que o professor pediu

#criando variável com o nome do estado
uf = 'SP'

# Ajustes iniciais
dataDir= os.path.join(r'C:\Users\Gabriel\OneDrive\GitHub\ENS5132\data', uf) # Definindo o caminho para a pasta de dados
outputDir = os.path.join(dataDir, 'dados_por_estacao') # Criando subpasta para os dados processados
os.makedirs(outputDir, exist_ok=True)  # Cria a pasta se não existir

# Listar apenas arquivos CSV (ignorando diretórios)
dataList = [f for f in os.listdir(dataDir) 
           if f.endswith('.csv') and os.path.isfile(os.path.join(dataDir, f))]

#movendo para a pasta dataDir
os.chdir(dataDir)

# colocando todos os nomes dos arquivos num df
allFiles = [] #lista vazia p inserir os df

for fileInList in dataList:
    print(fileInList) #printa o nome do csv na pasta
    dfConc = pd.read_csv(fileInList, encoding='latin1') #le o csv na pasta
    allFiles.append(dfConc) #adiciona o csv lido no all files

allFiles = pd.concat(allFiles) #transforma a lista de df em um df único

#Extraindo nomes das estações sem redundância
stations = pd.unique(allFiles['Estacao'])

for i, station in enumerate(stations):
    stationDf = allFiles[allFiles['Estacao']== station].copy()
    
    # 1. Primeiro convertemos a coluna 'Data' para datetime
    stationDf['Data'] = pd.to_datetime(stationDf['Data'], format = '%Y-%m-%d')

    # 2. Substituímos "24:00" por "00:00" e identificamos essas linhas
    mask = stationDf['Hora'] == '24:00'
    stationDf.loc[mask, 'Hora'] = '00:00'

    # 3. Avançamos a data em 1 dia APENAS para os casos de 24:00
    stationDf.loc[mask, 'Data'] = stationDf.loc[mask, 'Data'] + pd.Timedelta(days=1)

    # 4. Agora criamos a coluna datetime combinando corretamente
    stationDf['datetime'] = pd.to_datetime(
        stationDf['Data'].dt.strftime('%Y-%m-%d') + ' ' + stationDf['Hora'],
        format='%Y-%m-%d %H:%M'
    )

    # 5. Definindo como índice
    stationDf = stationDf.set_index('datetime')
    
    #drop multiple columns by name
    stationDf. drop (['Data', 'Hora'], axis= 1 , inplace= True )
    
    stationDf['year'] = stationDf.index.year    
    stationDf['month'] = stationDf.index.month
    stationDf['day'] = stationDf.index.day
    stationDf['hour'] = stationDf.index.hour
    
    # 6. Exportando para CSV
    nome_arquivo = f'dados_estacao_{station.lower().replace(" ", "").replace("-", "_")}.csv'
    caminho_completo = os.path.join(outputDir, nome_arquivo)
    
    # Usando o método to_csv do DataFrame, não do pandas diretamente
    stationDf.to_csv(caminho_completo, index=True, encoding='utf-8-sig')
    print(f"Arquivo salvo em: {caminho_completo}")
    


























