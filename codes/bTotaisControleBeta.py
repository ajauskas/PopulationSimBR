"""
PopulationSimBR | Codigo para Tratamento dos Dados de Entrada - 1 Totais de Controle
@author: rodrigo.ajauskas
"""
#TODO: Trocar titulo das colunas após teste do PopulationSim

import pandas as pd
import numpy as np

pasta = "bruto/"
data = "PopulationSimBR/data/"
configs = 'PopulationSimBR/configs/'
valid = 'PopulationSimBR/validacao/'
pastacomb = "/VarCombinadas"

parte = 4
arqmun = "municipios"+str(parte)+".yaml"

varcombinadas = 0 #Procedimento: teste para variáveis não controladas

""" Identificação dos municípios a sintetizar no arquivo configs/municipios.yaml """
import yaml
abrirmunicipios = yaml.load(open(configs+arqmun), Loader=yaml.FullLoader)
listamunicipios = abrirmunicipios["municipios"]
abruf = abrirmunicipios["abreviacao_uf"]
tagrmsp = abrirmunicipios["tag_rmsp"]
if tagrmsp == 1: #temporario
    pasta = "D:/Data/r.ajauskas/Documents/Pessoal/Diss/IBGE-AgSC/SP1/CSV/"
    if listamunicipios[0] != "São Paulo":
        pasta = "D:/Data/r.ajauskas/Documents/Pessoal/Diss/IBGE-AgSC/SP2/CSV/"
    
""" Continuação da seção de nome de pastas e arquivos """
c = ".csv"
ufbarra = abruf+"/"
if tagrmsp == 1: 
    ufbarra = ""   
if listamunicipios[0] == "São Paulo":
    abruf = abruf+"1"
arqdom1 = "Domicilio01_"+abruf+c
arqres2 = "Responsavel02_"+abruf+c
arqdore = "DomicilioRenda_"+abruf+c
if tagrmsp == 1 and listamunicipios[0] != "São Paulo": #alguns dos arquivos do Censo para a o Estado de SP tem sufixo "SP2" (todos menos os arquivos "PessoaXX")
    arqdom1 = "Domicilio01_"+abruf+"2"+c
    arqres2 = "Responsavel02_"+abruf+"2"+c
    arqdore = "DomicilioRenda_"+abruf+"2"+c
arqp03 = "Pessoa03_"+abruf+c
arqp11 = "Pessoa11_"+abruf+c
arqp12 = "Pessoa12_"+abruf+c
arqcomp = "geo_cross_walk.csv"

""" --- Extracao de dados das planilhas de controle e criacao de classes --- """

""" Número de pessoas """
dom1 = pd.read_csv(pasta+ufbarra+arqdom1, sep=';', engine='python')

varini = 50 #variavel inicial a ser extraida, inclusive
varfin = 59 #variavel final a ser extraida, inclusive
a = ["V"]*(varfin-varini+1)
z = ["0"]*(varfin-varini+1)
b = range(varini,varfin+1)
b = list(map(str, b))
b = ["0"+cod if len(cod)==1 else cod for cod in b]       
lista = [i + j + k for i, j, k in zip(a, z, b)] 

dom1 = dom1[["V001"]+["V002"]+["Cod_setor"]+lista]

dom1 = dom1.apply(pd.to_numeric, errors='coerce')
dom1.rename(columns=
            {"V001":"HHTOTAL",
            "V002":"HHBASE", #V001 inclui domicílios coletivos, V002 é apenas particulares
            "V050":"HHSIZE1",
            "V051":"HHSIZE2",
            "V052":"HHSIZE3",
            "V053":"HHSIZE4",
            "V054":"HHSIZE5"},
            inplace=True) 
