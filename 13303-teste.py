#!/usr/bin/env python
# coding: utf-8

# # Extrair dados de site web
O objetivo deste programa é extrair informações específicas (que contenham a palavra "COGERH") de PDFs presentes em uma página web ("https://www.pge.ce.gov.br/download/modalidade-da-lei-n-13303/") e enviar estas informações - organizadas em uma tabela - por e-mail, para determinadas pessoas. Vale ressaltar que o(s) PDF(s) têm uma estrutura homogênea (na maior parte do tempo).

Essa versão usa o Chromedriver. Por usar a biblioteca Camelot (que depende do Tkinter), não é possível ainda fazer o deploy dela. Como alternativa para atividades de frequência diária, por exemplo, podemos criar um executável dele e/ou inseri-lo no agendador de tarefas do Windows.
# Importar bibliotecas

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import camelot
import time
import pandas as pd


# Baixar os PDFs dos quais queremos extrair as informações

# In[2]:


# acessar o site
driver = webdriver.Chrome(r'C:\Users\Micaella\miniconda3\chromedriver.exe')
driver.get("https://www.pge.ce.gov.br/download/modalidade-da-lei-n-13303/")
time.sleep(5)


# In[3]:


# detectar o número de PDFs disponiveis por meio da classe "listfiles__link"
elementos = driver.find_elements(by=By.CLASS_NAME, value='listfiles__link')
j = len(elementos)


# In[4]:


# baixar os arquivos para a pasta onde se encontra o programa (a pasta Downloads)
home = os.path.expanduser('~')
home
location = os.path.join(home, 'Downloads')
location_ = []

for elemento in range(j):
    elementos[elemento].click()
    location_.append(os.path.join(location, f'{elementos[elemento].text}'))
time.sleep(5)


# Extrair informações das linhas do(s) PDF(s) que contêm a palavra "COGERH"

# In[5]:


dfs = []
ind = []
ind0 = []

for file in location_:
    if file.endswith('pdf'):
        tables = camelot.read_pdf(file, pages='all', line_scale = 40)
        for table in tables:
            df = table.df
            dfs.append(df)
            df = pd.concat(dfs, axis = 0, ignore_index = True)
            ind0 = df.loc[df[1].str.contains('COGERH')].index
            ind0 = list(ind0)
            ind = df.loc[(df[1].str.contains('COGERH')) & ~(df[2].str.endswith('.')) & ~(df[3].str.endswith('.'))].index
            for i in ind:
                if i < (len(df)-1):
                    i+=1
                    ind0.append(i)


# Transformar as informações em um novo dataframe e convertê-lo para html

# In[6]:


# tratar a tabela, removendo registros duplicados e inserindo legendas
df = df.iloc[sorted(ind0),:]
df.drop_duplicates(inplace=True)
df.replace(r"\n", "  ", regex=True, inplace=True)
df = df.rename(columns = {df.columns[0] : 'Número da Licitação', df.columns[1] : 'Número VIPROC', df.columns[2] : 'Objeto', df.columns[3] : 'Situação'})
# converter em html
email = df.to_html(classes='table table-stripped')


# Enviar a tabela para os e-mails listados

# In[1]:


# aqui é necessário ter um token da SendGrid para usar a API deles de envio de e-mails


# In[10]:


message = Mail(
    from_email='xxx@gmail.com',
    to_emails=[('xxx@yahoo.com.br'),('yyy@gmail.com'),('www@cogerh.com.br')],
    subject='Andamento dos processos lei n13.303',
    html_content= email)
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)

