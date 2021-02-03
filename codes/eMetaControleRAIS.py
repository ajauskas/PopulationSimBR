"""
PopulationSimBR | Codigo para Tratamento dos Dados de Entrada - 4 Meta Controle: RAIS
@author: rodrigo.ajauskas
"""

import pandas as pd
import numpy as np

pasta = "bruto/"
rais = "rais/"
arqcomp = "geo_cross_walk.csv"
arqmunsc = "Áreas de Ponderação por UF e Município.xls"
arqmun = 'municipios2.yaml'
data = "PopulationSimBR/data/"
configs = 'PopulationSimBR/configs/'
meta = "control_totals_meta"

""" Identificação dos municípios a sintetizar no arquivo configs/municipios.yaml """
import yaml
abrirmunicipios = yaml.load(open(configs+arqmun), Loader=yaml.FullLoader)
uf = [abrirmunicipios["estado"]]
listamunicipios = abrirmunicipios["municipios"]
abruf = abrirmunicipios["abreviacao_uf"]
codest = pd.read_excel(pasta+arqmunsc, sheet_name='UF')
ufdf = pd.DataFrame(uf, columns=["Nome"])
coduf = pd.merge(ufdf, codest, how='left', on='Nome')
coduf = str(coduf.iloc[0,1])
coduf2 = coduf[:2]

""" Continuação da seção de nome de pastas e arquivos """
arq = abruf+"2010.txt"

""" Redução do código de 5/6 dígitos para código de 1 dígito (classe) e contar número de pessoas """
baserais = pd.read_csv(pasta+rais+arq, sep=';', engine='python')
print(baserais.info())
baserais["ClasseCBO"] = np.where(baserais["CBO Ocupação 2002"] > 99999, np.floor(baserais["CBO Ocupação 2002"]/10**5), 0) #Necessário para separar classe 0 (zero à esquerda é desconsiderado)
print(baserais)
baserais = baserais[["Município", "CBO Ocupação 2002", "ClasseCBO"]]
baserais.to_excel("baseraissssssssssss.xlsx")

""" Aplicação da seleção para municípios de interesse """
geocw = pd.read_csv(data+arqcomp)
geocw["Mun"] = np.floor(geocw["PUMA"]/10**7)
dfmun = pd.DataFrame(geocw["Mun"].unique(), columns=["Município"])
print(dfmun)
print(len(dfmun))

# Uma contagem para cada um
# 1. puxar lista de municipios, feito
# 2. inserir na pivot tablea abaixo
    
""" Criação da tabela de incidência, pivot table  """
cbo = []
for i in range(10):
    cbo.append("CBO"+str(i))
table = pd.pivot_table(baserais, index='Município', columns='ClasseCBO', aggfunc=np.count_nonzero)
table2 = pd.merge(dfmun, table, how='left', on='Município')
cbo.insert(0,"REGION")
table2.columns = cbo
print(table2)

table.to_excel("table.xlsx")
table2.fillna(0, inplace=True)
table2 = table2.apply(pd.to_numeric, errors='coerce', downcast='integer') #XXX
table2.to_csv(data+meta+".csv", index=False)

"""
#ToDo incorporar em formato compacto:
    numbers = range(1, 10)
    sequence_of_numbers = [number for number in numbers if (number % 5 in (1, 2))]
    print(sequence_of_numbers)
baserais = pd.read_csv(r"D:\TestePython\teste.txt", sep=',', engine='python')
print(baserais)

freime = pd.DataFrame([], columns=["a"])
print(a)
"""