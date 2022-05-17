import requests
import os, os.path, datetime
from time import sleep
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import logging
import logging.handlers

datahj = datetime.datetime.now()
datahoje = datahj.strftime("%Y%m%d")
datao = datahj - datetime.timedelta(days=1)
dataontem = datao.strftime("%Y%m%d")
datanto = datahj - datetime.timedelta(days=2)
data2diasAtras = datanto.strftime("%Y%m%d")
mesO = datao.strftime("%m")
anoO = datao.strftime("%Y")
caminho = (r'C:/Gdrive/Dados_Publicos_SP/Saude/Vacinacao/RankingAplicacaoDoses.csv')
dataArquivo = str(datahj.strftime("%d-%m-%Y"))
nmArquivo = str(datahj.strftime("RankingAplicacaoV2.py - %d_%m_%Y.txt"))
DataEmail = str(datahj.strftime("%d/%m/%Y - %H:%M:%S"))
url = f'https://www.saopaulo.sp.gov.br/wp-content/uploads/{anoO}/{mesO}/{dataontem}_ranking_aplicacao_doses.csv'

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
    enviarEmail['subject'] = "Erro na Execução RankingAplicacaoV2.py na data "+DataEmail
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


def baixar_arquivo(url, caminho):
    resposta = requests.get(url, headers={'User-Agent': 'Custom'})
    if resposta.status_code == requests.codes.OK:
        with open(caminho, 'wb') as novo_arquivo:
                novo_arquivo.write(resposta.content)
        print("Download finalizado. Arquivo salvo em: {}".format(caminho))
    else:
        resposta.raise_for_status()

try:
    if __name__ =="__main__":
        baixar_arquivo(url = url,caminho=caminho)
except Exception as e: 
    logging.error(e)    
    enviaEmail()