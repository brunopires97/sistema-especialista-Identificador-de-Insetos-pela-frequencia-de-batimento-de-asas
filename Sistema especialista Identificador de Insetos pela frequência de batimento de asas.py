# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl

""" Carregamento dos e adequação dos dados dos arquivos ---------------"""
data_capitata = pd.read_csv('Dataset C. capitata.csv', sep=';', decimal=',')
data_fraterculus = pd.read_csv('Dataset A. fraterculus.csv', sep=';', decimal=',')

F0_aut_capitata = np.round_(data_capitata.iloc[:,0].values,2)
F0_FFT_capitata = np.round_(data_capitata.iloc[:,1].values,2)
F1_FFT_capitata = np.round_(data_capitata.iloc[:,2].values,2)
F1_F0_FFT_capitata = F1_FFT_capitata - F0_FFT_capitata

F0_aut_fraterculus = np.round_(data_fraterculus.iloc[:,0].values,2)
F0_FFT_fraterculus = np.round_(data_fraterculus.iloc[:,1].values,2)
F1_FFT_fraterculus = np.round_(data_fraterculus.iloc[:,2].values,2)
F1_F0_FFT_fraterculus = F1_FFT_fraterculus - F0_FFT_fraterculus
"""--------------------------------------------------------------------"""


freq_limit = 1000.00
f = np.arange(0,freq_limit,0.5)


""" Definição das entradas e saídas do sistema de controle-------------"""
freq_F0_aut = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F0_aut')
freq_F0_FFT = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F0_FFT')
freq_F1_F0 = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F1_F0')
mosca = ctrl.Consequent(np.arange(0, freq_limit, 0.5), 'mosca')
"""--------------------------------------------------------------------"""


""" Funções de pertinência das classes de entrada ('Antecedents') -----"""
freq_F0_aut['baixa'] = fuzz.membership.trapmf(f, (0,0,80,100))
freq_F0_aut['capitata'] = fuzz.membership.gaussmf(f, 160.81 , 10.71)
freq_F0_aut['fraterculus'] = fuzz.membership.gaussmf(f, 113.75 , 7.97)
freq_F0_aut['alta'] = fuzz.membership.trapmf(f, (200,220,freq_limit,freq_limit))

freq_F0_FFT['baixa'] = fuzz.membership.trapmf(f, (0,0,80,110))
freq_F0_FFT['capitata'] = fuzz.membership.gaussmf(f, 162.25 , 13.06)
freq_F0_FFT['fraterculus'] = fuzz.membership.gaussmf(f, 116.40 , 10.09 )
freq_F0_FFT['alta'] = fuzz.membership.trapmf(f, (200,220,freq_limit,freq_limit))

freq_F1_F0['baixa'] = fuzz.membership.trapmf(f, (0,0,80,102))
freq_F1_F0['capitata'] = fuzz.membership.gaussmf(f, 158 , 14.95)
freq_F1_F0['fraterculus'] = fuzz.membership.gaussmf(f, 110.5 , 12.56)
freq_F1_F0['alta'] = fuzz.membership.trapmf(f, (200,220,freq_limit,freq_limit))
"""--------------------------------------------------------------------"""


""" Funções de pertinência das classes de saída ('Consequent') --------"""
mosca['nenhuma'] = fuzz.membership.trapmf(mosca.universe, (0,0,80,102))
mosca['capitata'] = fuzz.membership.gaussmf(mosca.universe, 160.81 , 10.71)
mosca['fraterculus'] = fuzz.membership.gaussmf(mosca.universe, 113.75 , 10.09)
"""--------------------------------------------------------------------"""


""" Espelho das funções de pertinência das classes de saída, que ---------
serão utilizadas para o cálculo da pertinência-------------------------"""
membership_mosca_nehuma = fuzz.membership.trapmf(mosca.universe, (0,0,80,102))
membership_mosca_fraterculus = fuzz.membership.gaussmf(mosca.universe, 113.75 , 10.09)
membership_mosca_capitata = fuzz.membership.gaussmf(mosca.universe, 160.81 , 10.71)
"""--------------------------------------------------------------------"""


""" Visualização das funções de pertinência de cada entrada e da saída """
#oifreq_F0_aut.view()
#freq_F0_FFT.view()
#freq_F1_F0.view()
#mosca.view()
"""--------------------------------------------------------------------"""


