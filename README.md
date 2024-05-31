O código **coleta-turmas.py** tem como objetivo coletar as turmas nas quais os integrantes do GTHC foram matriculados e retornar um arquivo contento nome, RA e turma. Os PDFs são selecionados automaticamente de acordo com a data atual.



No mesmo diretório em que o código **coleta-turmas.py** estiver, deve haver também um arquivo *csv* (normalmente o arquivo de recadastro de membros), com a **nome do integrante na terceira coluna** e o **RA do mesmo na quinta coluna** seguindo o seguinte padrão:

```
Coluna_1,Coluna_2,Nome_completo,Coluna_4,RA, ... ,Coluna_N
info,info,Nome_completo,Coluna,RA, ... ,Coluna_N
info,info,Nome_completo,Coluna,RA, ... ,Coluna_N
...
```

A saída do código tem formato *csv* separado por ponto e vírgula e segue o seguinte padrão:

```
Name,RA,Group
Nome;RA;turma_deferida
Nome;RA;turma_deferida
Nome;RA;turma_deferida
...
```