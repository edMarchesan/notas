# notas
Projeto para facilitar a emissao de notas de produto e servicos para MEIs do RS

Instrucoes
*Necessário ter Python instalado
*Necessário ter as libraries no arquivo requirements.txt instalado, recomendo o uso do pip install para isso

1 - Faca o download da pasta em zip e extraia no seu Computador, pode ser em qualquer pasta.
2 - Certifique-se de que a pasta contenha o arquivo icone.ico, pois sem ele o programa retornará um erro.
3 - Insira no arquivo empresas.txt os dados da empresa que deseja cadastrar (este passo pode ser feito diretamente quando o programa rodar).
4 - O arquivo deve apresentar uma empresa por linha, na seguinte formatacao NOME|CPF|DATA DE NASCIMENTO|CNPJ|NIRE OU NOME DA MAE|SENHA GOV.BR.
NOME é o que aparecerá para voce selecionar, entao caso queira botar apenas o primeiro, a seu critério.
CPF apenas números.
DATA DE NASCIMENTO apenas números.
CNPJ apenas números.
NIRE OU NOME DA MAE o sistema irá automaticamente detectar se digitar número ele irá selecionar o NIRE, se digitar letrar, irá selecionar o NOME DA MAE.
SENHA GOV.BR é um campo opcional, precisa preencher para fazer notas de servico, mas caso nao queira pode deixar em branco, mas a linha tem que terminar com |.

Depois de configurado, basta executar o programa, "pythonw.exe ./notacomgov.pyw" no terminal na pasta do programa, voce tambem pode criar um .bat para criar um atalho e facilitar, basta adicionar "start pythonw.exe ./notacomgov.pyw" no arquivo e enviar um atalho para a área de trabalho.

O programa utiliza undetected_chromedriver para conseguir preencher a protecao captcha do gov.br, mas o captcha deve ser solucionado manualmente.
O programa utiliza da biblioteca selenium para manipular o navegador, abrir, e inserir os dados conforme inseridos na empresas.txt
Notas baixadas usando o programa ficaram disponiveis na pasta do programa, dentro da pasa downloaded_files

Modo de uso:

1 - Com o programa aberto, ele ira listar as empresas adicionadas, caso nao tenha nenhuma, adicione uma com o botao adicionar empresa.
2 - Para excluir, selecione a empresa e clique em "Excluir empresa".
3 - Para editar, selecione a empresa e clique em "Editar empresa".
4 - Para fazer nota de produto, selecione a empresa e clique em "Nota Produto"
5 - Para fazer nota de servico, selecione a empresa e clique em "Nota Servico"
6- Após finalizar, feche o navegador aberto e em seguida o programa.