""" Definição das regras de inferência para o sistema de controle -----"""
rule1 = ctrl.Rule(freq_F0_aut['baixa']|freq_F0_FFT['baixa'] | freq_F1_F0['baixa'], mosca['nenhuma'])
rule2 = ctrl.Rule(freq_F0_aut['alta'] | freq_F0_FFT['alta'] | freq_F1_F0['alta'], mosca['nenhuma'])

rule3 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta'])) & freq_F0_aut['capitata'] & freq_F0_FFT['capitata'],mosca['capitata'])
rule4 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta'])) & freq_F0_aut['capitata'] & freq_F1_F0['capitata'],mosca['capitata'])
rule5 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta'])) & freq_F1_F0['capitata'] & freq_F0_FFT['capitata'],mosca['capitata'])

rule6 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta']))& freq_F0_aut['fraterculus'] & freq_F0_FFT['fraterculus'],mosca['fraterculus'])
rule7 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta']))& freq_F0_aut['fraterculus'] & freq_F1_F0['fraterculus'],mosca['fraterculus'])
rule8 = ctrl.Rule((~(freq_F0_FFT['baixa'] | freq_F1_F0['baixa']))&(~(freq_F0_FFT['alta'] | freq_F1_F0['alta']))& freq_F1_F0['fraterculus'] & freq_F0_FFT['fraterculus'],mosca['fraterculus'])
"""--------------------------------------------------------------------"""


""" Atribuiçõa das regras ao sistema de controle ----------------------"""
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4 , rule5, rule6, rule7, rule8])
"""--------------------------------------------------------------------"""


""" Instanciação da simulação do sistema de controle ------------------"""
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
"""--------------------------------------------------------------------"""


""" Função que retorna a maior pertinência de um conjunto de entrada --"""
def calculaPertinencia():
    membership_capitata = fuzz.interp_membership(mosca.universe, membership_mosca_capitata, tipping.output['mosca'] )
    membership_fraterculus = fuzz.interp_membership(mosca.universe, membership_mosca_fraterculus, tipping.output['mosca'] )
    membership_nehuma = fuzz.interp_membership(mosca.universe, membership_mosca_nehuma, tipping.output['mosca'] )
    
    if (membership_capitata > membership_fraterculus) and  (membership_capitata > membership_nehuma):
        return 'Classe Capitata', membership_capitata
    
    if (membership_fraterculus > membership_capitata) and  (membership_fraterculus > membership_nehuma):
        return 'Classe Fraterculus', membership_fraterculus
    
    if (membership_nehuma > membership_capitata) and (membership_nehuma > membership_fraterculus):
        return 'Não é mosca', membership_nehuma    
"""--------------------------------------------------------------------"""   


""" Acumuladres para a contagem das ocorrencias de cada classe --------""" 
n_capitata = 0
n_fraterculus = 0
n_nehuma_a = 0
"""--------------------------------------------------------------------"""   


for i in range(0,len(F0_aut_fraterculus)):
    
    in_F0_aut = F0_aut_fraterculus[i]
    in_F0_FFT = F0_FFT_fraterculus[i]
    in_F1_F0 = F1_F0_FFT_fraterculus[i]
       
    tipping.input['freq_F1_F0'] = in_F1_F0
    tipping.input['freq_F0_FFT'] = in_F0_FFT
    tipping.input['freq_F0_aut'] = in_F0_aut
    
    tipping.compute()
       
    resultado_amostra = calculaPertinencia()
    if(resultado_amostra[0]=='Classe Capitata'):
        n_capitata+=1
    if(resultado_amostra[0]=='Classe Fraterculus'):
        n_fraterculus+=1
    if(resultado_amostra[0]=='Não é mosca'):
        n_nehuma_a+=1

    
    """
    if(membership_capitata>0.1):
        print('Amostra ', i)
        print(tipping.output['mosca'])
        print('membership Capitata',membership_capitata)
        print('membership Fraterculus',membership_fraterculus)
        print('membership_mosca_nehuma ',membership_nehuma)
        print('in_F0_aut', in_F0_aut)
        print('in_F0_FFT', in_F0_FFT)
        print('in_F1_F0', in_F1_F0)
        n_capitata+=1
    
    if(membership_fraterculus>0.1):
        #print('membership Fraterculus',membership_fraterculus)
        n_fraterculus+=1
    
    if(membership_nehuma>0.1):
        n_nehuma_a+=1
        #print('membership_nehuma_a ',membership_nehuma)
    #print('membership Nenhuma A',membership_nehuma_a)
    #print('membership Nenhuma B',membership_nehuma_b)
    
    """

