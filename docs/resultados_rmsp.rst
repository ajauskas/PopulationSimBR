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

+-------------------------------------+----------------------------------------------------------------------+
| Código do atributo                  | Descrição                                                            |
+=====================================+======================================================================+
| household_id                        | Id do domicílio                                                      |
+-------------------------------------+----------------------------------------------------------------------+
| PUMA                                | Área de ponderação                                                   |
+-------------------------------------+----------------------------------------------------------------------+
| TAZ                                 | Setor censitário                                                     |
+-------------------------------------+----------------------------------------------------------------------+

Downloads
---------

* Download das bases de **domicílios** sintéticos: 

  * RMSP apenas SP: synthetic_households1.csv (3.000.000 domicílios, 156 MB)
  * RMSP exc. SP: synthetic_households2.csv (3.000.000 domicílios, XXX MB)


* Download das bases de **indivíduos** sintéticos:

  * RMSP apenas SP: synthetic_persons1.csv (10.000.000 indivíduos, 396 MB)
  * RMSP exc. SP: synthetic_persons2.csv (9.000.000 indivíduos, XXX MB)
