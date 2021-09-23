"""
PopulationSimBR | Codigo para Validação - 6 Validação
@author: rodrigo.ajauskas
"""

import pandas as pd
import datetime
import numpy as np

av_varcruz = 0 #usuário: avaliar variaveis cruzadas? 0 para não, 1 para sim

controle = []
output = 'PopulationSimBR/output/'
configs = 'PopulationSimBR/configs/'    
valid = 'PopulationSimBR/validacao/'
pastacomb = "/VarCombinadas/"
pop = 'PopulationSimBR/'
arq = 'final_summary_TAZ.csv' 
arqmeta = 'final_summary_TAZ_PUMA.csv' #XXX _PUMA adicionado pra verificar controles meta
controls = 'controls.csv'
ctrl = pd.read_csv(configs+controls)
ctrlp = ctrl[['geography']+['target']+['importance']]
print(ctrlp)
synp = 'synthetic_persons.csv'

""" Procedimentos a realizar (usuário: especificar 0/1) """
metricas = 1 #Procedimento: calculo de 4 metricas de validação
varcombinadas = 0 #Procedimento: teste para variáveis não controladas

if metricas == 1:
    """ Identifica máximo fator de expansão especificado """
    import yaml
    settings = 'settings.yaml'
    a_yaml_file = open(configs+settings)
    iamil = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
    #print(iamil["trace_geography"])
    print(iamil["max_expansion_factor"])
    
    """ Prepara atributos em diferentes abas de um .xls (arquivo Excel) """
    geografias = ["TAZ","META"]
    arqs = [arq, arqmeta]
    print(arqs)
    double = len(ctrl[(ctrl["target"].str.contains('#')) & (ctrl["geography"].str.contains('REGION'))]) #caso conte 2 negativos (REGION e #)
    num_atr = []
    num_atr.append(ctrl["target"].count()-ctrl["target"].str.contains('#').sum()-ctrl["geography"].str.contains('REGION').sum()+double)
    num_atr.append(ctrl["target"].count()-(ctrl["target"].str.contains('#')).sum())
    print(num_atr)
    
    for i in range(2):
        print(geografias[i])
        print(ctrl["target"].count())
        print((ctrl.target.str.contains('#')).sum())
        print(num_atr[i])
        summ = pd.read_csv(output+arqs[i])
        controle = summ.iloc[:,2:2+num_atr[i]]
        print(controle)
        sint = summ.iloc[:,2+num_atr[i]:2+2*num_atr[i]]
        print(sint)
        diff = summ.iloc[:,2+2*num_atr[i]:2+3*num_atr[i]]
        print(diff)
        coluna = geografias[i]
        totcont = controle.sum() #XXX verif
        
        """ Correção do valor de controle para referência do cálculo do Qui-quadrado """
        if geografias[i] == "META":
            listameta1 = ['hh_aut_0_control','hh_aut_1_control']
            listameta2 = ['p_educ_1_control','p_educ_2_control','p_educ_3_control','p_educ_4_control']
            
            controle["soma1"] = 0        
            for j in range(0,len(listameta1)):
                controle["soma1"] += controle[listameta1[j]]
            controle["fmc1"] = controle['num_hh_control']/controle["soma1"]
            for k in range(0,len(listameta1)):
                controle[listameta1[k]] = np.floor(controle[listameta1[k]]*controle["fmc1"])
            controle = controle[controle.columns.drop(list(controle.filter(regex='soma1')))] 
            controle = controle[controle.columns.drop(list(controle.filter(regex='fmc1')))]
    
            controle["soma2"] = 0   
            for j in range(0,len(listameta2)):
                controle["soma2"] += controle[listameta2[j]]
            controle["fmc2"] = (controle['p_sex_masc_control']+controle['p_sex_femi_control'])/controle["soma2"]
            for j in range(0,len(listameta2)):
                controle[listameta2[j]] = np.floor(controle[listameta2[j]]*controle["fmc2"])
            controle = controle[controle.columns.drop(list(controle.filter(regex='soma2')))] 
            controle = controle[controle.columns.drop(list(controle.filter(regex='fmc2')))]
            
            controlecalc = controle.transpose()   
            controlecalc = controlecalc.reset_index()
            controlecalc = controlecalc.drop(['index'], axis=1)
            controlecalc = controlecalc.transpose()  
            sintcalc = sint.transpose()  
            sintcalc = sintcalc.reset_index()
            sintcalc = sintcalc.drop(['index'], axis=1)
            sintcalc = sintcalc.transpose() 
            diff = sintcalc-controlecalc
            
        controle = controle.transpose()   
        totsint = sint.sum()  #XXX verif
        sint = sint.transpose()
        sint.columns = summ["id"] #XXX Para indicar id da geografia
        diff = diff.transpose()
        diff2 = diff.reset_index()
        diff3 = diff2.drop(['index'], axis=1)
        controle2 = controle.reset_index()
        controle3 = controle2.drop(['index'], axis=1)
        diffr = diff3.div(controle3,fill_value=0)
        print(diffr)
        for j in range(0,len(diffr.columns)):
            diffr[j] = np.where(np.isinf(diffr[j]), diff[j], diffr[j])
            #verifica se valor é infinito (resultado da divisão por 0, obtido quando o total de controle é 0) e substitui por 0
        diffr.index = diff.index
            
        """ Média da diferença relativa (negativo pode compensar negativo) """
        diffr2 = diffr.transpose()
        meanpcdif = diffr2.mean()
        
        """ Desvio padrão ("STD") da diferença relativa """
        std = diffr2.std()
        std.index = diff.index
        
        """ Raiz do erro quadrático médio (root mean square error, RMSE) """
        diffquad = diff3**2
        diffquad.index = diff.index
            
        diffquad2 = diffquad.transpose()
        rmse = (diffquad2.sum()/diffquad2.count())**0.5
        rmse.index = diff.index
        
        """ Chi-quadrado """
        chiquad = (diff3**2)/controle3
        for k in range(0,len(chiquad.columns)):
            chiquad[k] = np.where(np.isinf(chiquad[k]), (diff3[k]**2)/1, chiquad[k])
            #verifica se valor é infinito (resultado da divisão por 0, obtido quando o total de controle é 0) e substitui por 0
        chiquad.index = diff.index
        chi2zona = chiquad.sum() #XXX verif
        chiquad2 = chiquad.transpose()
        chi2var = chiquad2.sum()
       
        estatisticas = pd.DataFrame({'Media':meanpcdif, 'STD':std, 'RMSE':rmse, 'Chi2':chi2var})
        totaiscont = pd.DataFrame({'Cont':totcont})
        totaissint = pd.DataFrame({'Sint':totsint})
        chi2zona = pd.DataFrame({'Chi2':chi2zona}) #XXX verif
        print(estatisticas)
        
        """ Nomeia arquivo em função do momento que ele foi gerado e do máximo fator de expansão utilizado """
        
        # Para incluir peso adotado para a variável de sexo (masculino) no nome do arquivo
        if ctrlp.iloc[13,0]=="p_sex_masc": 
            peso_sex = ctrlp.iloc[13,1]
        else : peso_sex = "Nctrl"
        
        # Para incluir máximo fator de expansão adotado
        maxexpfac = iamil["max_expansion_factor"]
        
        t = datetime.datetime.now()
        month = t.month
        day = t.day
        hour = t.hour
        minute = t.minute
        time = [month, day, hour, minute]
        for x in range(4):
            if time[x] < 10: time[x] = str("0"+str(time[x]))
        
        nome = str(t.year)+str(time[0])+str(time[1])+'_'+str(time[2])+str(time[3])+"_PSBr_Estatisticas"+geografias[i]+"_FatExp"+str(maxexpfac)+".xlsx"
       
        with pd.ExcelWriter(valid+nome) as writer:
            ctrlp.to_excel(writer, sheet_name='Atributos & Pesos')    
            controle.to_excel(writer, sheet_name='Totais Controle')
            sint.to_excel(writer, sheet_name='Sintetizado')
            diff.to_excel(writer, sheet_name='Diferença')
            diffr.to_excel(writer, sheet_name='Diferença Relativa')
            diffquad.to_excel(writer, sheet_name='Dif^2')
            chiquad.to_excel(writer, sheet_name='ChiQuad')
            estatisticas.to_excel(writer, sheet_name='StatsVariaveis')
            chi2zona.to_excel(writer, sheet_name='ChiQuadZonas')
            totaiscont.to_excel(writer, sheet_name='TotControle')
            totaissint.to_excel(writer, sheet_name='TotSintetizado')
            
        diffr.columns = summ["id"]
        diffquad.columns = summ["id"] 
        chiquad.columns = summ["id"] 
        diffr = diffr.transpose()
        diffquad = diffquad.transpose()
        chiquad = chiquad.transpose()
        chiquad["ChiQuadAtr"] = chiquad.sum(axis=1)
        diffr.to_csv(valid+geografias[i]+'DiferençaRelativa'+'.csv')
        diffquad.to_csv(valid+geografias[i]+'DiferençaQuad'+'.csv')
        chiquad.to_csv(valid+geografias[i]+'ChiQuad'+'.csv')
        
        print(">>> Atributos: "+str(num_atr))
        print(">>> Arquivo "+nome+" gerado!")
        print(geografias)
        print(i)
        print(time)

