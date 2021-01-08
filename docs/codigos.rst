Códigos desenvolvidos
========

Códigos de tratamento de dados de entrada
-----------

a. Área a Sintetizar
~~~~~~~~~~~

O código em Python aAreaSintetizar gera o arquivo de entrada “geo_cross_walk.csv” a partir da (i) lista de municípios inserida pelo usuário no arquivo Municipios.yaml e da (ii) lista de correspondência entre setores censitários e áreas de ponderação do IBGE (arquivo XXXX,  a partir do qual podem ser extraídos distrito e município a partir do código do setor censitário).

::

  TAZ,PUMA,REGION
  350390105000001,3503901003001,3503901
  350390105000002,3503901003001,3503901
  350390105000003,3503901003001,3503901
  350390105000004,3503901003001,3503901
  350390105000005,3503901003002,3503901
  350390105000006,3503901003002,3503901
  
**Municipios.yaml: Arquivo contendo lista de municípios a sintetizar**

De forma a facilitar o trabalho do usuário e evitar eventuais alterações involuntárias do código, um arquivo de extensão .yaml é utilizado para a identificação dos municípios de interesse para a sintetização. A extensão de .yaml pode ser visualizada com um software de bloco de notas comum e tem como premissa a exibição de fácil leitura de dados de entrada: os diferentes itens de uma lista são indicados através de "bullet points", sem a necessidade de colchetes ou aspas.

Um exemplo de arquivo de entrada é apresentado a seguir, contendo as 4 variáveis mínimas: estado (nome do estado por extenso), abreviacao_UF (abreviação oficial da unidade federativa), tag_rmsp (indica se os municípios fazem parte da RMSP – 1 – ou não – 0) e municípios (lista de municípios a gerar população sintética).


::

  estado: Acre
  abreviacao_uf: AC
  tag_rmsp: 0

  municipios:
      - Cruzeiro do Sul
      - Mâncio Lima
      - Rodrigues Alves
  #   - Rio Branco

Visto que o arquivo é lido por um programa em Python, a adição de um símbolo “#” no início da linha faz com que a linha se torne um comentário e assim não seja processada. No exemplo acima, são processados apenas os três primeiros municípios.

Caso haja uma diferença de grafia entre o nome indicado para o município e a base do IBGE, o código aAreaSintetizar.py – que lê este arquivo – deve acusar este erro.
Caso o usuário deseje sintetizar áreas menores (como distritos ou mesmo conjunto de setores censitários), este deve alterar os códigos a, b e c na parte de seleção de municípios.


b. Totais de controle
~~~~~~~~~~~

c. Matriz semente
~~~~~~~~~~~

d. Meta controles: ODSP 2017
~~~~~~~~~~~

e. Meta controles: RAIS 2010
~~~~~~~~~~~

Códigos de validação
----------

a. Qualidade do ajuste
~~~~~~~~~~~

b. Gráficos
~~~~~~~~~~~
