# sistema-especialista-Identificador-de-Insetos-pela-frequencia-de-batimento-de-asas
#Autor: Bruno Pires Lourenço

1. INTRODUÇÃO
  O reconhecimento automatizado de insetos é uma demanda para os agricultores, pois possibilita a aplicação correta dos métodos defensivos para as lavouras com uma diminuição nos custos de produção devido a substituição de um especialista humano (mais custoso) por um sistema de especialista. Na região sul temos uma grande produção frutífera, dentre elas a produção de pêssego. Na produção de pêssego uma das pragas que causam grande perda na produção e restrições para a exportação dos frutos são as moscas-das-frutas, sendo a Anastrepha fraterculus e a Ceratitis capitata as duas com maiores incidências.

  Como método defensivo os produtores fazem uso de armadilhas como MacPhail para o monitoramento manual da praga e avaliação da quantidade e tipo de defensivo agrícola para ser aplicado, sendo este método bastante ineficiente e custoso devido a erros de identificação e custo de um especialista humano.

  Uma alternativa para melhorar o monitoramento é o uso de armadilhas inteligentes que possam identificar e contar corretamente as moscas-das-frutas, fazendo uso de métodos de inteligencia artificial. Um dos métodos de inteligencia artificial que podem aplicados são os sistemas especialistas.

  O sistema especialista é um método de inteligencia artificial especializado na execução de determinada tarefa utilizado para substituir um especialista humano. Um dos métodos utilizados para o desenvolvimento de sistemas especialista é o sistema fuzzy baseado em regras como classificador. Assim é utilizado o sistema fuzzy para traduzir o conhecimento de um especialista humano em um algoritmo para ser aplicado ao sistema de identificação de insetos 

  Assim, este trabalho consiste no desenvolvimento de um classificador de moscas-das-frutas utilizando o sistemas fuzzy baseado em regras. O conhecimento do especialista pode ser obtido no artigo https://www.mdpi.com/1424-8220/19/5/1254, onde foi realizado um trabalho de desenvolvimento e avaliação de uma armadilha inteligente para as moscas-das-frutas de interesse e também podem ser realizadas perguntas ao professor sobre o comportamento dos insetos.

  Os dados gerados pela a armadilha são os sinais do batimento de asas capturados com passagem de insetos pela armadilha que foram processados utilizando o método da autocorrelação e transformada rápida de Fourier, sendo com a autocorrelação foi medido a frequência fundamental do sinal e com a transformada rápida de Fourier foram medidas a frequências fundamental até a 5ª harmônica e as intensidades dos picos correspondentes as frequências fundamental até a 5ª harmônica.

  As características extraídas da passagem de cada inseto foram armazenadas em dois arquivos .csv. Um para a Anastrepha fraterculus (A_fraterculus.csv) com o sinal capturado de 397 moscas e outro para a Ceratitis capitata (C_capitata.csv) com o sinal capturado de 429 moscas. Nos arquivos cada linha corresponde a uma passagem de inseto e cada coluna corresponde conforme a seguir:


- F0-Autocorrelação: frequência fundamenta pela autocorrelação;
- F0-FFT: frequência fundamenta pela FFT;
- F1-FFT: 2ª harmônica pela FFT;
- F2-FFT: 3ª harmônica pela FFT;
- F3-FFT: 4ª harmônica pela FFT;
- F4-FFT: 5ª harmônica pela FFT;
- E0-FFT: Intensidade frequência fundamenta pela FFT;
- E1-FFT: Intensidade 2ª harmônica pela FFT;
- E2-FFT: Intensidade 3ª harmônica pela FFT;
- E3-FFT: Intensidade 4ª harmônica pela FFT;
- E4-FFT: Intensidade 5ª harmônica pela FFT;


2. SISTEMA
  Para o desenvolvimento do trabalho foi preciso estabelecer as entradas e saídas do sistema de controle. As funções de entrada são instanciadas com o método Antecedent, que recebe como parâmetros o conjunto universo da variável de entrada e uma etiqueta para identificar tal variável. Já para determinar a saída do sistema, deve ser utilizado o método Consequent, que recebe como parâmetros os mesmos dados, entretanto, referentes à variável de saída. No código a baixo estão as declarações das entradas e saída do sistema de controle.
```
freq_F0_aut = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F0_aut')
freq_F0_FFT = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F0_FFT')
freq_F1_F0 = ctrl.Antecedent(np.arange(0, freq_limit, 0.5), 'freq_F1_F0')
mosca = ctrl.Consequent(np.arange(0, freq_limit, 0.5), 'mosca')
```
  De acordo com os dados apresentados no artigo, foi realizada a fuzzyficação para as duas classes, levando em consideração as entradas: F0-Autocorrelação, F0-FFT e a diferença entre a segunda componente e frequência fundamental obtidas pela FFT. A biblioteca scikit-fuzzy apresenta o método fuzz.membership.gaussmf, que gera uma função de pertinência para uma distribuição gaussiana (normal). Esse método recebe como parâmetros um vetor com os valores da variável independente, o valor da variável relativo ao centro da distribuição e o valor do desvio padrão, respectivamente. Para cada “nível” das variáveis de entrada e de saída, é preciso identificar essas funções de pertinência.
  Além da distribuição gaussiana, também foi utilizada a função trapmf, que gera por sua vez, uma função trapezoidal para a pertinência da classe. Para as variáveis do sistema de controle, a fuzzyficação foi realizada da seguinte forma:  
