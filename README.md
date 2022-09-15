# AutomatizeStuff
Programs to automatize repeated tasks from work

O objetivo deste programa é extrair informações específicas (que contenham a palavra "COGERH") de PDFs presentes em uma página web ("https://www.pge.ce.gov.br/download/modalidade-da-lei-n-13303/") e enviar estas informações - organizadas em uma tabela - por e-mail, para determinadas pessoas. Vale ressaltar que o(s) PDF(s) têm uma estrutura homogênea (na maior parte do tempo).
Essa versão usa o Chromedriver. Por usar a biblioteca Camelot (que depende do Tkinter), não é possível ainda fazer o deploy dela. Como alternativa para atividades de frequência diária, por exemplo, podemos criar um executável dele e/ou inseri-lo no agendador de tarefas do Windows.

The goal of this code is to extract specific information (rows that contain the word "COGERH") from PDFs which are part of a webpage ("https://www.pge.ce.gov.br/download/modalidade-da-lei-n-13303/") and send those information - organized in a table - by e-mail. The PDFs present themselves - most of the time - with an homogeneous structure. 
