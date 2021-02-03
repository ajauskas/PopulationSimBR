"""
PopulationSimBR | Codigo para Tratamento dos Dados de Entrada - 2 Matriz Semente
@author: rodrigo.ajauskas
"""

import pandas as pd
import numpy as np
import time
import locale as lc

inicio = time.time()
lc.setlocale(lc.LC_ALL, 'pt_BR')

pasta = "bruto/"
arqdic = "Layout_microdados_Amostra.xls"
arqcomp = "geo_cross_walk.csv"
arqmunsc = "Áreas de Ponderação por UF e Município.xls"
configs = 'PopulationSimBR/configs/'

parte = 7
arqmun = "municipios"+str(parte)+".yaml"

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
tagrmsp = abrirmunicipios["tag_rmsp"]

""" Continuação da seção de nome de pastas e arquivos """
uf = abruf+"/"
arqpes = "Amostra_Pessoas_"+coduf2+".txt"
arqdom = "Amostra_Domicilios_"+coduf2+".txt"
if tagrmsp == 1:
    arqpes = "Amostra_Pessoas_"+coduf2+"_RMSP"+".txt"
    arqdom = "Amostra_Domicilios_"+coduf2+"_RMSP"+".txt"
data = "PopulationSimBR/data/"
auxi = "auxi"

codest = pd.read_excel(pasta+arqmunsc, sheet_name='UF')
geocw = pd.read_csv(data+arqcomp)
print(geocw)

""" --- Criacao da pasta de saida, se inexistente --- """
import os
if not os.path.exists(data):
    os.makedirs(data)
if not os.path.exists(auxi):
    os.makedirs(auxi)

""" --- Tratamento de dados dos arquivos de microdados de pessoas --- """

aba2 = "PESS"
dic2 = pd.read_excel(pasta+arqdic, usecols="A,J,K", skiprows=1, header=0, sheet_name=aba2)
dic2.columns = ["var", "int", "dec"]
dic2.fillna(0, inplace=True)
dic2 = dic2.astype({"dec": int})
dic2["tam"] = dic2["int"]+dic2["dec"]
if tagrmsp == 0:
    mbasepes = pd.read_fwf(pasta+uf+arqpes, header=None, widths=dic2["tam"])
if tagrmsp == 1: #caminho temporario
    mbasepes = pd.read_fwf(r"D:\Users\rodrigo.ajauskas\Documents\Rodrigo Ajauskas 2020\ACADEMICO\Arquivos BR\Microdados SP2-RM"+"/"+arqpes, header=None, widths=dic2["tam"])
par = time.time()

mbasepes.columns = dic2["var"]
mbasepes["REND"] = mbasepes["V6528"]/(10**5)
mbasepes["PWGTP"] = mbasepes["V0010"]/(10**13)
#TODO: (i) deixar automatico pelo decimal e (ii) fazer um "for" para todas as variaveis

mbasepes.rename(columns=
                {"V0011":"PUMA",
                "V0300":"hhnum2",    
                "V0504":"SPORDER",
                "V0502":"RELP",
                "V0601":"SEX",
                "V6036":"AGEP",
                "V6400":"EDUC",
                "V6461":"OCUP4dg",
                "V0648":"ENQUAD"},
                inplace=True)

mbasepes["OCUP"] = np.where(len(mbasepes["OCUP4dg"]) > 999, np.floor(mbasepes["OCUP4dg"]/1000), 0)
mbasepes["OCUP"] = np.where(mbasepes["OCUP4dg"] == 0, "a", mbasepes["OCUP"])
mbasepes["EDUC"] = np.where(mbasepes["EDUC"] == 5, 1, mbasepes["EDUC"])
mbasepes = mbasepes[["PUMA","PWGTP","hhnum2","SPORDER","RELP","SEX","AGEP", "EDUC", "OCUP", "ENQUAD", "REND"]]

""" Aplicação da seleção para municípios de interesse """
geocw = pd.read_csv(data+arqcomp)
dfpuma = pd.DataFrame(geocw["PUMA"].unique(), columns=["PUMA"])
mbasepes = pd.merge(dfpuma, mbasepes, how='left', on='PUMA')
mbasepes.insert(len(mbasepes.columns), "REGION", np.floor(mbasepes["PUMA"]/10**6))
if tagrmsp == 1:
    geocwrm_sp = geocw[["PUMA", "REGION"]]
    geocwrm_sp = geocwrm_sp.drop_duplicates(subset=["PUMA"])
    geocwrm_sp.rename(columns=
                {"REGION":"REGION2"},
                inplace=True)    
    mbasepes = pd.merge(mbasepes, geocwrm_sp, how='inner', on='PUMA')
    mbasepes["REGION"] = np.where(mbasepes["REGION"]==3550308, mbasepes["REGION2"], mbasepes["REGION"])
    