```
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
```
  Após o estabelecimento das funções de pertinência do sistema, é possível visualizá-las através do comando view. Esse comando gera um gráfico com as funções de pertinência para cada variável do sistema. Após serem executados os quatro comandos abaixo, foi possível gerar os gráficos de pertinência.
```
freq_F0_aut.view()
freq_F0_FFT.view()
freq_F1_F0.view()
mosca.view()
```
  A partir das funções de pertinência do sistema, foi possível estabelecer as regras do mesmo. Essas regras são geradas a partir do método skfuzzy.control.Rule, que relaciona uma condição composta pelas variáveis de entrada com uma função de pertinência da variável de saída. Para a composição das condições podem ser utilizados os operadores | (OR), & (AND), ~ (NOT) e parênteses para o agrupamento de termos. 
Após analisar a identificação das classes utilizando cada um dos arquivos de teste, foi possível estabelecer regras condizentes com o sistema. O método utilizado foi o de tentativa e erro, no qual buscou-se que a quantidade de moscas do tipo oposto ao do arquivo fosse menor possível. A seguir estão relacionadas as regras de inferência para o sistema implementado:
```
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
```
  Com as regras estabelecidas, foi preciso atribuí-las ao sistema e, também, necessário a instanciação da simulação do sistema de controle, para que seja possível inserir valores de entrada e avaliar as respostas dessas entradas. Essas duas ações foram realizadas por meio da execução do seguinte código:
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4 , rule5, rule6, rule7, rule8])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
  Para indicar quais serão as entradas do sistema é preciso utilizar o método input, indicando a qual variável de entrada determinado dado será atribuído. Após fazer isso, deve-se executar o comando compute para iniciar a simulação do sistema e, então visualizar o gráfico da saída do sistema com o seu resultado com o comando view.
```
tipping.input['freq_F1_F0'] = in_F1_F0
tipping.input['freq_F0_FFT'] = in_F0_FFT
tipping.input['freq_F0_aut'] = in_F0_aut
    
tipping.compute()
mosca.view(sim=tipping)
```

  Entretanto, não é possível extrair diretamente a pertinência de cada classe a partir da simulação do sistema de controle. Portanto, foi preciso calcular a pertinência de cada classe de saída com o método interp_membership. 
Para identificar as moscas a partir dos dados dos arquivos, foi utilizado um laço para iteração de todas as amostras. Os dados de entrada de cada amostra são atribuídos às variáveis de entrada do sistema de controle; é calcula a saída do sistema a partir dessas variáveis e então é avaliada a pertinência de cada classe. Para determinação da classe a qual amostra faz parte, é avaliada a classe com maior pertinência através da função calculaPertinencia(), que executa os dois blocos de comandos exibidos logo acima desse parágrafo.
```
n_capitata = 0
n_fraterculus = 0
n_nehuma_a = 0

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
print('--------------------------------------------')
print()
print("resultado Fraterculus")   
print('n_capitata', n_capitata)
print( 'n_fraterculus' ,n_fraterculus)
print( 'n_nehuma', n_nehuma_a)
print()
```
  O mesmo algoritmo também é aplicado aos dados do arquivo referente à mosca Capitata:
```
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
    
    mosca.view(sim=tipping)
    
    resultado_amostra = calculaPertinencia()
    if(resultado_amostra[0]=='Classe Capitata'):
        n_capitata+=1
    if(resultado_amostra[0]=='Classe Fraterculus'):
        n_fraterculus+=1
    if(resultado_amostra[0]=='Não é mosca'):
        n_nehuma_a+=1
print('--------------------------------------------')
print()
print("resultado Capitata")   
print('n_capitata', n_capitata)
print( 'n_fraterculus' ,n_fraterculus)
print( 'n_nehuma', n_nehuma_a)
print()
```
  Após a avaliação dos dois arquivos de teste, foi implementada a inserção de novas entradas a serem classificadas de um arquivo csv. As etapas de aquisição dos dados e de iteração através das entradas do arquivo foram aproveitadas dos algoritmos que já haviam sido implementados no script.


3. RESULTADOS
  Ao executar o script em posse dos arquivos Dataset C. capitata.csv e Dataset C. Fraterculus.csv, foram obtidos os resultados que podem ser visualizados na tabela abaixo:
 | First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
  Ao se analisar a tabela acima, é possível perceber que quase a totalidade das entradas de cada um dos arquivos foram classificadas ou como o tipo de mosca correspondente ao arquivo ou foram identificadas como não pertencendo a nenhum dos grupos.


4. CONCLUSÃO
  Os resultados obtidos foram satisfatórios, visto que as regras de inferência foram construídas a partir da análise de apenas uma porção dos dados coletados.
