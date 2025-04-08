# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:48:10 2025

@author: Gabriel

Esse script sera utizado para analisar os dados de qualidade do ar disponibili-
zados pela plataforma do INstitudo de Energia e Meio Ambiente.

    - Abrir corretamente o dado (ok)
    - Inserir coluna datetime  (ok)
    - Criar coluna com estação do ano (ok)
    - Filtrar dataframe (ok) (ok)
    - Extrair estatísticas básicas
    - Estatísticas por agrupamento
    - Exportar estatísticas agrupadas
    - Criar uma função para realizar as tarefas acima
    - Criar função para gerar figuras
    - Loop para qualquer arquivo dentro da pasta
    - Estatística univariada e bivariada – função exclusiva
    - Análise de dados usando o statsmodel

"""

#importação dos pacotes

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def airQualityAnalysis(uf):
    #criando variável com o nome do estado
    #uf = 'SP'
    
    # Ajustes iniciais
    dataDir= os.path.join(r'C:\Users\Gabriel\OneDrive\GitHub\ENS5132\projeto01\inputs', uf) # Definindo o caminho para a pasta de dados
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
    
    aqData = pd.concat(allFiles) #transforma a lista de df em um df único
    
    #Extraindo nomes das estações sem redundância
    stations = pd.unique(aqData['Estacao'])
    
    # 1. Primeiro convertemos a coluna 'Data' para datetime
    aqData['Data'] = pd.to_datetime(aqData['Data'], format = '%Y-%m-%d')
    
    # 2. Substituímos "24:00" por "00:00" e identificamos essas linhas
    mask = aqData['Hora'] == '24:00'
    aqData.loc[mask, 'Hora'] = '00:00'
    
    # 3. Avançamos a data em 1 dia APENAS para os casos de 24:00
    aqData.loc[mask, 'Data'] = aqData.loc[mask, 'Data'] + pd.Timedelta(days=1)
    
    # 4. Agora criamos a coluna datetime combinando corretamente
    aqData['datetime'] = pd.to_datetime(
        aqData['Data'].dt.strftime('%Y-%m-%d') + ' ' + aqData['Hora'],
        format='%Y-%m-%d %H:%M'
    )
    
    # 5. Definindo como índice
    aqData = aqData.set_index('datetime')
    
    #drop multiple columns by name
    aqData. drop (['Data', 'Hora'], axis= 1 , inplace= True )
    
    aqData['year'] = aqData.index.year    
    aqData['month'] = aqData.index.month
    aqData['day'] = aqData.index.day
    aqData['hour'] = aqData.index.hour
    
    #------------------------------Estação do Ano----------------------------------
    
    #Criando uma coluna vazia com NaN de estações
    aqData['Season']=np.nan
    
    #Verão (convencionalmente usamos dez jan fev)
    aqData['Season'][(aqData.month==1)|(aqData.month==12)|(aqData.month==2)] = 'Verão'
    
    #Outono (convencionalmente usamos mar abr mai)
    aqData['Season'][(aqData.month==3)|(aqData.month==4)|(aqData.month==5)] = 'Outono'
    
    #Inverno (convencionalmente usamos jun jul ago)
    aqData['Season'][(aqData.month==6)|(aqData.month==7)|(aqData.month==8)] = 'Inverno'
    
    #Primavera (convencionalmente usamos set out nov)
    aqData['Season'][(aqData.month==9)|(aqData.month==10)|(aqData.month==11)] = 'Primavera'
    
    #---------------------------Estatísticas Básicas-------------------------------
    
    #Extrair o nome dos polentes sem redundância
    polluants= np.unique(aqData.Poluente)
    
    # Ajustes iniciais
    dataDir2= os.path.join(r'C:\Users\Gabriel\OneDrive\GitHub\ENS5132\projeto01\outputs',uf) # Definindo o caminho para a pasta de dados
    outputDir2 = os.path.join(dataDir2, 'basicStats') # Criando subpasta para os dados processados
    
    '''
    for st in stations:
        print(st)
        statsAll = []
        for pol in polluants:
            print(pol)
            basicStat = aqData['Valor'][(aqData.Poluente==pol) & aqData.Estacao==st].describe()
            basicStat = pd.DataFrame(basicStat)
            basicStat.columns = [pol]
            statsAll.append(basicStat)
        dfmerge = pd.concat(statsAll,axis=1)
        os.makedirs(outputDir2, exist_ok=True)  # Cria a pasta se não existir
        dfmerge.to_csv(outputDir2+'/'+st+'.csv')
     '''
    
    # Estatística básica usando groupby
    statGroup = aqData.groupby(['Estacao','Poluente']).describe()
    
    # Salvando em csv
    statGroup.to_csv(outputDir2+'/'+'/basicStat_ALL.csv',encoding='latin1')

    return aqData, stations














