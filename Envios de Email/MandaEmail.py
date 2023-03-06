
from email import encoders
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import datetime
import logging
import logging.handlers

#esse import serve apenas para envio de logs de erro pelo telegram através do bot
from BotTelegram import telegram_bot_sendtext_simple

datahj = datetime.datetime.now()
nmArquivo = str(datahj.strftime("MandaEmail.py - %d_%m_%Y.txt"))
caminhoLog = r'D:\Gdrive\Dados_Publicos_SP\python\Logs de Erro/'
GMAIL_ID = 'Seu Email'
GMAIL_PWD = 'senha de app configurada no GMAIL'

log_format = '%(desctime)s:%(levelname)s:%(filename)s:%(message)s'
logging.basicConfig(filename=caminhoLog+nmArquivo,
                    filemode='w',
                    format=log_format)

def enviaEmail(assunto,caminho,destino,nomeArquivo):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  
        server.login(GMAIL_ID, GMAIL_PWD)  
        corpo = ""
        enviarEmail = MIMEMultipart()
        enviarEmail['From'] = GMAIL_ID
        enviarEmail['to'] = destino 
        enviarEmail['subject'] = assunto
        enviarEmail.attach(MIMEText(corpo, 'plain'))
        attchment = open(caminho+nomeArquivo, 'rb')
        att = MIMEBase('application', 'octet=stream')
        att.set_payload(attchment.read())
        encoders.encode_base64(att)
        att.add_header('Content-Disposition', f'attachment; filename = {nomeArquivo}')
        attchment.close
        enviarEmail.attach(att)
        server.sendmail(enviarEmail["From"], enviarEmail["To"].split(";"), enviarEmail.as_string())
        server.quit()
    except Exception as e: 
        logging.error(e)    
        telegram_bot_sendtext_simple(bot_message='MandaEmail.py - '+str(e))

def enviaEmailSimples(assunto,destino,corpo):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)   
        server.login(GMAIL_ID, GMAIL_PWD)  
        enviarEmail = MIMEMultipart()
        enviarEmail['From'] = GMAIL_ID
        enviarEmail['to'] = destino 
        enviarEmail['subject'] = assunto
        enviarEmail.attach(MIMEText(corpo, 'plain'))
        server.sendmail(enviarEmail["From"], enviarEmail["To"].split(";"), enviarEmail.as_string())
        server.quit()
    except Exception as e: 
        logging.error(e)    
        telegram_bot_sendtext_simple(bot_message='MandaEmail.py - '+str(e))

if __name__ == '__main__':
    print(__package__)
    print("Main")

