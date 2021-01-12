População Sintética da RMSP
========


Introdução
-----------
A população sintética é dada por dois arquivos: domicílios e indivíduos.
Foi gerada apenas para os domicílios particulares da RMSP (excluídos domicílios coletivos - como orfanatos, presídios e quarteis).

Atributos
---------

Atributos disponíveis na população sintética gerada, tanto controlados como não controlados.

* Domicílios:

  * Número de moradores (NP),
  * ...
  
* Indivíduos:

  * Sexo (SEX),
  * ...

* Em ambas as bases:

  * Id do domicílio (household_id)
  * Área de ponderação (PUMA)
  * Setor censitário (TAZ)
  * 
  
+-------------------------------------+----------------------------------------------------------------------+
| Código do atributo                  | Descrição                                                          |
+=====================================+======================================================================+
| household_id        | Id do domicílio |
+-------------------------------------+----------------------------------------------------------------------+
| PUMA                   | Área de ponderação                                           |
+-------------------------------------+----------------------------------------------------------------------+
| TAZ                 | Setor censitário                                            |
+-------------------------------------+----------------------------------------------------------------------+


Downloads
---------

* Download da base de **domicílios** sintéticos: 

  * RMSP apenas SP: synthetic_households1.csv (156 MB)
  * RMSP exc. SP: synthetic_households2.csv (XXX MB)


* Download da base de **indivíduos** sintéticos:

  * RMSP apenas SP: synthetic_persons1.csv (396 MB)
  * RMSP exc. SP: synthetic_persons2.csv (XXX MB)