dom1["HHSIZE6"] = dom1["V055"]+dom1["V056"]+dom1["V057"]+dom1["V058"]+dom1["V059"]
dom1["HHSIZE5"] = np.where(np.isnan(dom1["HHSIZE5"]), 0, dom1["HHSIZE5"])
dom1["HHSIZE6"] = np.where(np.isnan(dom1["HHSIZE6"]), 0, dom1["HHSIZE6"])
dom1["HHDC"] = dom1["HHTOTAL"]-dom1["HHBASE"]

""" Para identificar os setores com celulas vazias (indicadas com "X" no Censo)
    e posteriormente preenchê-las em função da distribuição de contagem dos demais setores censitários filtrados """
dom1["XFLAG"] = np.where(np.isnan(dom1["HHSIZE1"]), 1, 0)

dom1 = dom1[dom1.columns.drop(list(dom1.filter(regex='V')))] #eliminar atributos originais
#print(dom1.info())

""" Idade do responsável pelo domicílio """
#print(pasta+ufbarra+arqres2)
res2 = pd.read_csv(pasta+ufbarra+arqres2, sep=',', engine='python')
if listamunicipios[0] == "São Paulo": #o arquivo "responsavel02_sp2.csv" utiliza "," como separador a
    res2 = pd.read_csv(pasta+ufbarra+arqres2, sep=';', engine='python')


varini = 2 #variavel inicial a ser extraida, inclusive
varfin = 92 #variavel final a ser extraida, inclusive
#estrutura: classes de 5 em 5 anos, desagrupadas por 5 cor ou raça
lista=[]
for i in range(varini,varfin+1):
    if i < 10:
        var = "00"+str(i)
    if (i >= 10 and i < 100):
        var = "0"+str(i)
    if i > 100:
        var = i
    lista.append("V"+str(var))
    
"""varini = 2 #variavel inicial a ser extraida, inclusive
varfin = 92 #variavel final a ser extraida, inclusive
a = ["V"]*(varfin-varini+1)
z = ["0"]*(varfin-varini+1)
b = range(varini,varfin+1)
b = list(map(str, b))
b = ["0"+cod if len(cod)==1 else cod for cod in b]    
lista = [i + j + k for i, j, k in zip(a, z, b)] """
res2 = res2[["Cod_setor"]+lista]

res2 = res2.apply(pd.to_numeric, errors='coerce')
#classes de idades
#10a29: v002-21
res2["HHAGE1"] = res2["V002"]+res2["V003"]+res2["V004"]+res2["V005"]+res2["V006"]+res2["V007"]+res2["V008"]+res2["V009"]+res2["V010"]+res2["V011"]+res2["V012"]+res2["V013"]+res2["V014"]+res2["V015"]+res2["V016"]+res2["V017"]+res2["V018"]+res2["V019"]+res2["V020"]+res2["V021"]
#30a44: v022-36
res2["HHAGE2"] = res2["V022"]+res2["V023"]+res2["V024"]+res2["V025"]+res2["V026"]+res2["V027"]+res2["V028"]+res2["V029"]+res2["V030"]+res2["V031"]+res2["V032"]+res2["V033"]+res2["V034"]+res2["V035"]+res2["V036"]
#45a59: v037-51
res2["HHAGE3"] = res2["V037"]+res2["V038"]+res2["V039"]+res2["V040"]+res2["V041"]+res2["V042"]+res2["V043"]+res2["V044"]+res2["V045"]+res2["V046"]+res2["V047"]+res2["V048"]+res2["V049"]+res2["V050"]+res2["V051"]
#60a100+: v052-92
res2["HHAGE4"] = res2["V052"]+res2["V053"]+res2["V054"]+res2["V055"]+res2["V056"]+res2["V057"]+res2["V058"]+res2["V059"]+res2["V060"]+res2["V061"]+res2["V062"]+res2["V063"]+res2["V064"]+res2["V065"]+res2["V066"]+res2["V067"]+res2["V068"]+res2["V069"]+res2["V070"]+res2["V071"]+res2["V072"]+res2["V073"]+res2["V074"]+res2["V075"]+res2["V076"]+res2["V077"]+res2["V078"]+res2["V079"]+res2["V080"]+res2["V081"]+res2["V082"]+res2["V083"]+res2["V084"]+res2["V085"]+res2["V086"]+res2["V087"]+res2["V088"]+res2["V089"]+res2["V090"]+res2["V091"]+res2["V092"]
res2 = res2[res2.columns.drop(list(res2.filter(regex='V')))] #eliminar atributos originais

