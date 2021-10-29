"""
PopulationSimBR | Codigo para Tratamento dos Dados de Entrada - 0 Area a Sintetizar
@author: rodrigo.ajauskas
"""
#ToDo: zipfile

import pandas as pd
import numpy as np
pd.show_versions()
pasta = "bruto/"
data = "PopulationSimBR/data/"
configs = 'PopulationSimBR/configs/'
arqcomp = "comp.csv"
arqmunsc = "Áreas de Ponderação por UF e Município.xls"

parte = 0
arqmun = "municipios"+str(parte)+".yaml"

""" Identificação dos municípios a sintetizar no arquivo configs/municipios.yaml """
import yaml
abrirmunicipios = yaml.load(open(configs+arqmun), Loader=yaml.FullLoader)
uf = [abrirmunicipios["estado"]]
listamunicipios = abrirmunicipios["municipios"]
tagrmsp = abrirmunicipios["tag_rmsp"]

""" --- Criacao da pasta de saida, se inexistente --- """
import os
if not os.path.exists(data):
    os.makedirs(data)
    
""" Gerar lista de correspondencia entre municípios e seus códigos de 7 dígitos do IBGE """
codmun1 = pd.read_excel(pasta+arqmunsc, sheet_name='Munic_Uma')
codmun2 = pd.read_excel(pasta+arqmunsc, sheet_name='Munic_Mais_de_uma')
codmun = codmun1.append(codmun2)

""" Filtrar apenas municípios de interesse """
municipios = pd.DataFrame(listamunicipios, columns=["Nome"])
codmunicipios = pd.merge(municipios, codmun, how='left', on='Nome')

""" Identifica se há algum município sem código alocado """
a = codmunicipios["Nome"].notnull().sum()
b = codmunicipios["Município"].notnull().sum()
if a != b: 
    print(codmunicipios)
    raise SystemExit("Rever nome dos municípios: há "+str(a-b)+" município(s) sem código do IBGE. Verificar arquivo /bruto/Áreas de Ponderação por UF e Município")

""" Elimina municipios de outros estados com mesmo nome """    
codest = pd.read_excel(pasta+arqmunsc, sheet_name='UF')
ufdf = pd.DataFrame(uf, columns=["Nome"])
coduf = pd.merge(ufdf, codest, how='left', on='Nome')
coduf = coduf.iloc[0,1]
print(codmunicipios)
codmunicipios["Mun"] = np.floor(codmunicipios["Município"]/(10**5))
codmunicipios = codmunicipios[codmunicipios["Mun"]==coduf]
print(codmunicipios)

""" Aplicar seleção no arquivo geocrosswalk """
comp = pd.read_csv(pasta+arqcomp) 
comp["Mun"] = np.floor(comp["PUMA"]/(10**6))
comp = comp[comp["Mun"].isin(codmunicipios["Município"])]
numtaz = comp["TAZ"].nunique()
numpuma = comp["PUMA"].nunique()
nummun = comp["Mun"].nunique()

numdist = "(Não se aplica)"
comp = comp[["TAZ"]+["PUMA"]]
dfpuma = pd.DataFrame(comp["PUMA"].unique(), columns=["PUMA"])
comp.insert(len(comp.columns), "REGION", np.floor(comp["PUMA"]/10**6)) # REGION = Município para o caso geral
if tagrmsp == 1:
    comp["REGION"] = np.where(comp["REGION"] == 3550308, np.floor(comp["TAZ"]/10**6), comp["REGION"]) # REGION = Distrito se código do município for = 3550308 (Mun. de São Paulo)
    numdist = comp["REGION"].nunique()
comp = comp.apply(pd.to_numeric, errors='coerce', downcast='integer')
print(dfpuma)
print(comp)
print(comp.columns)
print(" ")
print(">>> Tag RMSP = "+str(tagrmsp))
print(">>> "+str(nummun)+" Municípios"+" | "+str(numdist)+" Distritos"+" | "+str(numpuma)+" PUMA"+" | "+str(numtaz)+" TAZ")

""" Criação do novo geocrosswalk a ser utilizado para filtrar os totais de controle e a matriz semente """
comp.to_csv(data+'/geo_cross_walk.csv', index=False)