""" --- Tratamento de dados dos arquivos de microdados de domicílios --- """

aba = "DOMI"
dic = pd.read_excel(pasta+arqdic, usecols="A,J,K", skiprows=1, header=0, sheet_name=aba)
dic.columns = ["var", "int", "dec"]
dic.fillna(0, inplace=True)
dic = dic.astype({"dec": int})
dic["tam"] = dic["int"]+dic["dec"]
if tagrmsp == 0:
    mbasedom = pd.read_fwf(pasta+uf+arqdom, header=None, widths=dic["tam"])
if tagrmsp == 1:
    mbasedom = pd.read_fwf(r"D:\Users\rodrigo.ajauskas\Documents\Rodrigo Ajauskas 2020\ACADEMICO\Arquivos BR\Microdados SP2-RM"+"/"+arqdom, header=None, widths=dic["tam"])
mbasedom.columns = dic["var"]
mbasedom["HHINCADJ"] = mbasedom["V6532"]/(10**5) #TODO: (i) deixar automatico pelo decimal
mbasedom["WGTP"] = mbasedom["V0010"]/(10**13) #TODO: (i) deixar automatico pelo decimal
#mbasedom["MOTOIBGE"] = mbasedom["V0221"] #a verificar se fica ou não
#mbasedom["AUTOIBGE"] = mbasedom["V0222"]
mbasedom["MOTO"] = -mbasedom["V0221"]+2 #corrige de 1=sim/2=não para 0=não/1=sim #a verificar se fica ou não
mbasedom["AUTO"] = -mbasedom["V0222"]+2 #corrige de 1=sim/2=não para 0=não/1=sim
mbasedom["HHAUT"] = mbasedom["AUTO"]
mbasedom["HHAUT"] = np.where(mbasedom["HHAUT"] == 2, 1, mbasedom["HHAUT"])
mbasedom["HHAUT"] = np.where(mbasedom["HHAUT"] != 1, 0, mbasedom["HHAUT"]) #se "branco", então auto/moto não disp.
mbasedom["HHMOT"] = mbasedom["MOTO"]
mbasedom["HHMOT"] = np.where(mbasedom["HHMOT"] == 2, 1, mbasedom["HHMOT"])
mbasedom["HHMOT"] = np.where(mbasedom["HHMOT"] != 1, 0, mbasedom["HHMOT"]) #se "branco", então auto/moto não disp.

mbasedom.rename(columns=
                {"V0011":"PUMA",
                "V0300":"hhnum2",
                "V0401":"NP",
                "V4001":"TIPODOM"},
                inplace=True)

mbasedom = mbasedom[mbasedom["TIPODOM"]==1] #filtra a base para manter apenas domicilios particulares
mbasedom = mbasedom[["PUMA","WGTP","hhnum2","TIPODOM","HHINCADJ","NP","MOTO", "AUTO", "HHAUT", "HHMOT"]]

""" Aplicação da seleção para municípios de interesse """
dfpuma = pd.DataFrame(geocw["PUMA"].unique(), columns=["PUMA"])
mbasedom = pd.merge(dfpuma, mbasedom, how='left', on='PUMA')

""" Correspondencia entre id e hhnum2 do censo """
mbasedom["hhnum"] = mbasedom.index + 1
hhhhnum = mbasedom[["hhnum2"]+["hhnum"]] #tabela de correspondencia entre indice e hhnum2 do censo
print(hhhhnum)

""" Presença de criança no domicílio """
transf2 = mbasepes[["hhnum2", "RELP", "AGEP"]]
agecrian = transf2["AGEP"].where(transf2["AGEP"]<18)
agecrian = agecrian[~agecrian.isin(["NaN"])].index
print(agecrian)
transf2 = transf2[transf2.index.isin(agecrian)]
print(transf2)
transf2 = pd.DataFrame(transf2["hhnum2"].unique(), columns=["hhnum2"])
transf2.insert(len(transf2.columns), "HHCRIAN", 1)
print(transf2)
mbasedom = pd.merge(mbasedom, transf2, how='left', on='hhnum2') #insere coluna de presença de crianças na planilha de domicilios
mbasedom["HHCRIAN"] = np.where(mbasedom["HHCRIAN"] != 1, 0, mbasedom["HHCRIAN"])
mbasedom = mbasedom[mbasedom.columns.drop(list(mbasedom.filter(regex='RELP')))] #exclui RELP na tabela de pessoas
mbasedom = mbasedom[mbasedom.columns.drop(list(mbasedom.filter(regex='AGEP')))] #exclui AGEP na tabela de pessoas
print(mbasedom) #XXX a deixar único
#a = pd.pivot_table(transf2, index='AGEP', aggfunc=np.count_nonzero)
#print(sum(a["RELP"]))
#print(a)

