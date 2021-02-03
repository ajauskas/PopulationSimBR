"""
PopulationSimBR | Codigo para Tratamento dos Dados de Entrada - 5 Meta Controle: OD 2017 Sao Paulo 
@author: rodrigo.ajauskas
"""

import pandas as pd
import numpy as np

pasta = "bruto/"
od = "OD/"
bd = "Banco de dados/"
odgeocw = "Corresp2007_2017.xlsx"
tg = "Tabelas Gerais/"
tabs = "Dados Gerais OD2017.xlsx"
ibgeodcw = "ibgeod_cross_walk.csv"
data = "PopulationSimBR/data/"
# não tem "parte" (consulta à arquivo de municípios) pq 

""" Criação de arquivo de geocrosswalk a partir de tabela da Pesquisa OD 2017 """
corresp = pd.read_excel(pasta+od+bd+odgeocw, sheet_name='Correspondência', usecols="B,F,G", skiprows=5)
corresp.columns = ["ZOD", "DistOD", "NomeDist"]
corresp.to_csv("correspod.csv", index=False, encoding="latin")
#print(corresp)

""" --- Identificação de atributos nas tabelas da Pesquisa OD --- """

""" Domicílios sem auto (HHAUT0) e com auto (HHAUT1) """
numauto = pd.read_excel(pasta+od+tg+tabs, sheet_name='Tabela 7', skiprows=6, nrows=517)
numauto.columns = ["ZOD", "0a", "1a", "2a", "3a+", "Total"]
numauto["HHAUT0"] = numauto["0a"]
numauto["HHAUT1"] = numauto["1a"]+numauto["2a"]+numauto["3a+"]
numauto = numauto[["ZOD","HHAUT0","HHAUT1"]]

""" Nível de instrução (EDUC) """
popeduc = pd.read_excel(pasta+od+tg+tabs, sheet_name='Tabela 3', skiprows=7, nrows=517)
popeduc.columns = ["ZOD", "1a", "1b", "EDUC2", "EDUC3", "EDUC4", "Total"]
popeduc["EDUC1"] = popeduc["1a"] + popeduc["1b"] #agregação de acordo com microdados do IBGE
popeduc = popeduc[["ZOD","EDUC1","EDUC2","EDUC3","EDUC4","Total"]]

""" Agregação das informações no nível geográfico de zona OD para distrito/município """
from_od0 = pd.merge(numauto, popeduc, how='left', on='ZOD')
from_od = pd.merge(from_od0, corresp, how='left', on='ZOD')
from_odpv = pd.pivot_table(from_od, index='DistOD', aggfunc=np.sum)
from_odpv.to_csv("numautopv.csv")

#popeduc = pd.merge(popeduc, corresp, how='left', on='ZOD')
#popeducpv = pd.pivot_table(popeduc, index='DistOD', aggfunc=np.sum)
#popeducpv.to_csv("popeducpv.csv")

""" União com tabela gerada manualmente (ibgeod_cross_walk.csv) contendo correspondência entre
    (i) código da zona OD, entre 1 e 517, e (ii) código do IBGE de cada distrito e município """
ibgeod = pd.read_csv(pasta+ibgeodcw, sep=';', engine='python')
ibgeod = ibgeod[["Cod_municipio","Cod_distrito","Nome_do_distrito","DistOD"]]

metactrlod = pd.merge(ibgeod, from_odpv, how='left', on='DistOD')
metactrlod["REGION"] = np.where(metactrlod["Cod_distrito"]>0, metactrlod["Cod_distrito"], metactrlod["Cod_municipio"])
metactrlod = metactrlod[["REGION","DistOD","Nome_do_distrito","HHAUT0","HHAUT1","EDUC1","EDUC2","EDUC3","EDUC4"]]

metactrlod["HHAUT0"] = np.floor(metactrlod["HHAUT0"])
metactrlod["HHAUT1"] = np.floor(metactrlod["HHAUT1"])
metactrlod["HH_ODSP"] = metactrlod["HHAUT0"]+metactrlod["HHAUT1"]

metactrlod["EDUC1"] = np.floor(metactrlod["EDUC1"])
metactrlod["EDUC2"] = np.floor(metactrlod["EDUC2"])
metactrlod["EDUC3"] = np.floor(metactrlod["EDUC3"])
metactrlod["EDUC4"] = np.floor(metactrlod["EDUC4"])
metactrlod["POP_ODSP"] = metactrlod["EDUC1"]+metactrlod["EDUC2"]+metactrlod["EDUC3"]+metactrlod["EDUC4"]

""" "Scale": Ajuste do ano base de 2017 (ano da OD) para 2010 (ano do Censo),
    proporcional à alteração do número de domicílios em cada REGION (distrito/município)
    Variáveis com valores reduzidos indicadas com sufixo _ (underline) """

"""
#Para ajustar via semente
basehh = pd.read_csv(data+'/seed_households.csv', sep=',', engine='python')
totalhhibge = pd.pivot_table(basehh, index='REGION', aggfunc=np.sum)
totalhhibge = totalhhibge[["WGTP"]]
totalhhibge.rename(columns= {"WGTP":"HH_IBGE"}, inplace=True)
baseind = pd.read_csv(data+'/seed_persons.csv', sep=',', engine='python')
baseind["POP_IBGE"] = np.where(baseind["EDUC"]==5, 0, baseind["PWGTP"])
totalpopibge = pd.pivot_table(baseind, index='REGION', aggfunc=np.sum)
totalpopibge = totalpopibge[["POP_IBGE"]]
ajuste = pd.merge(metactrlod, totalhhibge, how='left', on='REGION')
ajuste = pd.merge(ajuste, totalpopibge, how='left', on='REGION')
"""

#Para ajustar via totais de controle 
totais = pd.read_csv(data+'/control_totals_taz.csv', sep=',', engine='python')
totais = pd.pivot_table(totais, index='REGION', aggfunc=np.sum)
totais = totais[["HHBASE","POPBASE"]]
totais.rename(columns= {"HHBASE":"HH_IBGE", "POPBASE":"POP_IBGE"}, inplace=True)
ajuste = pd.merge(metactrlod, totais, how='left', on='REGION')

ajuste["FatRedHH"] = 1+( (ajuste["HH_IBGE"]-ajuste["HH_ODSP"]) / ajuste["HH_ODSP"] )
ajuste["HHAUT0_"] = np.floor(ajuste["HHAUT0"]*ajuste["FatRedHH"])
ajuste["HHAUT1_"] = np.floor(ajuste["HHAUT1"]*ajuste["FatRedHH"])
ajuste["FatRedPOP"] = 1+( (ajuste["POP_IBGE"]-ajuste["POP_ODSP"]) / ajuste["POP_ODSP"] )
ajuste["EDUC1_"] = np.floor(ajuste["EDUC1"]*ajuste["FatRedPOP"])
ajuste["EDUC2_"] = np.floor(ajuste["EDUC2"]*ajuste["FatRedPOP"])
ajuste["EDUC3_"] = np.floor(ajuste["EDUC3"]*ajuste["FatRedPOP"])
ajuste["EDUC4_"] = np.floor(ajuste["EDUC4"]*ajuste["FatRedPOP"])
print(ajuste)

ajuste.to_csv(data+"control_totals_meta.csv", index=False, encoding="latin")