""" Idade da pessoa """
pes3 = pd.read_csv(pasta+ufbarra+arqp03, sep=';', engine='python')

varini = 7 #variavel inicial a ser extraida, inclusive
varfin = 246 #variavel final a ser extraida, inclusive
#estrutura: classes de 5 em 5 anos, desagrupadas por 5 cor ou raça
lista=[]
for i in range(varini,varfin+1):
    if i < 10:
        var = "00"+str(i)
    if (i >= 10 and i < 100):
        var = "0"+str(i)
    if i > 100:
        var = i
    lista.append("V"+str(var))

pes3 = pes3[["V001"]+["Cod_setor"]+lista]
pes3.rename(columns={"V001":"POPTOTAL"},inplace=True) 

pes3 = pes3.apply(pd.to_numeric, errors='coerce')
#classes de idades
pes3["AGEP01"] = pes3["V007"]+pes3["V008"]+pes3["V009"]+pes3["V010"]+pes3["V011"] #0a4 anos de idade
pes3["AGEP02"] = pes3["V012"]+pes3["V013"]+pes3["V014"]+pes3["V015"]+pes3["V016"] #5a9
pes3["AGEP03"] = pes3["V017"]+pes3["V018"]+pes3["V019"]+pes3["V020"]+pes3["V021"] #10a14
pes3["AGEP04"] = pes3["V022"]+pes3["V023"]+pes3["V024"]+pes3["V025"]+pes3["V026"] #15a19
pes3["AGEP05"] = pes3["V037"]+pes3["V038"]+pes3["V039"]+pes3["V040"]+pes3["V041"] #20a24 (há salto devido a desagregações da classe anterior)
pes3["AGEP06"] = pes3["V042"]+pes3["V043"]+pes3["V044"]+pes3["V045"]+pes3["V046"] #25a29
pes3["AGEP07"] = pes3["V047"]+pes3["V048"]+pes3["V049"]+pes3["V050"]+pes3["V051"] #30a34
pes3["AGEP08"] = pes3["V052"]+pes3["V053"]+pes3["V054"]+pes3["V055"]+pes3["V056"] #35a39
pes3["AGEP09"] = pes3["V057"]+pes3["V058"]+pes3["V059"]+pes3["V060"]+pes3["V061"] #40a44
pes3["AGEP10"] = pes3["V062"]+pes3["V063"]+pes3["V064"]+pes3["V065"]+pes3["V066"] #45a49
pes3["AGEP11"] = pes3["V067"]+pes3["V068"]+pes3["V069"]+pes3["V070"]+pes3["V071"] #50a54
pes3["AGEP12"] = pes3["V072"]+pes3["V073"]+pes3["V074"]+pes3["V075"]+pes3["V076"] #55a59
pes3["AGEP13"] = pes3["V077"]+pes3["V078"]+pes3["V079"]+pes3["V080"]+pes3["V081"] #60a69 (classe com 10 anos ao invés de 5 anos)
pes3["AGEP14"] = pes3["V082"]+pes3["V083"]+pes3["V084"]+pes3["V085"]+pes3["V086"] #70+

""" Agregando mais os grupos de idade (redução de 14 p/ 9 categorias) """
pes3["AGEP1"] = pes3["AGEP01"]                  #0a4
pes3["AGEP2"] = pes3["AGEP02"]+pes3["AGEP03"]   #5a14
pes3["AGEP3"] = pes3["AGEP04"]                  #15a19
pes3["AGEP4"] = pes3["AGEP05"]+pes3["AGEP06"]   #20a29
pes3["AGEP5"] = pes3["AGEP07"]+pes3["AGEP08"]   #30a39
pes3["AGEP6"] = pes3["AGEP09"]+pes3["AGEP10"]   #40a49
pes3["AGEP7"] = pes3["AGEP11"]+pes3["AGEP12"]   #50a59
pes3["AGEP8"] = pes3["AGEP13"]+pes3["AGEP14"]   #60+