""" Idade do responsavel: transferência da tabela PESS para o seed_households """
transf = mbasepes[["hhnum2", "RELP", "AGEP"]]
resp = transf["RELP"].isin([1, 20])
resp = transf[transf["RELP"].isin([1, 20])].index #identifica linhas que correspondem ao responsável pelo domicílio (ou individual em dom. coletivo)
print(resp)
#naoresp = transf[(transf["RELP"]!=1)].index #identifica linhas que não correspondem ao responsável pelo domicílio
transf = transf[transf.index.isin(resp)] #seleciona linhas que correspondem ao responsável pelo domicílio, deixando apenas os responsaveis
print(transf)
#transf.drop(naoresp, inplace=True) #exclui linhas que não correspondem ao responsável pelo domicílio, deixando apenas os responsaveis
transf.rename(columns={"AGEP":"AGEHOH"},inplace=True)
mbasedom = pd.merge(mbasedom, transf, how='left', on='hhnum2') #insere coluna de idade do responsavel na planilha de domicilios
mbasedom = mbasedom[mbasedom.columns.drop(list(mbasedom.filter(regex='RELP')))] #exclui RELP na tabela de pessoas
mbasedom.insert(len(mbasedom.columns), "REGION", np.floor(mbasedom["PUMA"]/10**6))
if tagrmsp == 1: 
    mbasedom = pd.merge(mbasedom, geocwrm_sp, how='inner', on='PUMA')
    mbasedom["REGION"] = np.where(mbasedom["REGION"]==3550308, mbasedom["REGION2"], mbasedom["REGION"])

""" Renda para relação de parentesco tipo 20: transferência da tabela PESS para o seed_households e junção com HHINCADJ """
transfr20 = mbasepes[["hhnum2", "RELP", "REND"]]
rend20 = transfr20[(transfr20["RELP"]==20)].index
transfr20 = transfr20[transfr20.index.isin(rend20)]
mbasedom = pd.merge(mbasedom, transfr20, how='left', on='hhnum2') #insere renda para relp=20
mbasedom["REND"].fillna(0, inplace=True)
mbasedom["HHINCADJ"].fillna(0, inplace=True)
mbasedom["HHINCADJ"] = mbasedom["HHINCADJ"] + mbasedom["REND"]
mbasedom = mbasedom[mbasedom.columns.drop(list(mbasedom.filter(regex='RELP')))] #exclui RELP na tabela de pessoas
mbasedom = mbasedom[mbasedom.columns.drop(list(mbasedom.filter(regex='REND')))] #exclui REND na tabela de pessoas

""" Criação dos arquivos com dados tratados """
#dic2.info()
dic2.to_csv(auxi+'/dicP.csv')
mbasepes = pd.merge(mbasepes, hhhhnum, how='left', on='hhnum2') #corresp id e cod domicilio censo
mbasepes = mbasepes.apply(pd.to_numeric, errors='coerce', downcast='integer') #XXX
mbasepes = mbasepes[mbasepes.columns.drop(list(mbasepes.filter(regex='REND')))] #exclui RELP na tabela de pessoas
mbasepes = mbasepes[~np.isnan(mbasepes["hhnum"])] #XXX verificar se funciona - exclui pessoas de domicilios sem hhnum (isto é, de domicílios que não são particulares)
mbasepes.to_csv(data+'/seed_persons.csv', index=False)
mbasepes.columns = mbasepes.columns.get_level_values(0) #XXX
mbasepes.info()

#dic.info()
dic.to_csv(auxi+'/dicD.csv')
#mbasedom = mbasedom.astype({"AGEHOH": "int64"}) 
mbasedom.columns = mbasedom.columns.get_level_values(0) #XXX
mbasedom.to_csv(data+'/seed_households.csv', index=False)
mbasedom = mbasedom.apply(pd.to_numeric, errors='coerce', downcast='integer') #XXX
mbasedom.info()

print(mbasepes.columns)
print(mbasedom)

tparseg = np.around(par-inicio,decimals=1)
fim = time.time()
texecseg = np.around(fim-inicio,decimals=1)
texecmin = np.around((fim-inicio)/60,decimals=1)
numhh = mbasedom["hhnum2"].nunique()
numind = mbasedom["NP"].sum()
numhhe = int(mbasedom["WGTP"].sum())
numinde = int(mbasepes["PWGTP"].sum())

print(">>> Na semente : "+str(numhh)+" Domicílios"+" | "+str(numind)+" Indivíduos")
print(">>> Expandido : "+str(numhhe)+" Domicílios"+" | "+str(numinde)+" Indivíduos")
print("\n"+"Tempo de leitura do fwf: "+str(tparseg)+" segundos")
print("Tempo de execução: "+str(texecseg)+" segundos ("+str(texecmin)+ " minutos)")