""" Para avaliação de variaveis combinadas """
if varcombinadas == 1:
    per = pd.read_csv(output+synp, sep=',', engine='python') #le synthetic_persons.csv
    print(per)
    per["SEXSTR"] = np.where(per["SEX"]==1, "M", "F")
    per["AGESTR1"] = np.where((per["AGEP"]>=20), "Qua", per["AGEP"])
    per["AGESTR2"] = np.where((per["AGEP"]<=29), "Qua", per["AGEP"])
    per["AGESTR3"] = np.where((per["AGEP"]>=50), "Set", per["AGEP"])
    per["AGESTR4"] = np.where((per["AGEP"]<=59), "Set", per["AGEP"])
    per["AGESTR"] = np.where(per["AGESTR1"]==per["AGESTR2"], per["AGESTR1"], "--")
    per["AGESTR"] = np.where(per["AGESTR3"]==per["AGESTR4"], per["AGESTR3"], per["AGESTR"])
    per["AGESEX"] = per["SEXSTR"]+per["AGESTR"]
    per2 = per[["AGESEX","per_num"]]
    combinadas = pd.pivot_table(per2, index='AGESEX', aggfunc=np.count_nonzero)
    per = per[["AGEP","SEX","AGESEX"]]
    per.to_csv(valid+pastacomb+"VarComb_SynPer.csv")
    combinadas.to_csv(valid+pastacomb+"VarComb_Agregado.csv")