""" Extração de variáveis cruzadas não controladas para etapa de validação """
if varcombinadas == 1: #Procedimento: teste para variáveis não controladas
    pes3["AGEM4"] = pes3["V117"]+pes3["V118"]+pes3["V119"]+pes3["V120"]+pes3["V121"]+pes3["V122"]+pes3["V123"]+pes3["V124"]+pes3["V125"]+pes3["V126"] #Masculino, idade entre 20 e 29
    pes3["AGEF4"] = pes3["V197"]+pes3["V198"]+pes3["V199"]+pes3["V200"]+pes3["V201"]+pes3["V202"]+pes3["V203"]+pes3["V204"]+pes3["V205"]+pes3["V206"] #F,20a29
    pes3["AGEM7"] = pes3["V147"]+pes3["V148"]+pes3["V149"]+pes3["V150"]+pes3["V151"]+pes3["V152"]+pes3["V153"]+pes3["V154"]+pes3["V155"]+pes3["V156"] #M,50a59
    pes3["AGEF7"] = pes3["V227"]+pes3["V228"]+pes3["V229"]+pes3["V230"]+pes3["V231"]+pes3["V232"]+pes3["V233"]+pes3["V234"]+pes3["V235"]+pes3["V236"] #F,50a59
    pes3["TST4"] = pes3["AGEP4"]-(pes3["AGEM4"]+pes3["AGEF4"])
    pes3["TST7"] = pes3["AGEP7"]-(pes3["AGEM7"]+pes3["AGEF7"])
    validcruz = pes3[["Cod_setor","AGEP4","AGEM4","AGEF4","AGEP7","AGEM7","AGEF7","TST4","TST7"]]
    validcruz.rename(columns={"Cod_setor":"TAZ"},inplace=True) 
    pes3 = pes3[["Cod_setor", "POPTOTAL", "AGEP1", "AGEP2", "AGEP3", "AGEP4", "AGEP5", "AGEP6", "AGEP7", "AGEP8"]]

""" Renda familiar """
dore = pd.read_csv(pasta+ufbarra+arqdore, sep=';', engine='python')

varini = 5 #variavel inicial a ser extraida, inclusive
varfin = 14 #variavel final a ser extraida, inclusive
a = ["V"]*(varfin-varini+1)
z = ["0"]*(varfin-varini+1)
b = range(varini,varfin+1)
b = list(map(str, b))
b = ["0"+cod if len(cod)==1 else cod for cod in b]    
lista = [i + j + k for i, j, k in zip(a, z, b)] 
dore = dore[["Cod_setor"]+lista]

dore = dore.apply(pd.to_numeric, errors='coerce')
dore["HHINC1"] = dore["V005"]+dore["V006"]+dore["V007"]+dore["V014"]   #renda domiciliar: ate 0.5SM per capita
dore["HHINC2"] = dore["V008"]                                          #0.5a1SM per capita
dore["HHINC3"] = dore["V009"]                                          #1a2SM per capita
dore["HHINC4"] = dore["V010"]                                          #2a3SM per capita
dore["HHINC5"] = dore["V011"]                                          #3a5SM per capita
dore["HHINC6"] = dore["V012"]+dore["V013"]                             #5+SM per capita
#Observação: V014: Domicílios particulares sem rendimento nominal mensal domiciliar per capita

dore = dore[dore.columns.drop(list(dore.filter(regex='V')))] #eliminar atributos originais

