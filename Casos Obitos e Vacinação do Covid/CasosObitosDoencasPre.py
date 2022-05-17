import zipfile
import requests
from lib2to3.pgen2 import driver
from datetime import datetime
import datetime
from tkinter import *
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import logging
import logging.handlers

datahj = datetime.datetime.now()
dataArquivo = str(datahj.strftime("%d-%m-%Y"))
nmArquivo = str(datahj.strftime("CasosObitosDoencasPre.py - %d_%m_%Y.txt"))
DataEmail = str(datahj.strftime("%d/%m/%Y - %H:%M:%S"))

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=r'C:\Gdrive\Dados_Publicos_SP\python\Logs de Erro/'+nmArquivo,
                    filemode='w',
                    level=logging.DEBUG,
                    format=log_format)

def enviaEmail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("bryan.zendron@gmail.com", "mrthnteqeohcaayw")
    corpo = ""
    enviarEmail = MIMEMultipart()
    enviarEmail['From'] = "bryan.zendron@gmail.com"
    enviarEmail['to'] = "bryan.38337@santanadeparnaiba.sp.gov.br;luciano.38265@santanadeparnaiba.sp.gov.br" 
    enviarEmail['subject'] = "Erro na Execução de Casos e Obitos Doenças pré.py na data "+DataEmail
    enviarEmail.attach(MIMEText(corpo, 'plain'))
    attchment = open(r'C:\Gdrive\Dados_Publicos_SP\python\Logs de Erro/'+nmArquivo, 'rb')
    att = MIMEBase('application', 'octet=stream')
    att.set_payload(attchment.read())
    encoders.encode_base64(att)
    att.add_header('Content-Disposition', f'attachment; filename = {nmArquivo}')
    attchment.close
    enviarEmail.attach(att)
    server.sendmail(enviarEmail["From"], enviarEmail["To"].split(";"), enviarEmail.as_string())
    server.quit()

try:
    url = 'https://github.com/seade-R/dados-covid-sp/raw/master/data/casos_obitos_doencas_preexistentes.csv.zip'
    def baixar_arquivo(url, endereco):
       resposta= requests.get(url)
       with open(endereco, 'wb') as covidobitos:
           covidobitos.write(resposta.content)
    print("Baixado")

except Exception as e: 
    logging.error(e)    
    enviaEmail()

try:
    if __name__ == "__main__":
        baixar_arquivo(url,'casos_obitos_doencas_preexistentes.zip')

    with zipfile.ZipFile("casos_obitos_doencas_preexistentes.zip","r") as zip_ref:
        zip_ref.extractall(r"C:\Gdrive\Dados_Publicos_SP\Saude\Seade-R")
    print("Finalizado")
except Exception as e: 
    logging.error(e)    
    enviaEmail()