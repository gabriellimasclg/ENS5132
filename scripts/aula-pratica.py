# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 13:45:28 2025

@author: glima
"""

#%% aqui vou colocar o código da aula passada, vai que ajuda

# -*- coding: utf-8 -*-
"""
Created on Tue May 27 15:36:28 2025

@author: Leonardo.Hoinaski
"""

# pip install netCDF4 xarray
# Ainda não funciona XARRAY
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
import geopandas as gpd

# Abrindo arquivo netCDF
data = nc.Dataset(r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto03\inputs\MERRA2_100.tavgM_2d_aer_Nx.198001.nc4")

# Analisando os dados dentro de data
print(data)

# Extraindo os dados de SO2SMASS
so2 = data['SO2SMASS'][:]
print(data['SO2SMASS'])
print(so2)

# Extraindo latitudes e longitudes
lon = data['lon'][:]
lat = data['lat'][:]

# Abrindo shape do Brasil
# Caminho para o arquivo com o shapefile dos municípios
munPath = r"C:\Users\Leonardo.Hoinaski\Documents\ENS5132\projeto02\inputs\BR_Municipios_2024\BR_Municipios_2024.shp"

# Abrindo o arquivo shapefile
geoMun = gpd.read_file(munPath)

fig, ax = plt.subplots()
ax.pcolor(lon,lat,so2[0,:,:])
geoMun.boundary.plot(ax=ax)

#%% desafio

# https://disc.gsfc.nasa.gov/information/howto?keywords=prerequisite&title=How%20to%20Generate%20Earthdata%20Prerequisite%20Files

# from netrc import netrc  # Comentado, pois não está sendo usado diretamente

from subprocess import Popen
from getpass import getpass  # Para entrada segura de senha
import platform  # Para verificar o sistema operacional
import os
import shutil

# Flag para decidir se irá configurar as credenciais Earthdata
earth_creds = True

if earth_creds:
    # URL do sistema de autenticação da NASA Earthdata
    urs = 'urs.earthdata.nasa.gov'

    # Prompts para solicitar usuário e senha da Earthdata
    prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
               'Enter NASA Earthdata Login Password: ']

    # Diretório do usuário (ex: C:\Users\SeuNome\ ou /home/seunome/)
    homeDir = os.path.expanduser("~") + os.sep

    # Cria o arquivo .netrc com credenciais
    with open(homeDir + '.netrc', 'w') as file:
        file.write('machine {} login {} password {}'.format(urs, getpass(prompt=prompts[0]), getpass(prompt=prompts[1])))
        file.close()

    # Cria arquivo vazio para cookies
    with open(homeDir + '.urs_cookies', 'w') as file:
        file.write('')
        file.close()

    # Cria o arquivo de configuração do DODS (OPeNDAP)
    with open(homeDir + '.dodsrc', 'w') as file:
        file.write('HTTP.COOKIEJAR={}.urs_cookies\n'.format(homeDir))
        file.write('HTTP.NETRC={}.netrc'.format(homeDir))
        file.close()

    print('Saved .netrc, .urs_cookies, and .dodsrc to:', homeDir)

    # Ajusta permissões no Linux/macOS para proteger o arquivo .netrc
    if platform.system() != "Windows":
        Popen('chmod og-rw ~/.netrc', shell=True)
    else:
        # No Windows, copia o arquivo .dodsrc para o diretório de trabalho
        shutil.copy2(homeDir + '.dodsrc', os.getcwd())
        print('Copied .dodsrc to:', os.getcwd())

# --- Abaixo: construção de URLs para baixar dados MERRA-2 ---

import os
import xarray as xr
import pandas as pd
from getpass import getpass
import requests

# --- Gerar lista de URLs (caso ainda não tenha) ---
y_time_series = pd.date_range(pd.to_datetime("2024"), periods=1, freq="YE")
f_time_series = pd.date_range(pd.to_datetime("2024-01-01"), periods=6, freq="MS")
year = [t.strftime("%Y") for t in y_time_series]
month = [t.strftime("%m") for t in f_time_series]

urllist = []
for y in year:
    for m in month:
        urllist.append(f"https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_MONTHLY/M2TMNXRAD.5.12.4/{y}/MERRA2_100.tavgM_2d_rad_Nx.{y+m}.nc4")

# --- Download dos arquivos ---
os.makedirs("dados_merra2", exist_ok=True)

username = input("Earthdata Username: ")
password = getpass("Earthdata Password: ")

with requests.Session() as session:
    session.auth = (username, password)
    
    for url in urllist:
        filename = url.split("/")[-1]
        path = os.path.join("dados_merra2", filename)
        
        if not os.path.exists(path):  # Evita baixar de novo
            print(f"Baixando {filename}...")
            r = session.get(url, stream=True)
            if r.status_code == 200:
                with open(path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"{filename} salvo com sucesso.")
            else:
                print(f"Erro {r.status_code} ao baixar {filename}")
        else:
            print(f"{filename} já existe, pulando.")

# --- Abrir e concatenar com xarray ---
nc_files = [os.path.join("dados_merra2", url.split("/")[-1]) for url in urllist]

# Abre todos os arquivos e concatena automaticamente pela dimensão 'time'
ds = xr.open_mfdataset(nc_files, combine='by_coords')

print(ds)  # Mostra as variáveis e dimensões
# Exibe a lista de URLs construídas
import requests
from getpass import getpass
import os

# Crie uma pasta para armazenar os arquivos (opcional)
os.makedirs("dados_merra2", exist_ok=True)
username = input("Earthdata Username: ")
password = getpass("Earthdata Password: ")

with requests.Session() as session:
    session.auth = (username, password)
    
    for url in urllist:
        filename = url.split("/")[-1]  # Extrai o nome do arquivo da URL
        print(f"Baixando {filename}...")
        response = session.get(url, stream=True)

        if response.status_code == 200:
            with open(f"dados_merra2/{filename}", "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"{filename} salvo com sucesso.")
        else:
            print(f"Erro {response.status_code} ao baixar {filename}")


pathh = r'C:\Users\glima\OneDrive\Documentos\ENS5132\scripts\dados_merra2'

import xarray as xr
import os

# Lista de arquivos baixados
folder = "dados_merra2"
nc_files = [os.path.join(pathh, f) for f in os.listdir(pathh) if f.endswith(".nc4")]

ds = xr.open_mfdataset(nc_files, combine='by_coords', engine='netcdf4')  # ou 'netcdf4'
print(ds)


with open(nc_files[0], "rb") as f:
    print(f.read(200))  # Lê os 200 primeiros bytes