""" Sexo
    Legenda para sufixo:    
        Números:    
            1 = Masculino; 2 = Feminino
        Letras:
            _DT = moradores de domicílios particulares + coletivos (T de total);
            _DP = moradores de domicílios coletivos;
            (vazio) = moradores de domicílios particulares """
    
p11 = pd.read_csv(pasta+ufbarra+arqp11, sep=';', engine='python')
p11 = p11[["Cod_setor"]+["V001"]+["V002"]]
p11.rename(columns={"V001":"SEX1_DT", "V002":"SEX1"}, inplace=True)
p11 = p11.apply(pd.to_numeric, errors='coerce', downcast='integer') 
p11["SEX1"] = np.where(dom1["XFLAG"]==1, p11["SEX1_DT"],p11["SEX1"])
p11["SEX1_DC"] = p11["SEX1_DT"]-p11["SEX1"]

p12 = pd.read_csv(pasta+ufbarra+arqp12, sep=';', engine='python')
p12 = p12[["Cod_setor"]+["V001"]+["V002"]]
p12.rename(columns={"V001":"SEX2_DT", "V002":"SEX2"}, inplace=True)
p12 = p12.apply(pd.to_numeric, errors='coerce', downcast='integer')
p12["SEX2"] = np.where(dom1["XFLAG"]==1, p12["SEX2_DT"],p12["SEX2"])
p12["SEX2_DC"] = p12["SEX2_DT"]-p12["SEX2"]

sexo = pd.merge(p11, p12, how='left', on='Cod_setor')
sexo["POPBASE"] = sexo["SEX1"]+sexo["SEX2"]
sexo["POPDC"] = sexo["SEX1_DC"]+sexo["SEX2_DC"]

""" --- União de tabelas --- """
base = pd.merge(dom1, res2, how='left', on='Cod_setor') 
base = pd.merge(base, dore, how='left', on='Cod_setor')
base = pd.merge(base, pes3, how='left', on='Cod_setor')
base = pd.merge(base, sexo, how='left', on='Cod_setor')
base.rename(columns={"Cod_setor":"TAZ"}, inplace=True)

base["HHFAT"]=base["HHBASE"]/base["HHTOTAL"]
base["POPFAT"]=base["POPBASE"]/base["POPTOTAL"]

""" Função propx: distribuição proporcional para atributos desconhecidos
    - Entradas:
        atr : atributo,
        cats : número de categorias,
        qbase : referência de base (domicílios:HHBASE ou indivíduos:POPBASE; se for MIX: HHDC e POPDC, respectivamente),
        flag: qual coluna de "flag" examinar (células vazias:XFLAG ou setores mistos:MIXFLAG)
    - Saída:
        vetor com pesos de cada categoria de cada variável """ 
        
def propx(atr,cats,qbase,flag):
    base[atr+"_AC"] = 0
    fatvec = []
    fatvecn = []
    for i in range(0,cats):
        fatvec.append(base[atr+str(i+1)].mean())
    s = sum(fatvec)
    for i in range(0,cats):
        fatvecn.append(fatvec[i]/s) #criação do vetor de pesos de cada categoria de uma dada variável
        if i != (cats-1):
            base[atr+str(i+1)] = np.where(base[flag]==1, np.floor(base[qbase]*fatvecn[i]), base[atr+str(i+1)])                 
            base[atr+"_AC"] += base[atr+str(i+1)]
        if i == (cats-1):
            base[atr+str(i+1)] = np.where(base[flag]==1, base[qbase]-base[atr+"_AC"], base[atr+str(i+1)]) #última categoria recebe o resto
            
def redmix(atr,cats,qbase,qfat,flag):
    base[atr+"_AC"] = 0
    base[atr+"_SOMA"] = 0
    for j in range(0,cats):
            base[atr+"_SOMA"] += base[atr+str(j+1)]
    for i in range(0,cats):
        if i != (cats-1):
            base[atr+str(i+1)] = np.where(base[flag]==1, np.floor(base[atr+str(i+1)]*base[qbase]/base[atr+"_SOMA"]), base[atr+str(i+1)])
            base[atr+"_AC"] += base[atr+str(i+1)]
        if i == (cats-1):
            base[atr+str(i+1)] = np.where(base[flag]==1, base[qbase]-base[atr+"_AC"], base[atr+str(i+1)]) #última categoria recebe o resto    
            