print('--------------------------------------------')
print()
print("resultado Fraterculus")   
print('n_capitata', n_capitata)
print( 'n_fraterculus' ,n_fraterculus)
print( 'n_nehuma', n_nehuma_a)
print()
print('--------------------------------------------')


n_capitata = 0
n_fraterculus = 0
n_nehuma_a = 0

for i in range(0,len(F0_aut_capitata)):
    
    in_F0_aut = F0_aut_capitata[i]
    in_F0_FFT = F0_FFT_capitata[i]
    in_F1_F0 = F1_F0_FFT_capitata[i]
     
    tipping.input['freq_F1_F0'] = in_F1_F0
    tipping.input['freq_F0_FFT'] = in_F0_FFT
    tipping.input['freq_F0_aut'] = in_F0_aut
    
    tipping.compute()
    
    #mosca.view(sim=tipping)
    
    resultado_amostra = calculaPertinencia()
    if(resultado_amostra[0]=='Classe Capitata'):
        n_capitata+=1
    if(resultado_amostra[0]=='Classe Fraterculus'):
        n_fraterculus+=1
    if(resultado_amostra[0]=='Não é mosca'):
        n_nehuma_a+=1
    
    """
    membership_capitata = fuzz.interp_membership(mosca.universe, membership_mosca_capitata, tipping.output['mosca'] )
    membership_fraterculus = fuzz.interp_membership(mosca.universe, membership_mosca_fraterculus, tipping.output['mosca'] )
    membership_nehuma = fuzz.interp_membership(mosca.universe, membership_mosca_nehuma, tipping.output['mosca'] )
    
    if(membership_nehuma>0.1):
        n_nehuma_a+=1
    
    if(membership_capitata>0.1):
        n_capitata+=1
    
    if(membership_fraterculus>0.1):
        print('Amostra ', i)
        print(tipping.output['mosca'])
        print('membership Capitata',membership_capitata)
        print('membership Fraterculus',membership_fraterculus)
        print('membership_mosca_nehuma ',membership_nehuma)
        print('in_F0_aut', in_F0_aut)
        print('in_F0_FFT', in_F0_FFT)
        print('in_F1_F0', in_F1_F0)
        n_fraterculus+=1
    """
   
print('--------------------------------------------')
print()
print("resultado Capitata")   
print('n_capitata', n_capitata)
print( 'n_fraterculus' ,n_fraterculus)
print( 'n_nehuma', n_nehuma_a)
print()
print('--------------------------------------------')


#print(tipping.output['mosca'])
#mosca.view(sim=tipping)

entrada = input("Digite o nome do arquivo que deseja-se avaliar: ")
print('Entrada', entrada)

""" Carregamento dos e adequação dos dados do arquivo de teste --------"""
data_teste = pd.read_csv(entrada, sep=';', decimal=',')

F0_aut_teste = np.round_(data_teste.iloc[:,0].values,2)
F0_FFT_teste = np.round_(data_teste.iloc[:,1].values,2)
F1_FFT_teste = np.round_(data_teste.iloc[:,2].values,2)
F1_F0_FFT_teste = F1_FFT_capitata - F0_FFT_capitata

n_capitata = 0
n_fraterculus = 0
n_nehuma_a = 0

print('--------------------------------------------')
print()
print("Arquivo de Teste :")   
print('-------')

for i in range(0,len(F0_aut_teste)):
    
    in_F0_aut = F0_aut_teste[i]
    in_F0_FFT = F0_FFT_teste[i]
    in_F1_F0 = F1_F0_FFT_teste[i]
    
    tipping.input['freq_F1_F0'] = in_F1_F0
    tipping.input['freq_F0_FFT'] = in_F0_FFT
    tipping.input['freq_F0_aut'] = in_F0_aut
    
    tipping.compute()
    #mosca.view(sim=tipping)
    
    

    resultado_amostra = calculaPertinencia()
    print('Amostra:',i,resultado_amostra[0], '\tPertinência: ', resultado_amostra[1] )
    if(resultado_amostra[0]=='Classe Capitata'):
        n_capitata+=1
    if(resultado_amostra[0]=='Classe Fraterculus'):
        n_fraterculus+=1
    if(resultado_amostra[0]=='Não é mosca'):
        n_nehuma_a+=1
        
print('--------------------------------------------')
print()
print("resultado arquivo teste")   
print('n_capitata', n_capitata)
print( 'n_fraterculus' ,n_fraterculus)
print( 'n_nehuma', n_nehuma_a)
print()
print('--------------------------------------------')