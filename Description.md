# sistema-especialista-Identificador-de-Insetos-pela-frequencia-de-batimento-de-asas

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