""" Para ponderar o atributo de idade para apenas moradores de domicílios particulares
    em função da distribuição de contagem dos demais setores censitários filtrados """
base["MIXFLAG"] = np.where(np.logical_and(np.not_equal(base["POPDC"], 0) , np.not_equal(base["POPBASE"], 0)), 1, 0)
            
""" Aplicação da função "propx" """           
#Para XFLAG 
propx("HHSIZE", 6,"HHBASE" ,"XFLAG"  )
propx("HHAGE" , 4,"HHBASE" ,"XFLAG"  )
propx("HHINC" , 6,"HHBASE" ,"XFLAG"  )
propx("AGEP"  , 8,"POPBASE","XFLAG"  )
# SEX não exige este processo pois está disponível diretamente no Censo (variável V002: "homens/mulheres em domicílios particulares permanentes")


""" Redução proporcional das contagens de indivíduos em setores censitários em
    que há tanto domicílios particulares como coletivos (POPDC diferente de 0) """
#Para MIXFLAG
#HHSIZE já é apenas para domicílios particulares, não há necessidade de transformar
redmix("HHAGE"  , 4,"HHBASE","HHFAT","MIXFLAG")
redmix("HHINC"  , 6,"HHBASE","HHFAT","MIXFLAG")
redmix("AGEP"   , 8,"POPBASE","POPFAT","MIXFLAG")
#SEX não exige este processo pois está disponível diretamente no Censo (variável V002: "homens/mulheres em domicílios particulares permanentes")
print(sum(base["SEX1"]))


""" --- Aplicação da seleção para municípios de interesse & inserção de região --- """
geocw = pd.read_csv(data+arqcomp)
if varcombinadas == 1: #Procedimento: teste para variáveis não controladas
    validcruz = pd.merge(geocw, validcruz, how='left', on='TAZ')
base = pd.merge(geocw, base, how='left', on='TAZ')
colpuma = base.pop("PUMA")
base.insert(len(base.columns), "PUMA", colpuma)
colregion = base.pop("REGION")
base.insert(len(base.columns), "REGION", np.floor(base["PUMA"]/10**6))
if tagrmsp == 1 and listamunicipios[0] == "São Paulo":
    base["REGION"] = np.floor(base["TAZ"]/10**6)
base = base.apply(pd.to_numeric, errors='coerce', downcast='integer')

base = base[(base["POPBASE"]/base["HHBASE"])<30] #elimina domicílios cuja relação POPBASE/HHBASE>30, provaveis erros (população residente em domicílios particulares sobre a população residente em domicílios particulares) 
""" Para ordenar colunas e limpar campos auxiliares de verificação criados """
""" Atenção: modificar se alterar variáveis ou número de categorias """
base = base[["TAZ","PUMA","REGION","XFLAG","MIXFLAG","HHBASE","HHSIZE1","HHSIZE2","HHSIZE3","HHSIZE4","HHSIZE5","HHSIZE6","HHAGE1","HHAGE2","HHAGE3","HHAGE4","HHINC1","HHINC2","HHINC3","HHINC4","HHINC5","HHINC6","POPBASE","AGEP1","AGEP2","AGEP3","AGEP4","AGEP5","AGEP6","AGEP7","AGEP8","SEX1","SEX2"]]

""" --- Criação do control_totals_taz filtrado --- """
base.to_csv(data+'/control_totals_taz.csv', index=False)

if varcombinadas == 1: #Procedimento: teste para variáveis não controladas
    validcruz.to_csv(valid+pastacomb+'/VarComb_Totais.csv', index=False)

print(base.info())
print(base)
print(base.columns)