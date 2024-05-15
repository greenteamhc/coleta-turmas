O código **coleta-turmas.py** tem como objetivo coletar as turmas nas quais os integrantes do GTHC foram matriculados e retornar um arquivo contento nome, RA e turma.

Os PDFs de deferimentos, enquanto tiverem que ser substituídos manualmente, podem ser pegos em:

+ [prograd.ufabc.edu.br/matriculas](https://prograd.ufabc.edu.br/matriculas) - Para o quadrimestre atual, caso disponível, ou;
+ [prograd.ufabc.edu.br/matriculas/arquivo](https://prograd.ufabc.edu.br/matriculas/arquivo) - Para quadrimestres anteriores.

<br>

No mesmo diretório em que o código **coleta-turmas.py** estiver, deve haver também um arquivo *csv* (normalmente o arquivo de recadastro de membros), com a **nome do integrante na terceira coluna** e o **RA do mesmo na quinta coluna** seguindo o seguinte padrão:

```
Coluna_1,Coluna_2,Nome_completo,Coluna_4,RA, ... ,Coluna_N
info_1_1,info_2_1,Nome_completo_1_1,Coluna_4_1,RA_1, ... ,Coluna_N_1
info_1_2,info_2_2,Nome_completo_2_2,Coluna_4_2,RA_2, ... ,Coluna_N_2
...
info_1_N,info_2_N,Nome_completo_4_N,Coluna_4_N,RA_N, ... ,Coluna_N_M
```

A saída do código tem formato *csv* separado por ponto e vírgula e segue o seguinte padrão:

```
Name,RA,Group
Nome_1;RA_1;turma_deferida_1-1
Nome_1;RA_1;turma_deferida_1-2
Nome_2;RA_2;turma_deferida_2-1
...
Nome_N;RA_N;turma_deferida_N-M
```