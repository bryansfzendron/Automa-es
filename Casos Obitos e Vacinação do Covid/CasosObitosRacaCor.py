import zipfile
import requests
from datetime import date
from time import sleep
from tkinter import *
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import logging
import logging.handlers

datahj = date.today()
dataArquivo = str(datahj.strftime("%d-%m-%Y"))
nmArquivo = str(datahj.strftime("CasosObitosRacaCor.py - %d_%m_%Y.txt"))
DataEmail = str(datahj.strftime("%d/%m/%Y - %H:%M:%S"))

def enviaEmail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("bryan.zendron@gmail.com", "mrthnteqeohcaayw")
    corpo = ""
    enviarEmail = MIMEMultipart()
    enviarEmail['From'] = "bryan.zendron@gmail.com"
    enviarEmail['to'] = "bryan.38337@santanadeparnaiba.sp.gov.br;luciano.38265@santanadeparnaiba.sp.gov.br" 
    enviarEmail['subject'] = "Erro na Execução de Casos e Obitos Raca Cor.py na data "+DataEmail
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
    url = 'https://github.com/seade-R/dados-covid-sp/raw/master/data/casos_obitos_raca_cor.csv.zip'
    def baixar_arquivo(url, endereco):
       resposta= requests.get(url)
       with open(endereco, 'wb') as covidobitos:
           covidobitos.write(resposta.content)
except Exception as e: 

    logging.error(e)    
    enviaEmail()

try:      
    if __name__ == "__main__":
        baixar_arquivo(url,'CovidObitos.zip')

        with zipfile.ZipFile("CovidObitos.zip","r") as zip_ref:
            zip_ref.extractall(r"C:\Gdrive\Dados_Publicos_SP\Saude\Seade-R")
        print("finalizado")    
except Exception as e: 

    logging.error(e)    
    enviaEmail()